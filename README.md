# Ubuntu-Inspired Image Fetcher

A Python utility for safely downloading images from the internet into a local directory.  
This program is designed with **security and efficiency precautions** inspired by Ubuntu’s philosophy of safety and reliability.

---

## ✨ Features
- ✅ Download single or multiple images from given URLs  
- ✅ Creates a `Fetched_Images/` directory automatically if it doesn’t exist  
- ✅ Prevents **duplicate downloads** using SHA-256 hashing  
- ✅ Validates `Content-Type` to ensure only real image files are saved  
- ✅ Respects `Content-Length` to prevent downloading oversized files (default: 5 MB limit)  
- ✅ Uses `Content-Disposition` header if available for correct filenames  
- ✅ Sanitizes filenames to prevent path traversal or unsafe characters  
- ✅ Streams large files to avoid memory issues  
- ✅ Handles network errors gracefully with descriptive messages  

---

## ⚙️ Requirements
- Python **3.7+**  
- [`requests`](https://pypi.org/project/requests/) library  

Install dependencies with:
```bash
pip install requests


🚀 Usage

Clone or download this repository.

Run the script:
