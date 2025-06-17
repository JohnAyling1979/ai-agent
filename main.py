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

response = client.models.generate_content(
	model='gemini-2.0-flash-lite',
	contents=sys.argv[1],
	config=types.GenerateContentConfig(system_instruction=system_prompt)
)

print(response.text)
if ('--verbose' in sys.argv):
	print('User prompt: ' + sys.argv[1])
	print('Prompt tokens: ' + str(response.usage_metadata.prompt_token_count))
	print('Response tokens: ' + str(response.usage_metadata.candidates_token_count))
