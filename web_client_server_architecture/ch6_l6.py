import json

def parse_project(project_string):
    try:
        # Attempt to parse the JSON string into a Python dictionary
        parsed_project = json.loads(project_string)
        # If successful, print the project object details
        print_project_obj(parsed_project)
    except json.JSONDecodeError:
        # If a parsing error occurs (e.g., due to invalid syntax), 
        # print the error message
        print("invalid json string")

# don't touch below this line

def print_project_obj(parsed):
    for key, value in parsed.items():
        print(f"{key}: {value}")

parse_project("""
{
  "completed": false,
  "id": "0194fdc2-fa2f-4cc0-81d3-ff12045b73c8",
  "title": "Unfidget the widget",
  "assignees": 14
}
""")
print("---")

parse_project("""
{
  "completed":true,
  "id":"2f8282cb-e2f9-496f-b144-c0aa4ced56db",
  "title":"Re-spaghettify the codebase - things broke",
  "assignees": 2
}
""")
print("---")

parse_project("""
{
  "completed": false,
  "id":"0f12951e-0a74-4846-a1e0-10b33b13112f"
  "title":"Report quarterly earnings",
  "assignees": 1
}
""")
