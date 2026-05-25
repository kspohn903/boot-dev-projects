import asyncio
import aiohttp # Replaces pyodide.http
import random

async def fetch_tasks(base_url, availability, api_key):
    # Determine the limit based on availability
    availability_dictionary = {
    "Low": 1,
    "Medium": 3,
    "High": 5
    }
    if(availability) in availability_dictionary:
      limit = availability_dictionary[availability]
    else:
        # Default limit if availability is unrecognized
        limit = 1 
        
    # Define the query parameters: sort is constant, limit is dynamic
    params = {
        "sort": "estimate",
        "limit": limit
    }

    # Pass base_url and the query parameters to get_issues
    return await get_issues(base_url, api_key, params)


# don't touch below this line

def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

# --- Adapted to aiohttp ---
async def get_issues(url, api_key, params=None):
    headers = {
        "X-API-Key": api_key,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        # aiohttp handles assembling the URL and query parameters using the 'params' argument
        async with session.get(url, params=params) as response:
            return await response.json()

# Standard Python async execution block
async def main():
    url = "https://api.boot.dev/v1/courses_rest_api/learn-http/issues"
    apiKey = generate_key()

    lowIssues = await fetch_tasks(url, "Low", apiKey)
    print("Getting issues for low availability user...")
    for issue in lowIssues:
        print(f"Issue: {issue['title']} - estimate: {issue['estimate']}")
    print("---")

    mediumIssues = await fetch_tasks(url, "Medium", apiKey)
    print("Getting issues for medium availability user...")
    for issue in mediumIssues:
        print(f"Issue: {issue['title']} - estimate: {issue['estimate']}")
    print("---")

    print("Getting issues for high availability user...")
    highIssues = await fetch_tasks(url, "High", apiKey)
    for issue in highIssues:
        print(f"Issue: {issue['title']} - estimate: {issue['estimate']}")
    
if __name__ == "__main__":
    asyncio.run(main())
