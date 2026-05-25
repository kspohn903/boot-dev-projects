import asyncio
import aiohttp # Replaces pyodide.http
import random

async def get_users(url, api_key):
    # Set headers once
    headers = {
        "X-API-Key": api_key,  # Use the provided API key for authentication
        "Content-Type": "application/json",
    }    
    # 1. Use aiohttp.ClientSession for requests
    async with aiohttp.ClientSession(headers=headers) as session:
        # 2. Perform the GET request using session.get()
        async with session.get(url) as response:
            # 3. Await the response and parse the JSON data
            return await response.json()

# Don't touch below this line

def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

def log_users(users):
    for user in users:
        print(f"User name: {user['user']['name']}, Role: {user['role']}, experience: {user['experience']}, Remote: {user['remote']}")

# New async main function to handle execution
async def main():
    generated_key = generate_key()
    url = "https://api.boot.dev/v1/courses_rest_api/learn-http/users"
    users = await get_users(url, generated_key)
    log_users(users)

# Run the async main function using asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())
