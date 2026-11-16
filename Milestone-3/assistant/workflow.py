
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from tools.trip_tools import trip_lookup_tool
from tools.weather_tools import weather_forecast_tool

from assistant.memory import save_message, get_chat_history


# PART 1: Connect to the LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# PART 2: Create the prompt
prompt = ChatPromptTemplate.from_template("""
You are an AI Travel and Weather Advisory Assistant.

Use the trip details and actual weather information
to answer the user's question.

Previous conversation:
{chat_history}

Trip details:
{trip_details}

Weather information:
{weather_details}

Current user question:
{question}

Give a clear answer and provide useful travel suggestions.
Do not invent weather information.
""")


# PART 3: Connect prompt and LLM
advisory_chain = prompt | llm


# PART 4: Generate travel advisory
def generate_travel_advisory(trip_id, session_id, question):

    # Retrieve trip information
    trip = trip_lookup_tool.invoke({
        "trip_id": trip_id
    })

    if "error" in trip:
        return trip["error"]

    # Retrieve actual weather information
    weather = weather_forecast_tool.invoke({
        "destination": trip["destination"],
        "start_date": trip["start_date"],
        "end_date": trip["end_date"]
    })

    if "error" in weather:
        return weather["error"]

    # Retrieve previous conversation from Redis
    history = get_chat_history(session_id)

    chat_history = "\n".join(
        f"{message['role']}: {message['message']}"
        for message in history
    )

    # Send information to the LLM
    response = advisory_chain.invoke({
        "chat_history": chat_history,
        "trip_details": str(trip),
        "weather_details": str(weather),
        "question": question
    })

    answer = response.content

    # Save current question and answer in Redis
    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

    return answer


# PART 5: Test the workflow
if __name__ == "__main__":

    trip_id = 1
    session_id = "jaipur_session"

    question1 = "What is the weather in Jaipur?"

    answer1 = generate_travel_advisory(
        trip_id,
        session_id,
        question1
    )

    print("\nQUESTION 1:", question1)
    print("ANSWER 1:", answer1)


    question2 = "Should I carry an umbrella?"

    answer2 = generate_travel_advisory(
        trip_id,
        session_id,
        question2
    )

    print("\nQUESTION 2:", question2)
    print("ANSWER 2:", answer2)
