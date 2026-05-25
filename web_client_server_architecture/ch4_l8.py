from ch4_l5 import update_task_status
import asyncio

async def main():
    # Call the coroutine and await its result, saving the value to 'message' 
    message = await update_task_status(
        task_id= 123, 
        current_status="In Progress", 
        is_completed=True
    )
    # Don't touch below this line

    print(message)

if __name__ == "__main__":
   asyncio.run(main()) 
