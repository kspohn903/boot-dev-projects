def count_marketers(job_titles):
    count = 0
    for title in job_titles:
        if title.lower() == "marketer":
           count += 1 
    return count
