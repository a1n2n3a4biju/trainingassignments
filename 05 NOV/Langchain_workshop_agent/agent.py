
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
#
# from guardrails import contains_pii,clean_output

from tools import search_workshops, calculate_workshop_fee


# STEP 1: Load environment
load_dotenv()

# STEP 2: Create model
model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)

# STEP 3: Create agent
# STEP 3: Create agent
agent = create_agent(
    model=model,
    tools=[search_workshops, calculate_workshop_fee],
    system_prompt=(
        "You are a Workshop AI Assistant. "
"Help users search for workshops and calculate workshop fees. "
    "When calculating fees, ask for the workshop ID and number of participants. "
    "Ask whether the user has a coupon code. "
    "If the user provides a coupon code, pass it to calculate_workshop_fee. "
    "If no coupon is provided, calculate the normal fee. "
    "Always explain the original fee, discount amount and final fee."

    ),
    checkpointer=InMemorySaver()
)

# STEP 4: Run application
if __name__ == "__main__":

    thread_number = 1
    previous_count = 0

    print("LangChain Workshop AI Agent")
    print("Type /new for a new conversation")
    print("Type exit to quit")

    while True:
        question = input("\nYou: ").strip()

        # if contains_pii(question):
        #     print ("PII detected. Please remove personal contact details.")
        #     break

        if question.lower() == "exit":
            break

        if question.lower() == "/new":
            thread_number += 1
            previous_count = 0
            print("New conversation started.")
            continue

        if not question:
            continue

        config = {
            "configurable": {
                "thread_id": f"workshop-{thread_number}"
            }
        }

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                },
                config=config
            )

            messages = result["messages"]
            new_messages = messages[previous_count:]
            previous_count = len(messages)

            for message in new_messages:

                if isinstance(message, AIMessage):
                    for call in message.tool_calls:
                        print("[TOOL]:", call["name"])
                        print("Arguments:", call["args"])

                if isinstance(message, ToolMessage):
                    print("[TOOL RESULT]:", message.content)

            print("\nAgent:", messages[-1].content)
            #input guardrail
            #output guardrail
            #system guardrail
            #tool guardrail
            #pii guardrail
        except Exception as error:
            print("Error:", error)
