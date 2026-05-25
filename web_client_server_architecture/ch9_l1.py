import asyncio
import aiohttp # Replaces pyfetch
import json
import random

# --- Function converted to use aiohttp ---
async def update_project_by_id(id, project_obj):
    path = f"https://api.boot.dev/v1/courses_rest_api/learn-http/projects/{id}"
    headers = get_headers()
    
    # 1. Serialize the dictionary to a JSON string
    json_string_body = json.dumps(project_obj)
    
    # 2. Use aiohttp ClientSession
    async with aiohttp.ClientSession(headers=headers) as session:
        # 3. Use session.put(), passing the JSON string to the 'data' parameter
        async with session.put(path, data=json_string_body) as response:
            return await response.json()

# Don't touch below this line
def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

api_key = generate_key()
project_id = "0194fdc2-fa2f-4cc0-81d3-ff12045b73c8"

# --- Function converted to use aiohttp ---
async def get_project_by_id(id):
    path = f"https://api.boot.dev/v1/courses_rest_api/learn-http/projects/{id}"
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(path) as response:
            return await response.json()


def get_headers():
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

# --- Standard Python async execution block ---
async def main():
    project = await get_project_by_id(project_id)
    print(f"Project '{project['title']}' fetched. Data: {json.dumps(project)}")

    project["completed"] = True
    await update_project_by_id(project_id, project)
    print(f"Project '{project['title']}' was completed!")

    updated_project = await get_project_by_id(project_id)
    print(
        f"Project '{updated_project['title']}' fetched. Data: {json.dumps(updated_project)}"
    )

if __name__ == "__main__":
    # Runs the async main function
    asyncio.run(main())
