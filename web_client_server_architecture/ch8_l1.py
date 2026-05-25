import asyncio
import aiohttp # Replaces pyodide.http
import random
import json


async def get_resources(path):
    """
    Performs a GET request using aiohttp, correctly building the full URL 
    by appending the 'path' to the base URL.
    """
    base_url = "https://api.boot.dev"
    # FIX: Correctly construct the full URL by combining base_url and path
    full_url = f"{base_url}{path}" 

    headers = {
        "X-API-Key": generate_key(),
        "Content-Type": "application/json",
    }

    # Use aiohttp for the GET request
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(full_url) as response:
            return await response.json()


# don't touch below this line


def log_resources(resources):
    for resource in resources:
        print(f" - {json.dumps(resource)}")

def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

# Standard Python async execution block
async def main():
    projects = await get_resources("/v1/courses_rest_api/learn-http/projects")
    print("Projects:")
    log_resources(projects)
    print(" --- ")

    issues = await get_resources("/v1/courses_rest_api/learn-http/issues")
    print("Issues:")
    log_resources(issues)
    print(" --- ")

    users = await get_resources("/v1/courses_rest_api/learn-http/users")
    print("Users:")
    log_resources(users)

if __name__ == "__main__":
    asyncio.run(main())
