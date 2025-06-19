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

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Root should be referanced as '.'. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Root should be referanced as '.'. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Root should be referanced as '.'. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Root should be referanced as '.'. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

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

if ('--verbose' in sys.argv):
	print('User prompt: ' + sys.argv[1])
	print('Prompt tokens: ' + str(response.usage_metadata.prompt_token_count))
	print('Response tokens: ' + str(response.usage_metadata.candidates_token_count))
