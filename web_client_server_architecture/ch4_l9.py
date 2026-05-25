import aiohttp
import asyncio

# The original async function logic, adapted for aiohttp
async def get_issue_data():
    url = "https://api.boot.dev/v1/courses_rest_api/learn-http/issues"
    headers = {"X-API-Key": "Testing", "Content-Type": "application/json"} 
    # 1. Create an asynchronous ClientSession
    async with aiohttp.ClientSession(headers=headers) as session:
        # 2. Perform the GET request within the session
        async with session.get(url) as response:
            # 3. Check for successful status (Optional but good practice)
            if response.status == 200:
               # 4. Await the JSON data
               data = await response.json()
               return data
            else:
               response.raise_for_status() 
               # Raise an exception for HTTP errors

# Standard way to run the async function outside of a Pyodide/Jupyter environment
# async def main():
#     issues = await get_issue_data()
#     # ... do something with issues ...
# 
# if __name__ == "__main__":
#     asyncio.run(main())
