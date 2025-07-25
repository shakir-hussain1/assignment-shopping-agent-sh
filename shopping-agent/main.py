from agents import Agent, Runner, function_tool
import requests
from connection import config
import asyncio
import rich

API_URL = "https://hackathon-apis.vercel.app/api/products"

@function_tool
def search_products(
    query: str = "",
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    brand: str = None,
    sort_by: str = None,
    limit: int = 5,
    offset: int = 0
) -> dict:
    """
    Search for products with optional filters.

    Returns a dictionary with product results or an error message.
    """

    params = {
        "q": query,
        "limit": limit,
        "offset": offset
    }

    # Add filters if they are provided
    if category:
        params["category"] = category
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price
    if brand:
        params["brand"] = brand
    if sort_by:
        params["sort_by"] = sort_by

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

agent = Agent(
    name="Shopping Agent",
    instructions="You are a shopping assistant and your task is to search and fetch products as per user query.",
    tools=[search_products]
    )

async def main():
    result = await Runner.run(
        agent,
        input="Search some products in furniture category, wood and revolving chairs ranging from 1 to 5000 US dollars and list them.",
        run_config=config,
        )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
