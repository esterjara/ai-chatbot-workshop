r"""Simple helper to download a model file from a direct URL.

Usage:
  python scripts/download_model.py --url <DIRECT_LINK> --out models/my-model.gguf

If you want Hugging Face support, install `huggingface_hub` and pass `--hf <repo_id>`.
"""
import argparse
import os
import sys


def download_url(url: str, out_path: str):
    try:
        import requests
    except Exception:
        print("Please install requests: pip install requests")
        sys.exit(1)
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Downloaded to", out_path)


def download_hf(repo_id: str, out_path: str, token: str | None = None, filename: str | None = None):
    try:
        from huggingface_hub import hf_hub_download
    except Exception:
        print("Install huggingface_hub for HF downloads: pip install huggingface-hub")
        sys.exit(1)
    
    if not filename:
        print(f"Error: Please specify --filename for the model file to download from {repo_id}")
        sys.exit(1)
    
    print(f"Downloading {filename} from {repo_id}...")
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    
    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        token=token,
        local_dir=os.path.dirname(out_path) if os.path.dirname(out_path) else ".",
        local_dir_use_symlinks=False
    )
    
    # Move to desired output path if different
    if downloaded_path != out_path:
        import shutil
        shutil.move(downloaded_path, out_path)
    
    print(f"Downloaded to {out_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", help="Direct download URL for a model file")
    p.add_argument("--out", default="models/model.gguf", help="Output path")
    p.add_argument("--hf", help="Hugging Face repo id (optional)")
    p.add_argument("--filename", help="Filename to download from HF repo")
    p.add_argument("--token", help="HF token if repository is gated")
    args = p.parse_args()

    if args.url:
        download_url(args.url, args.out)
    elif args.hf:
        download_hf(args.hf, args.out, args.token, args.filename)
    else:
        print("Provide --url or --hf. See script help.")


if __name__ == "__main__":
    main()
