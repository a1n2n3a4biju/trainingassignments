
import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Never

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agent_framework import (
    Agent,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    executor,
    handler,
    response_handler,
)

from agent_framework.openai import OpenAIChatClient


# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


def read_setting(name: str) -> str:
    """Read and validate Azure AI Foundry configuration."""

    value = os.getenv(name, "").strip()

    if (
        not value
        or value.startswith("PASTE_")
        or value.startswith("YOUR_")
    ):
        raise ValueError(
            f"Please configure {name} correctly in your .env file."
        )

    return value


# ============================================================
# 2. MANAGER APPROVAL REQUEST
# ============================================================

@dataclass
class ManagerApprovalRequest:
    request: dict
    prompt: str


# ============================================================
# 3. DETERMINISTIC ELIGIBILITY CHECKS
# ============================================================

def check_eligibility(request: dict) -> list:
    """
    Check the return request against the company's
    return policy using deterministic Python conditions.
    """

    issues = []

    amount = float(request["amount_inr"])

    days = int(
        request["days_since_delivery"]
    )

    invoice = request["invoice_available"]

    photos = request["photo_evidence_available"]

    condition = request["item_condition"].upper()

    previous_returns = int(
        request["previous_returns_90_days"]
    )

    # RULE 1: Amount must be below Rs. 25,000

    if amount >= 25000:
        issues.append(
            "Product amount is Rs. 25,000 or above."
        )

    # RULE 2: Return must be within 30 days

    if days > 30:
        issues.append(
            "Return request exceeds 30 days from delivery."
        )

    # RULE 3: Invoice must be available

    if not invoice:
        issues.append(
            "Customer invoice is missing."
        )

    # RULE 4: Item must be unopened OR damaged with photographs

    valid_condition = (
        condition == "UNOPENED"
        or (
            condition == "DAMAGED"
            and photos
        )
    )

    if not valid_condition:
        issues.append(
            "Item condition does not satisfy the return policy."
        )

    # RULE 5: Fewer than 3 previous returns

    if previous_returns >= 3:
        issues.append(
            "Customer has 3 or more previous returns within 90 days."
        )

    return issues


# ============================================================
# 4. BUILD MULTI-AGENT WORKFLOW
# ============================================================

def build_workflow(chat_client: OpenAIChatClient):

    # --------------------------------------------------------
    # AGENT 1: ELIGIBILITY AGENT
    # --------------------------------------------------------

    eligibility_agent = Agent(
        client=chat_client,
        name="EligibilityAgent",
        instructions=(
            "You are an e-commerce returns eligibility specialist. "

            "Review the customer's return request against "
            "the company's return policy. "

            "The policy requires: "
            "product amount below Rs. 25,000, "
            "return within 30 days, "
            "invoice availability, "
            "unopened item or damaged item with photographs, "
            "and fewer than three previous returns in 90 days. "

            "Identify eligibility issues and explain exceptions. "

            "Do not make the final approval decision. "
            "Deterministic Python checks determine eligibility. "

            "Provide a concise and clear assessment."
        ),
    )

    # --------------------------------------------------------
    # AGENT 2: RISK AGENT
    # --------------------------------------------------------

    risk_agent = Agent(
        client=chat_client,
        name="RiskAgent",
        instructions=(
            "You are an e-commerce returns risk assessment specialist. "

            "Analyze the return request for suspicious patterns. "

            "Consider high-value products, "
            "unusual return frequency, "
            "and missing evidence. "

            "Mark HIGH when a significant risk is identified. "
            "Otherwise mark LOW. "

            "Reply with exactly one word: HIGH or LOW."
        ),
    )

    # --------------------------------------------------------
    # AGENT 3: CUSTOMER RESPONSE AGENT
    # --------------------------------------------------------

    customer_response_agent = Agent(
        client=chat_client,
        name="CustomerResponseAgent",
        instructions=(
            "You are an e-commerce customer support specialist. "

            "Generate a polite and professional customer-facing "
            "message based on the final workflow decision. "

            "Respect the exact decision supplied by the workflow. "
            "Never override a manager's rejection. "

            "For approved requests, explain that the return "
            "request has been approved for further processing. "

            "For rejected requests, communicate the rejection "
            "politely and clearly. "

            "Do not claim that a refund has been completed, "
            "payment has been processed, or replacement shipped. "

            "Keep the message concise."
        ),
    )

    # ========================================================
    # 5. EXECUTOR 1: ELIGIBILITY REVIEW
    # ========================================================

    @executor(id="eligibility_review")
    async def eligibility_review(
        request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print(
            "\n[Eligibility Agent] "
            "Reviewing customer return request..."
        )

        result = await eligibility_agent.run(
            "Review this return request:\n"
            + json.dumps(
                request,
                ensure_ascii=False,
            )
        )

        # Apply deterministic Python checks

        issues = check_eligibility(request)

        eligibility_status = (
            "ELIGIBLE"
            if not issues
            else "NOT_ELIGIBLE"
        )

        print(
            f"[Eligibility Agent] "
            f"Status: {eligibility_status}"
        )

        if issues:
            for issue in issues:
                print(f"  - {issue}")

        await ctx.send_message({
            **request,
            "eligibility_status": eligibility_status,
            "eligibility_findings": result.text.strip(),
            "eligibility_issues": issues,
        })

    # ========================================================
    # 6. EXECUTOR 2: RISK REVIEW
    # ========================================================

    @executor(id="risk_review")
    async def risk_review(
        request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print(
            "\n[Risk Agent] "
            "Assessing customer return risk..."
        )

        result = await risk_agent.run(
            "Assess the risk of this return request. "
            "Reply HIGH or LOW only:\n"
            + json.dumps(
                request,
                ensure_ascii=False,
            )
        )

        risk = (
            result.text
            .strip()
            .upper()
            .strip(". ")
        )

        # Fail safely if AI gives an unexpected response

        if risk not in {"HIGH", "LOW"}:
            risk = "HIGH"

        risk_reasons = []

        # Deterministic risk safeguards

        if float(request["amount_inr"]) >= 25000:
            risk_reasons.append(
                "High-value return request."
            )

        if request["previous_returns_90_days"] >= 3:
            risk_reasons.append(
                "Frequent previous returns."
            )

        if not request["invoice_available"]:
            risk_reasons.append(
                "Missing invoice evidence."
            )

        if (
            request["item_condition"].upper() == "DAMAGED"
            and not request["photo_evidence_available"]
        ):
            risk_reasons.append(
                "Missing damage photographs."
            )

        # Python safeguards can increase risk,
        # but cannot lower an AI HIGH assessment.

        if risk_reasons:
            risk = "HIGH"

        if risk == "HIGH" and not risk_reasons:
            risk_reasons.append(
                "Potential risk identified by Risk Agent."
            )

        risk_assessment = (
            "; ".join(risk_reasons)
            if risk_reasons
            else "No significant risk concerns identified."
        )

        print(
            f"[Risk Agent] Risk Level: {risk}"
        )

        print(
            f"[Risk Agent] Assessment: {risk_assessment}"
        )

        await ctx.send_message({
            **request,
            "risk": risk,
            "risk_assessment": risk_assessment,
        })

    # ========================================================
    # 7. EXECUTOR 3: HUMAN APPROVAL GATEWAY
    # ========================================================

    class ApprovalGateway(Executor):

        def __init__(self):
            super().__init__(
                id="approval_gateway"
            )

        @handler
        async def review(
            self,
            request: dict,
            ctx: WorkflowContext[dict],
        ) -> None:

            # Automatic approval requires all conditions
            # to be satisfied and risk must be LOW.

            needs_approval = (
                request["eligibility_status"] != "ELIGIBLE"
                or request["risk"] == "HIGH"
            )

            # AUTOMATIC APPROVAL

            if not needs_approval:

                request["approval_route"] = "Automatic"

                request["decision"] = "AUTO_APPROVED"

                request["decision_by"] = "Automatic Policy"

                print(
                    "\n[Approval Gateway] "
                    "Request automatically approved."
                )

                await ctx.send_message(request)

                return

            # HUMAN-IN-THE-LOOP

            print(
                "\n[Approval Gateway] "
                "PAUSED - Manager approval required."
            )

            prompt = (
                f"Request ID: {request['request_id']}\n"
                f"Order ID: {request['order_id']}\n"
                f"Product: {request['product']}\n"
                f"Amount: Rs. {request['amount_inr']:,}\n"
                f"Requested Action: {request['request_type']}\n"
                f"Eligibility Status: "
                f"{request['eligibility_status']}\n"
                f"Eligibility Issues: "
                f"{request['eligibility_issues']}\n"
                f"Risk Level: {request['risk']}\n"
                f"Risk Assessment: "
                f"{request['risk_assessment']}\n"
                "\nManager decision required."
            )

            # Pause workflow and request human information

            await ctx.request_info(
                request_data=ManagerApprovalRequest(
                    request=request,
                    prompt=prompt,
                ),
                response_type=str,
            )

        # ----------------------------------------------------
        # RESUME WORKFLOW AFTER MANAGER DECISION
        # ----------------------------------------------------

        @response_handler
        async def on_manager_decision(
            self,
            original_request: ManagerApprovalRequest,
            response: str,
            ctx: WorkflowContext[dict],
        ) -> None:

            request = dict(
                original_request.request
            )

            decision = response.strip().lower()

            if decision not in {"approve", "reject"}:
                decision = "reject"

            request["approval_route"] = "Human Review"

            request["decision"] = (
                "MANAGER_APPROVED"
                if decision == "approve"
                else "MANAGER_REJECTED"
            )

            request["decision_by"] = "Human Manager"

            print(
                f"\n[Approval Gateway] "
                f"Final Decision: {request['decision']}"
            )

            # Resume workflow with manager decision

            await ctx.send_message(request)

    # ========================================================
    # 8. EXECUTOR 4: CUSTOMER RESPONSE
    # ========================================================

    @executor(id="customer_response")
    async def customer_response(
        request: dict,
        ctx: WorkflowContext[Never, str],
    ) -> None:

        print(
            "\n[Customer Response Agent] "
            "Preparing customer communication..."
        )

        result = await customer_response_agent.run(
            "Generate a customer response using these details:\n"
            + json.dumps(
                request,
                ensure_ascii=False,
            )
        )

        customer_message = result.text.strip()

        # Build final structured output

        final_output = {
            "request_id": request["request_id"],
            "order_id": request["order_id"],
            "product": request["product"],
            "product_category": request["product_category"],
            "requested_amount": request["amount_inr"],
            "requested_action": request["request_type"],
            "eligibility_status": request["eligibility_status"],
            "eligibility_findings": request["eligibility_findings"],
            "eligibility_issues": request["eligibility_issues"],
            "risk": request["risk"],
            "risk_assessment": request["risk_assessment"],
            "approval_route": request["approval_route"],
            "final_decision": request["decision"],
            "decision_by": request["decision_by"],
            "customer_communication": customer_message,
        }

        print(
            "\n[Customer Response Agent] "
            "Customer message generated."
        )

        await ctx.yield_output(
            json.dumps(
                final_output,
                indent=4,
                ensure_ascii=False,
            )
        )

    # ========================================================
    # 9. CREATE GRAPH WORKFLOW
    # ========================================================

    gateway = ApprovalGateway()

    workflow = (
        WorkflowBuilder(
            start_executor=eligibility_review
        )

        .add_edge(
            eligibility_review,
            risk_review,
        )

        .add_edge(
            risk_review,
            gateway,
        )

        .add_edge(
            gateway,
            customer_response,
        )

        .build()
    )

    return workflow


# ============================================================
# 10. EXECUTE WORKFLOW WITH HUMAN APPROVAL
# ============================================================

async def run_one(
    workflow,
    request: dict,
) -> None:

    responses = None

    first_run = True

    while True:

        # INITIAL EXECUTION

        if first_run:

            stream = workflow.run(
                request,
                stream=True,
            )

            first_run = False

        # RESUMED EXECUTION

        else:

            stream = workflow.run(
                stream=True,
                responses=responses,
            )

        pending = {}

        completed = False

        async for event in stream:

            # Capture human approval request

            if event.type == "request_info":

                pending[event.request_id] = event.data

            # Capture final workflow output

            elif event.type == "output":

                print(
                    "\n" + "=" * 65
                )

                print(
                    "FINAL RETURN PROCESSING RECORD"
                )

                print(
                    "=" * 65
                )

                print(event.data)

                completed = True

        if completed:
            return

        if not pending:

            raise RuntimeError(
                "Workflow stopped without output "
                "or manager approval request."
            )

        responses = {}

        # ASK MANAGER FOR APPROVAL

        for request_id, approval in pending.items():

            print(
                "\n" + "=" * 65
            )

            print(
                "MANAGER APPROVAL REQUIRED"
            )

            print(
                "=" * 65
            )

            print(
                approval.prompt
            )

            print(
                "\nEligibility Findings:"
            )

            print(
                approval.request["eligibility_findings"]
            )

            print(
                "\nRisk Assessment:"
            )

            print(
                approval.request["risk_assessment"]
            )

            # Validate manager input

            while True:

                answer = input(
                    "\nType approve or reject: "
                ).strip().lower()

                if answer in {"approve", "reject"}:
                    break

                print(
                    "Invalid input. "
                    "Please type approve or reject."
                )

            responses[request_id] = answer


# ============================================================
# 11. MAIN APPLICATION
# ============================================================

async def main() -> None:

    print(
        "=" * 65
    )

    print(
        "E-COMMERCE RETURNS & REFUND PROCESSING SYSTEM"
    )

    print(
        "Microsoft Agent Framework + Azure AI Foundry"
    )

    print(
        "=" * 65
    )

    # LOAD AZURE CONFIGURATION

    api_key = read_setting(
        "AZURE_OPENAI_API_KEY"
    )

    base_url = read_setting(
        "AZURE_OPENAI_BASE_URL"
    )

    deployment = read_setting(
        "AZURE_OPENAI_MODEL"
    )

    print(
        "\nAzure AI Foundry configuration loaded."
    )

    print(
        f"Deployment: {deployment}"
    )

    # LOAD CUSTOMER RETURN REQUESTS

    returns_file = BASE_DIR / "returns.json"

    if not returns_file.exists():

        raise FileNotFoundError(
            "returns.json file not found."
        )

    with returns_file.open(
        encoding="utf-8"
    ) as file:

        requests = json.load(file)

    if not isinstance(requests, list):

        raise ValueError(
            "returns.json must contain a JSON list."
        )

    print(
        f"\nTotal return requests loaded: {len(requests)}"
    )

    # CONNECT TO AZURE AI FOUNDRY

    async with AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    ) as client:

        chat_client = OpenAIChatClient(
            model=deployment,
            async_client=client,
        )

        print(
            "\nAzure AI Foundry client initialized."
        )

        # PROCESS EACH RETURN REQUEST

        for request in requests:

            print(
                "\n" + "=" * 65
            )

            print(
                f"Processing Request: {request['request_id']}"
            )

            print(
                f"Order ID: {request['order_id']}"
            )

            print(
                f"Product: {request['product']}"
            )

            print(
                f"Amount: Rs. {request['amount_inr']:,}"
            )

            print(
                f"Request Type: {request['request_type']}"
            )

            print(
                "=" * 65
            )

            # Build a fresh workflow for each request

            workflow = build_workflow(
                chat_client
            )

            # Execute and handle manager approval

            await run_one(
                workflow,
                request,
            )

    print(
        "\n" + "=" * 65
    )

    print(
        "ALL RETURN REQUESTS PROCESSED"
    )

    print(
        "=" * 65
    )


# ============================================================
# 12. APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except (ValueError, FileNotFoundError) as error:

        print(
            f"\nConfiguration / File Error: {error}"
        )

    except KeyError as error:

        print(
            f"\nMissing required data field: {error}"
        )

    except Exception as error:

        print(
            f"\nApplication Error: {error}"
        )
