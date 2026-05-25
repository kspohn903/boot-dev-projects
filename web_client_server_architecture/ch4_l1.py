import asyncio

# Set the delays to control the execution order
project_complete_wait = 4  # Prints last (longest delay)
ci_wait = 2                # Prints second
repo_creation_wait = 1     # Prints first (shortest delay)
board_config_wait = 3      # Prints third

# don't touch below this line

async def announce(message, delay):
    await asyncio.sleep(delay)
    print(message)

# 1. Make main() an async function
async def main():
    tasks = [
        announce("Project setup complete!", project_complete_wait),
        announce("Setting up continuous integration...", ci_wait),
        announce("Creating project repository...", repo_creation_wait),
        announce("Configuring project boards...", board_config_wait),
    ]
    print("Starting project initialization...")
    
    # 2. Await the gather call to ensure the tasks run to completion
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # 3. Use asyncio.run() to execute the async main function
    asyncio.run(main())
