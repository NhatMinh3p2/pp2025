import os
import subprocess

while True:
    try:
        command = input("shell> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break

    if command.lower() in ['exit', 'quit', 'bye']:
        print("Goodbye!")
        break

    if command == "":
        continue


    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr, end="")


        if not result.stdout and not result.stderr:
            pass

    except Exception as e:
        print(f"Error executing command: {e}")