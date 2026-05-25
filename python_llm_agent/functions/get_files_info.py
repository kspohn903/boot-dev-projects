import os
from config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    """
    Reads the content of a file within the permitted working directory,
    truncating the content if it exceeds MAX_FILE_CHARS.
    
    :param working_directory: The base directory path for access control.
    :param file_path: The path to the file, relative to working_directory.
    :return: The file content as a string, or an error string.
    """
    try:
        # 1. Path Construction and Security Guardrail
        abs_working_directory = os.path.abspath(working_directory)
        
        # Join the paths and normalize (resolving '..', '.', etc.)
        target_path = os.path.join(abs_working_directory, file_path)
        abs_target_path = os.path.abspath(target_path)

        # Check if target_path is outside the working_directory
        if not abs_target_path.startswith(abs_working_directory):
           return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 2. Check if the target path is a regular file
        if not os.path.isfile(abs_target_path):
           return f'Error: File not found or is not a regular file: "{file_path}"'
        # 3. Read and Truncate Content
        with open(abs_target_path, 'r', encoding='utf-8') as f:
           content = f.read(MAX_FILE_CHARS + 1) 
           # Read up to limit + 1 to check for truncation

        # 4. Truncation Logic
        if len(content) > MAX_FILE_CHARS:
           content = content[:MAX_FILE_CHARS]
           return f"{content}[...File \"{file_path}\" truncated at {MAX_FILE_CHARS} characters]"
        else:
           return content
    except UnicodeDecodeError:
        return f"Error: Could not decode file contents: {file_path}. Is it a binary file?"
    except Exception as e:
        # Catch any other unexpected OS errors
        return f"Error: An unexpected error occurred while reading the file: {e}"
