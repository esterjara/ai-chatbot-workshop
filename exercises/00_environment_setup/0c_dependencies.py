#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("Installing project dependencies using Poetry...")
    
    try:
        subprocess.check_call(["poetry", "install"])
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
