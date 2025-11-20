"""Simple helper to download a model file from a direct URL.

Usage:
  python scripts\download_model.py --url <DIRECT_LINK> --out models/my-model.gguf

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


def download_hf(repo_id: str, out_path: str, token: str | None = None):
    try:
        from huggingface_hub import snapshot_download
    except Exception:
        print("Install huggingface_hub for HF downloads: pip install huggingface-hub")
        sys.exit(1)
    path = snapshot_download(repo_id, use_auth_token=token)
    print("Downloaded snapshot to", path)
    # The snapshot may contain multiple files; user must pick correct model file.
    print("Please copy the desired model file from the snapshot to:", out_path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", help="Direct download URL for a model file")
    p.add_argument("--out", default="models/model.gguf", help="Output path")
    p.add_argument("--hf", help="Hugging Face repo id (optional)")
    p.add_argument("--token", help="HF token if repository is gated")
    args = p.parse_args()

    if args.url:
        download_url(args.url, args.out)
    elif args.hf:
        download_hf(args.hf, args.out, args.token)
    else:
        print("Provide --url or --hf. See script help.")


if __name__ == "__main__":
    main()
