#!/usr/bin/env python3
import sys

MIN_PYTHON = (3, 9)

def main():
    print("Checking Python version...")
    current = sys.version_info
    print(f"Detected Python version: {current.major}.{current.minor}.{current.micro}")

    if current < MIN_PYTHON:
        print(f"❌ Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or higher is required.")
        sys.exit(1)
    else:
        print("✅ Python version is sufficient.")

if __name__ == "__main__":
    main()