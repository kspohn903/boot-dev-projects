import asyncio
import random

async def update_task_status(task_id:id, current_status:str, is_completed:bool) -> str:
    # Simulate an unpredictable wait time (around 2 seconds)
    await asyncio.sleep(1 + random.random()) 
    
    # Rule 1: "In Progress" AND completed
    if current_status == "In Progress" and is_completed:
        return f"Task {task_id} has been completed successfully."
        
    # Rule 2: "In Progress" AND NOT completed
    elif current_status == "In Progress" and not is_completed:
        return f"task {task_id} is still in progress and cannot be completed."
        
    # Rule 3: Otherwise (status is not "In Progress" or is_completed is irrelevant)
    else:
        return f"Task {task_id} status updated to {current_status}."

# Example Usage (You'd typically use asyncio.run(main()) to execute this):
async def main():
    # Sanitize .csv, task files for deserialized processes
    # with open(fpath, 'r') as f:
    #      while f.readLines() != -1:
    #         try:
    #            task_thread_data = f.read().split(",")
    #            id,progress_message,is_completed = int(task_thread_data[0]), str(task_thread_data[1]), bool(task_thread_data[2])
    #            print(await update_task_status(id, progress_message, is_completed))
    #         except Error as e:
    #            print(f"[Error has occurred]: {e}"); tb.print_exc();
     task_ids = [42, 99, 101]
     task_threads_progress = ["In Progress", "In Progress", "Blocked"]
     tasks_completed = [True, False, True]
     for i in range(len(task_ids)):
         print(await update_task_status(task_ids[i], task_threads_progress[i],                                                      tasks_completed[i]) )

if __name__ == "__main__":
   asyncio.run(main())
