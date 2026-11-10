import os
from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient

from tools import search_product,calculate_order_total

def create_agent():
    client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "openai/gpt-oss-120b"),
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    #Agent 1: Find workshops
    search_agent=Agent(
        client=client,
        name="SearchAgent",
        instructions=(
        "You are a product serach specialist"
        "Use search_product to find product "
        "matching the user's requested topic. "
        "List the matching product IDs and details. "
        "Do not calculate total order cost."
    ),
    tools=[search_product]

    )
    #Agent 2:Calculate fees
    pricing_agent = Agent(
        client=client,
        name="PricingAgent",
        instructions=(
            "You are a product pricing specialist. "
            "Read the previous search results and user request. "
            "Use calculate_order_total for each matching product "
            "using the requested number of quantity. "
            "Report the verified totals. "
            "Never invent prices."
        ),
        tools=[calculate_order_total]
    )

    #Agent 3:Recommend
    recommendation_agent = Agent(
        client=client,
        name="RecommendationAgent",
        instructions=(
            "You are a product recommendation specialist. "
            "Read the search and pricing results. "
            "Recommend the best matching product "
            "within the user's budget. "
            "Explain your choice briefly. "
            "Use only verified workshop data and totals."
        )
    )
    return search_agent, pricing_agent, recommendation_agent


