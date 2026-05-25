import asyncio
import aiohttp # Replaces pyodide.http
import random

async def get_user_code(url, api_key):
    headers = {
        "X-API-Key": api_key,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        # Perform the GET request
        async with session.get(url) as response:
            # FIX: Return the status code using the .status property
            return response.status

# Don't touch below this line

def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

# Standard Python async execution block
async def main():
    api_key = generate_key()
    # Test 1: Existing user (should return 200)
    user_url_exists = "https://api.boot.dev/v1/courses_rest_api/learn-http/users/0194fdc2-fa2f-4cc0-81d3-ff12045b73c8"
    status_exists = await get_user_code(user_url_exists, api_key)
    print(f"Status for existing user: {status_exists}")
    # Test 2: Non-existent user (should return 404)
    user_url_non_existent = "https://api.boot.dev/v1/courses_rest_api/learn-http/users/non-existent-id"
    status_not_found = await get_user_code(user_url_non_existent, api_key)
    print(f"Status for non-existent user: {status_not_found}")

if __name__ == "__main__":
    asyncio.run(main())
