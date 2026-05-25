import csv

def write_csv_report(page_data, filename="report.csv"):
    """
    Exports crawler page data from a dictionary into a CSV file.

    :param page_data: A dictionary where keys are URLs and values are 
                      dictionaries containing page details (h1, links, etc.).
    :param filename: The name of the CSV file to create.
    """
    # Define the column headers (fieldnames) for the CSV file
    fieldnames = [
        "page_url", 
        "h1", 
        "first_paragraph", 
        "outgoing_link_urls", 
        "image_urls"
    ]
    
    # Open the file for writing. 'newline=""' is critical for CSV files 
    # on all operating systems to prevent extra blank rows.
    # 'encoding="utf-8"' ensures proper character handling.
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        # Create a DictWriter instance
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the column headers to the first row
        writer.writeheader()
        
        # Iterate over the page data values (the dictionaries containing the extracted details)
        for page in page_data.values():
            # Create a new dictionary for the CSV row to prepare the data.
            # We copy the dictionary to avoid modifying the original 'page' object.
            row = page.copy()
            
            # --- Data Preparation ---
            # The 'page_url' column is already correct from the 'url' field.
            # The assignment asks for the column name to be 'page_url', but the 
            # dictionary key is likely 'url'. We rename it here for consistency 
            # with the fieldnames list, and assume 'url' is the key in the input.
            if 'url' in row:
                row["page_url"] = row.pop("url")
            
            # Join the list values with a semicolon (;) for the CSV cell
            if "outgoing_links" in row and isinstance(row["outgoing_links"], list):
                row["outgoing_link_urls"] = ";".join(row["outgoing_links"])
                # Remove the original list field if it clashes with the fieldnames, 
                # though DictWriter should handle this as long as the key is not in fieldnames.
                row.pop("outgoing_links", None)
            
            if "image_urls" in row and isinstance(row["image_urls"], list):
                row["image_urls"] = ";".join(row["image_urls"])
            
            # Write the prepared row to the CSV file. DictWriter only writes 
            # fields that match the defined 'fieldnames'.
            writer.writerow(row)

# --- Example Usage (Optional Test) ---

# Example data structure expected from the prompt
page_data_example = {
    "blog.boot.dev": {
        "url": "https://blog.boot.dev",
        "h1": "Learn Backend Development",
        "first_paragraph": "Boot.dev teaches backend development...",
        "outgoing_links": ["https://boot.dev/courses", "https://boot.dev/about"],
        "image_urls": ["https://blog.boot.dev/logo.png"]
    },
    "boot.dev/courses": {
        "url": "https://boot.dev/courses",
        "h1": "Backend Courses",
        "first_paragraph": "Learn Go, Python, and Rust.",
        "outgoing_links": ["https://boot.dev/login"],
        "image_urls": []
    }
}

# write_csv_report(page_data_example, "test_report.csv")
# print("Test report created as 'test_report.csv'")
