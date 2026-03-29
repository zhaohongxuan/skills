#!/usr/bin/env python3
"""
Upload image to GitHub Picgo repository
Usage: python3 upload_pic.py <image_path>
Returns: markdown_image_link\nraw_link\nfilename
"""

import sys
import os
import subprocess
import shutil
from datetime import datetime

def upload_to_github(image_path):
    """Upload image to Picgo repo and return links"""
    
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    
    # Generate timestamp filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        ext = '.png'  # default to png
    
    filename = f"{timestamp}{ext}"
    
    # Get repo path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    repo_path = os.path.join(skill_dir, "picgo-temp")
    
    # Clone picgo repo if not exists
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        subprocess.run(
            ["git", "clone", "https://github.com/zhaohongxuan/picgo.git", repo_path],
            cwd=skill_dir,
            capture_output=True
        )
    
    # Ensure images directory exists
    images_dir = os.path.join(repo_path, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Copy image to repo/images/
    dest_path = os.path.join(images_dir, filename)
    shutil.copy2(image_path, dest_path)
    
    # Commit and push
    subprocess.run(["git", "add", f"images/{filename}"], cwd=repo_path, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"feat: upload {filename}"],
        cwd=repo_path,
        capture_output=True
    )
    subprocess.run(
        ["git", "push", "origin", "master"],
        cwd=repo_path,
        capture_output=True
    )
    
    # Generate links - use master branch and images/ directory
    owner = "zhaohongxuan"
    repo = "picgo"
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/images/{filename}"
    markdown_link = f"![{filename}]({raw_url})"
    
    # Output result
    print(markdown_link)
    print(raw_url)
    print(filename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upload_pic.py <image_path>", file=sys.stderr)
        sys.exit(1)
    
    upload_to_github(sys.argv[1])
