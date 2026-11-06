import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from openai import OpenAI
from tools import search_restaurants,calculate_dining_cost
from guardrails import contains_pii,clean_output,validate_input,is_restaurant_related

load_dotenv()


model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "openai/gpt-oss-120b"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


agent=create_agent(
    model=model,
    tools=[search_restaurants,calculate_dining_cost],
    system_prompt=(
        "You are a Workshop AI Assistant."

        ),
    checkpointer = InMemorySaver()
)

if __name__ == "__main__":

    thread_number = 1
    previous_count = 0

    print("Restaurant AI Agent")
    print("Type /new for a new conversation")
    print("Type exit to quit")

    has_history = False

    while True:

        question = input("\nYou: ").strip()

        # Exit the application
        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Start a new conversation
        if question.lower() == "/new":
            has_history = False
            thread_number += 1
            previous_count = 0
            print("New conversation started.")
            continue

        # Input guardrail
        valid, message = validate_input(question)

        if not valid:
            print("Agent:", message)
            continue

        # PII guardrail
        if contains_pii(question):
            print("Agent: PII detected. Please remove personal contact details.")
            continue

        # Domain restriction
        if not is_restaurant_related(question, has_history):
            print("Agent: I can only help with restaurant-related questions.")
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

            # Display tool execution details
            for message in new_messages:

                if isinstance(message, AIMessage):
                    for call in message.tool_calls:
                        print("[TOOL]:", call["name"])
                        print("Arguments:", call["args"])

                if isinstance(message, ToolMessage):
                    print("[TOOL RESULT]:", message.content)

            # Output guardrail
            answer = messages[-1].content
            answer = clean_output(answer)

            print("\nAgent:", answer)

            has_history = True

        except Exception as error:
            print("Error:", error)
