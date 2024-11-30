import concurrent.futures
import time
import os
import logging
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Constants
MAX_RETRIES = 3
WORKER_RETRY_DELAY = 1  # Seconds


def process_task(task_id, data, retry_count=0):
    """
    Process a task with some workload, includes retry logic.

    Parameters:
        task_id (int): A unique identifier for the task.
        data (str): Input data to be processed.
        retry_count (int): The current retry count.

    Returns:
        str: The result of the processing.
    """
    try:
        logger.info(f"Task {task_id} started by Process {os.getpid()}")
        # Simulating workload with potential random failure (e.g., a Web3 transaction might fail)
        if random.choice([True, False]) and retry_count < MAX_RETRIES:
            raise ValueError(f"Simulated error in task {task_id} (retry count: {retry_count})")

        time.sleep(random.uniform(1, 3))  # Simulate variable processing time
        processed_data = data.upper()  # Example of a simple processing step

        logger.info(f"Task {task_id} completed by Process {os.getpid()}")
        return f"Task {task_id}: Processed data: {processed_data}"

    except Exception as e:
        if retry_count < MAX_RETRIES:
            logger.warning(f"Task {task_id} failed with error '{e}', retrying... ({retry_count + 1}/{MAX_RETRIES})")
            time.sleep(WORKER_RETRY_DELAY)
            return process_task(task_id, data, retry_count + 1)
        else:
            logger.error(f"Task {task_id} failed after {MAX_RETRIES} retries")
            return f"Task {task_id}: Failed after {MAX_RETRIES} retries"


def parallel_executor(tasks, max_workers=4):
    """
    Execute multiple tasks in parallel using ThreadPoolExecutor.

    Parameters:
        tasks (list of tuples): A list of tasks, where each task is a tuple containing
                                (task_id, data).
        max_workers (int): The maximum number of workers to run concurrently.

    Returns:
        list: A list of results from the processed tasks.
    """
    results = []

    # Using ThreadPoolExecutor for managing multiple threads.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Mapping tasks to be processed in parallel
        future_to_task = {executor.submit(process_task, task[0], task[1]): task for task in tasks}

        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                logger.error(f"Task {task[0]} generated an unexpected exception: {exc}")

    return results


def main():
    # Sample tasks: List of tuples (task_id, data)
    task_list = [
        (1, "Process privacy contract A"),
        (2, "Handle Web3 transaction X"),
        (3, "Encrypt data block Y"),
        (4, "Verify zero-knowledge proof Z"),
        (5, "Fetch external API data Q"),
        (6, "Optimize computation for blockchain P"),
    ]

    start_time = time.time()

    # Run the tasks in parallel with a pool of 4 workers
    logger.info("Starting task execution...")
    results = parallel_executor(task_list, max_workers=4)

    # Print the results
    for res in results:
        logger.info(res)

    end_time = time.time()
    logger.info(f"Completed all tasks in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
# Parallel execution support for concurrency
