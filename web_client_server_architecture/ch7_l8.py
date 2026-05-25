import asyncio
import aiohttp # Replaces pyodide.http
import json
import random

def get_full_url(base_url, transaction_id):
    return f"{base_url}/{transaction_id}"

async def update_user(base_url, transaction_id, data, api_key):
    """
    Performs an asynchronous PUT request to update user data.
    Requires serializing the data dictionary to a JSON string.
    """
    full_url = get_full_url(base_url, transaction_id)

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    
    # 1. Serialize the Python dictionary 'data' into a JSON string
    json_string_body = json.dumps(data)
    
    # 2. Use aiohttp for the PUT request
    async with aiohttp.ClientSession(headers=headers) as session:
        # Pass the JSON string to the 'data' parameter for the request body
        async with session.put(full_url, data=json_string_body) as response:
            # 3. Return the parsed JSON response
            return await response.json()


async def get_user_by_id(base_url, transaction_id, api_key):
    """
    Performs an asynchronous GET request to retrieve user data.
    """
    full_url = get_full_url(base_url, transaction_id)
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    # 1. Use aiohttp for the GET request
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(full_url) as response:
            # 2. Return the parsed JSON response
            return await response.json()

# don't touch below this line

def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result


user_id = "2f8282cb-e2f9-496f-b144-c0aa4ced56db"
generated_key = generate_key()
base_url = "https://api.boot.dev/v1/courses_rest_api/learn-http/users"

def log_user(user):
    print(f"User name: {user['user']['name']}, Role: {user['role']}, experience: {user['experience']}, Remote: {user['remote']}")

# Standard Python async execution block
async def main():
    # Initial GET to retrieve user data
    user_data = await get_user_by_id(base_url, user_id, generated_key)
    
    print("--- Initial User Data ---")
    log_user(user_data)

    print(f"\nUpdating user with id: {user_id}")
    
    # Prepare data for PUT request
    user_data["experience"] = 2
    user_data["role"] = "Junior Developer"
    user_data["remote"] = True
    user_data["user"]["name"] = "Dan"
    
    # PUT request to update user
    updated_user = await update_user(base_url, user_id, user_data, generated_key)
    print("--- Updated User Data ---")
    log_user(updated_user)

if __name__ == "__main__":
    asyncio.run(main())
