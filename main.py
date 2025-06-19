import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if (len(sys.argv) < 2):
	print("Please enter a prompt.")
	exit(1)
client = genai.Client(api_key=api_key)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to read. All paths are relative. You don't need the full path.",
            ),
        },
    ),
)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files and contents of directories.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list. All paths are relative. You don't need the full path.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to write to. All paths are relative. You don't need the full path.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute/Run Python files with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the python file to run. All paths are relative. You don't need the full path. You don't need to know the contents of the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

You MUST use function calls to help users. Do NOT respond with text explanations or offers to help - instead, immediately use the appropriate function call.

Available functions:
- get_file_content: Read file contents
- get_files_info: List files and contents of directories
- write_file: Write or overwrite files
- run_python_file: Execute/run Python files

CRITICAL: When a user asks you to do something, you MUST use a function call. Do not say "I can help you" or ask questions - just call the appropriate function.

Examples:
- "list the contents of pkg directory" → call get_files_info with directory="pkg"
- "run main.py" → call run_python_file with file_path="main.py"
- "read file.txt" → call get_file_content with file_path="file.txt"
- "write Hello to file.txt" → call write_file with file_path="file.txt" and content="Hello"

All paths should be relative.
"""

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

response = client.models.generate_content(
	model='gemini-2.0-flash-lite',
	contents=sys.argv[1],
	config=config
)

if (response.function_calls):
	for function in response.function_calls:
		print(f"Calling function: {function.name}({function.args})")
else:
	print(response.text)

if ('--verbose' in sys.argv):
	print('User prompt: ' + sys.argv[1])
	print('Prompt tokens: ' + str(response.usage_metadata.prompt_token_count))
	print('Response tokens: ' + str(response.usage_metadata.candidates_token_count))
