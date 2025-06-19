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
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
client = genai.Client(api_key=api_key)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to read, relative to the working directory.",
            ),
        },
    ),
)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists file information if a directory is provided it lists all files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory or file to show file info for, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to write to, relative to the working directory.",
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
    description="Run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the python file to run, relative to the working directory.",
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

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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
