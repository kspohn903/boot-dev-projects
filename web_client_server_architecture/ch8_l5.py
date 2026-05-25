import asyncio
import aiohttp # Replaces pyodide.http
import random

async def get_users(url, api_key):
    # FIX: Append the query parameter ?sort=experience to the URL
    full_url = f"{url}?sort=experience"
    
    headers = {
        "X-API-Key": api_key,
    }

    # Use aiohttp for the GET request
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(full_url) as response:
            return await response.json()

# Don't touch below this line
def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

base_url = "https://api.boot.dev/v1/courses_rest_api/learn-http/users"

api_key = generate_key()

# Standard Python async execution block
async def main():
    users = await get_users(base_url, api_key)
    for user in users:
        print(f"got user with name: {user['user']['name']}, and experience: {user['experience']}")

if __name__ == "__main__":
    asyncio.run(main())
