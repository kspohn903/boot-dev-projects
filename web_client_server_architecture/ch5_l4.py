import asyncio
import aiohttp # Replaces pyodide.http
import json
import random

# --- The main logic function ---
async def update_user():
    generated_api_key = generate_key()
    url = "https://api.boot.dev/v1/courses_rest_api/learn-http/projects/52fdfc07-2182-454f-963f-5f0f9a621d72"
    new_project_data = {
        "completed": False,
        "id": "52fdfc07-2182-454f-963f-5f0f9a621d72",
        "title": "Product Roadmap 2025",
        "assignees": 1,
    }

    # 1. Get initial project (Uses: generated_api_key)
    old_project = await get_project_response(generated_api_key, url)
    print("Got old project:")
    print(f"- title: {old_project['title']}, assignees: {old_project['assignees']}")
    print("---")

    # 2. Update project (Uses: new_generated_api_key for the write operation)
    new_generated_api_key = generate_key() 
    await put_project(new_generated_api_key, url, new_project_data)
    print("Project updated!")
    print("---")

    # 3. Get updated project (FIX: Uses new_generated_api_key to retrieve the updated data)
    new_project = await get_project_response(new_generated_api_key, url)
    print("Got new project:")
    print(f"- title: {new_project['title']}, assignees: {new_project['assignees']}")
    print("---")

# --- Conversion to aiohttp (replaces pyfetch) ---

async def get_project_response(api_key, url):
    """Performs an asynchronous GET request using aiohttp."""
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    # Use ClientSession for asynchronous HTTP requests
    async with aiohttp.ClientSession(headers=headers) as session:
        # Perform the GET request
        async with session.get(url) as response:
            return await response.json()

async def put_project(api_key, url, data):
    """Performs an asynchronous PUT request using aiohttp."""
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    # Use ClientSession for asynchronous HTTP requests
    async with aiohttp.ClientSession(headers=headers) as session:
        # Perform the PUT request, passing the JSON body as a string
        async with session.put(url, data=json.dumps(data)) as response:
            return await response.json()

# --- Don't touch below this line (Standard utility functions) ---

def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

# Standard Python execution block for running the top-level async function
if __name__ == "__main__":
    asyncio.run(update_user())
