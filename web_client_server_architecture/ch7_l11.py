import asyncio
import aiohttp # Replaces pyodide.http
import random

# --- Function to be completed (using aiohttp) ---
def get_full_url(base_url, transaction_id):
    return f"{base_url}/{transaction_id}"

async def delete_user(base_url, transaction_id, api_key):
    """Sends a DELETE request to delete a specific user resource."""
    full_url = get_full_url(base_url, transaction_id)
    
    headers = {
        "X-API-Key": api_key, # Required for authentication
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # Use session.delete() for the DELETE method
        async with session.delete(full_url) as response:
            # DELETE often returns an empty body or a simple status, 
            # but we return the status code for confirmation.
            return response.status 

# don't touch below this line
def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

user_id = "0194fdc2-fa2f-4cc0-81d3-ff12045b73c8"
generated_key = generate_key()
url = "https://api.boot.dev/v1/courses_rest_api/learn-http/users"

# --- Adapted to aiohttp ---
async def get_users(url, api_key):
    headers = {
        "X-API-Key": api_key,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.json()

def log_users(users):
    print("Logging user records:")
    for user in users:
        print(f"User name: {user['user']['name']}, Role: {user['role']}, experience: {user['experience']}, Remote: {user['remote']}")

# Standard Python async execution block
async def main():
    users = await get_users(url, generated_key)
    log_users(users)
    print("---")

    await delete_user(url, user_id, generated_key)
    print(f"Deleted user with id: {user_id}")
    print("---")

    new_users = await get_users(url, generated_key)
    log_users(new_users)
    print("---")

if __name__ == "__main__":
    asyncio.run(main())
