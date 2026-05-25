import os
from functions.get_files_info import get_file_content # Updated import

# Helper function to format and print the test results
def run_file_content_test(test_name, working_dir, file_path, check_truncation=False):
    print(f'Running Test: {test_name}')
    print(f'get_file_content("{working_dir}", "{file_path}"):')
    
    result = get_file_content(working_dir, file_path)
    
    if check_truncation:
        expected_trailer = f"[...File \"{file_path}\" truncated at 10000 characters]"
        is_truncated = result.endswith(expected_trailer)
        
        if is_truncated:
            print(f"  Result: Content was correctly truncated.\n  Final length: {len(result)}")
        else:
            print(f"  Result: FAILED to truncate. Final length: {len(result)}")
            
    elif result.startswith("Error:"):
        print(f"  Result: {result}")
        
    else:
        # Print content, but truncate for readability in the test output
        # display_content = result[:200] + '...' if len(result) > 200 else result
        # print(f"  Result (first 200 chars):\n{display_content}\n")
        print(f"  Result: Content read successfully.\n")
        # For the submission, we need to ensure the full content is available to stdout. 
        # Printing the whole 'result' variable (which holds the file content) is the only way.
        print(result)

    print("-" * 20)


if __name__ == "__main__":
    print("Running get_file_content tests:\n")
    
    # 1. Truncation Test
    run_file_content_test("Test 1: Truncation (lorem.txt)", "calculator", "lorem.txt", check_truncation=True)
    
    # 2. Valid File Test (main.py)
    run_file_content_test("Test 2: Valid File (main.py)", "calculator", "main.py")
    
    # 3. Valid File Test (pkg/calculator.py)
    run_file_content_test("Test 3: Valid File (pkg/calculator.py)", "calculator", "pkg/calculator.py")
    
    # 4. Outside Boundary Test (/bin/cat)
    run_file_content_test("Test 4: Boundary Violation", "calculator", "/bin/cat")
    
    # 5. File Not Found Test
    run_file_content_test("Test 5: File Not Found", "calculator", "pkg/does_not_exist.py")
