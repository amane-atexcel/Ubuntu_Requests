import os
import requests
import uuid
import hashlib
from urllib.parse import urlparse

# Allowed MIME types
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def sanitize_filename(filename: str) -> str:
    return "".join(c for c in filename if c.isalnum() or c in (".", "_", "-")).strip()

def file_already_exists(save_dir, content_bytes):
    """Check if an image with the same hash already exists in the directory."""
    file_hash = hashlib.sha256(content_bytes).hexdigest()
    for existing_file in os.listdir(save_dir):
        existing_path = os.path.join(save_dir, existing_file)
        if os.path.isfile(existing_path):
            with open(existing_path, "rb") as f:
                existing_hash = hashlib.sha256(f.read()).hexdigest()
                if file_hash == existing_hash:
                    return True
    return False

def fetch_images():
    urls_input = input("Enter image URLs (separated by space or comma): ").strip()
    urls = [u.strip() for u in urls_input.replace(",", " ").split() if u.strip()]

    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    for url in urls:
        try:
            print(f"🔄 Checking: {url}")
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # --- Check important headers ---
            headers = response.headers
            content_type = headers.get("Content-Type", "").lower()
            if content_type not in ALLOWED_CONTENT_TYPES:
                print(f"❌ Skipped (invalid content type: {content_type})")
                continue

            content_length = headers.get("Content-Length")
            if content_length and int(content_length) > MAX_FILE_SIZE:
                print(f"❌ Skipped (file too large: {int(content_length)} bytes)")
                continue

            # --- Choose filename ---
            # Prefer server-provided filename
            if "Content-Disposition" in headers and "filename=" in headers["Content-Disposition"]:
                filename = headers["Content-Disposition"].split("filename=")[-1].strip('"')
            else:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)

            if not filename or "." not in filename:
                filename = f"image_{uuid.uuid4().hex}.jpg"

            filename = sanitize_filename(filename)
            save_path = os.path.join(save_dir, filename)

            # --- Read file into memory first (for hash check) ---
            content = response.content

            # Prevent duplicates by hash
            if file_already_exists(save_dir, content):
                print(f"⚠️ Duplicate detected, skipping {url}")
                continue

            # --- Save file ---
            with open(save_path, "wb") as f:
                f.write(content)

            print(f"✅ Saved: {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error for {url}: {e}")

if __name__ == "__main__":
    fetch_images()
