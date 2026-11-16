
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)



prompt = ChatPromptTemplate.from_template("""
You are an AI-powered business travel assistant.

Your job is to provide travel advice using the
trip details and actual weather information provided.

Trip Details:
{trip_details}

Weather Information:
{weather_details}

Instructions:
1. Mention the destination and travel dates.
2. Summarize the available weather information.
3. Provide 3 to 4 useful packing suggestions.
4. Do not invent weather information.
5. If weather information is unavailable, clearly say so.

Generate a short and simple travel advisory.
""")



advisory_chain = prompt | llm



if __name__ == "__main__":

    result = advisory_chain.invoke({
        "trip_details": """
        Destination: Jaipur
        Start date: 2026-11-20
        End date: 2026-11-23
        Purpose: Client meeting
        """,

        "weather_details": """
        Example weather data:
        Maximum temperature: 30°C
        Minimum temperature: 18°C
        Precipitation: 0 mm
        """
    })

    print("\nTRAVEL ADVISORY")
    print(result.content)
