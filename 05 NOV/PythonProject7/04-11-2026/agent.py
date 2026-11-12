
import json
import os

from openai import OpenAI
from dotenv import load_dotenv

from tools import search_books, reserve_book

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Search books by title, author or category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Book title, author or category"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": "Reserve an available book for a customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "ID of the book"
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Customer name"
                    }
                },
                "required": ["book_id", "customer_name"]
            }
        }
    }
]


def run_agent(user_message):

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Library Assistant. "
                "Help users search and reserve books. "
                "For reservations, first identify the correct book ID. "
                "Never invent book IDs. "
                "Only confirm a reservation if the tool reports success."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:

        messages.append(response_message)

        for tool_call in response_message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("\nSelected Tool:", function_name)

            if function_name == "search_books":
                result = search_books(**arguments)

            elif function_name == "reserve_book":
                result = reserve_book(**arguments)

            else:
                result = {"error": "Unknown tool"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        return final_response.choices[0].message.content

    return response_message.content


if __name__ == "__main__":

    print("Welcome to AI Library Assistant!")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        try:
            answer = run_agent(user_input)
            print("\nAI:", answer)

        except Exception as error:
            print("\nError:", error)
