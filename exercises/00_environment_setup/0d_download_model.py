#!/usr/bin/env python3
import subprocess
import os
import argparse
import shutil

DEFAULT_MODEL_HF = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
DEFAULT_HF_FILENAME = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
DEFAULT_OUTPUT_FILE = "models/tinyllama.gguf"

def main():
    parser = argparse.ArgumentParser(description="Download TinyLlama GGUF model and save as tinyllama.gguf")
    parser.add_argument("--hf", default=DEFAULT_MODEL_HF, help="Hugging Face model ID")
    parser.add_argument("--hf_filename", default=DEFAULT_HF_FILENAME, help="Filename to download from HF repo")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_FILE, help="Final output path for tinyllama.gguf")
    args = parser.parse_args()

    if os.path.exists(args.out):
        print(f"✅ Model already exists at {args.out}")
        return

    # Temporal folder
    temp_dir = "models/temp_download"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, args.hf_filename)

    print(f"⬇️  Downloading {args.hf_filename} from {args.hf}...")

    # Download
    cmd = [
        "poetry", "run", "python", "scripts/download_model.py",
        "--hf", args.hf,
        "--filename", args.hf_filename,
        "--out", temp_dir
    ]

    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download model: {e}")
        return

    # Move and rename to tinyllama.gguf
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    shutil.move(temp_file_path, args.out)
    print(f"✅ Model saved as {args.out}")

    # Clean temporal folder
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

if __name__ == "__main__":
    main()
