import subprocess

command = "your_command_here"

# Execute the command and pass "y\n" as input to stdin
result = subprocess.run(command, input="y\n", text=True, capture_output=True)

# Print the output and return code
print(result.stdout)
print(result.returncode)
