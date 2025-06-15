import os
import subprocess

def get_file_content(working_directory, file_path):
	abs_working_directory, abs_file_path = get_abs(working_directory, file_path)

	if (abs_working_directory not in abs_file_path):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

	if (not os.path.isfile(abs_file_path)):
		return f'Error: File not found or is not a regular file: "{file_path}"'

	MAX_CHARS = 10000

	with open(abs_file_path, 'r') as f:
		contents = f.read(MAX_CHARS)
		if (os.path.getsize(abs_file_path) > MAX_CHARS):
			contents += '\n...File "{file_path}" truncated at 10000 characters'

		return contents

def get_files_info(working_directory, directory=None):
	abs_working_directory, abs_directory = get_abs(working_directory, directory)

	if (abs_working_directory not in abs_directory):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	if (not os.path.isdir(abs_directory)):
		return f'Error: "{directory}" is not a directory'

	files = []
	for file in os.listdir(abs_directory):
		abs_file = abs_directory + '/' + file
		files.append(f'- {file}: file_size={os.path.getsize(abs_file)}, is_dir={os.path.isdir(abs_file)}')


	return '\n'.join(files)

def write_file(working_directory, file_path, content):
	abs_working_directory, abs_file_path = get_abs(working_directory, file_path)

	if (abs_working_directory not in abs_file_path):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

	if (not os.path.exists(os.path.dirname(abs_file_path))):
		os.makedirs(abs_file_path)

	with open(abs_file_path, "w") as f:
		f.write(content)

		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path):
	abs_working_directory, abs_file_path = get_abs(working_directory, file_path)

	if (abs_working_directory not in abs_file_path):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	if (not os.path.isfile(abs_file_path)):
		return f'Error: File "{file_path}" not found.'

	if (not abs_file_path.endswith('.py')):
		return f'Error: "{file_path}" is not a Python file.'

	try:
		result = subprocess.run(['python3', abs_file_path],timeout=30, capture_output=True, cwd=abs_working_directory)

		lines = [
			f'STDOUT: {result.stdout}',
			f'STDERR: {result.stderr}',
		]

		if (result.returncode != 0):
			lines.append(f'Process exited with code {result.returncode}')
		return '\n'.join(lines)
	except:
		return f"Error: executing Python file: {e}"


def get_abs(working_directory, path):
	if (path.startswith('/')):
		combined_path = path
	else:
		combined_path = working_directory + '/' + path

	abs_working_directory = os.path.abspath(working_directory)
	abs_path = os.path.abspath(combined_path)

	return abs_working_directory, abs_path
