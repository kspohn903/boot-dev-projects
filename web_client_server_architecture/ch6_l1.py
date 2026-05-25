import asyncio # Needed to run the async logic
import aiohttp # Replaces pyfetch for native Python async HTTP
import random

async def get_projects():
    api_key = generate_key()
    url = "https://api.boot.dev/v1/courses_rest_api/learn-http/projects"    
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    # Use aiohttp.ClientSession for requests
    async with aiohttp.ClientSession(headers=headers) as session:
        # Replace await pyfetch(...) with await session.get(...)
        async with session.get(url) as response:
            # Await the asynchronous .json() method and return it
            return await response.json()

# Don't touch below this line
def generate_key():
    characters = "ABCDEF0123456789"
    result = ""
    n_chars = len(characters)
    for _ in range(n_chars):
        result += characters[random.randint(0, n_chars - 1)]
    return result

# New async main function to handle execution
async def main():
    projects = await get_projects()
    print("Got some projects from the server.")
    for project in projects:
        print(f"- title: {project['title']}, assignees: {project['assignees']}")

# Run the async main function
if __name__ == "__main__":
   asyncio.run(main())
