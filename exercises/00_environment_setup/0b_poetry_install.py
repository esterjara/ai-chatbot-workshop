#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("Checking Poetry installation...")
    try:
        result = subprocess.run(["poetry", "--version"], capture_output=True, text=True)
        print(f"Detected: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Poetry is not installed. Install it from https://python-poetry.org/docs/#installation")
        sys.exit(1)

    print("✅ Poetry is installed.")
    
    # Check virtual environment
    print("Checking if Poetry virtual environment exists...")
    result = subprocess.run(["poetry", "env", "info"], capture_output=True, text=True)
    if "No virtual environment has been created" in result.stdout:
        print("❌ No Poetry virtual environment found. Run `poetry install` to create it.")
    else:
        print("✅ Poetry virtual environment exists.")
    
if __name__ == "__main__":
    main()
