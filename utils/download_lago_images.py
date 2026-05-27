import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from google_images_download import google_images_download
except ImportError:
    print("Installing required package: google_images_download...")
    install_package("google_images_download")
    from google_images_download import google_images_download

def download_lake_images():
    """Download 50 lake images from Google Images."""
    # Configuration - modify these values as needed
    KEYWORDS = "rio"           # Search term
    LIMIT = 50                  # Number of images to download
    IMAGE_FORMAT = "jpg"        # Can be "jpg", "png", "gif", "bmp", etc.
    IMAGE_SIZE = "medium"       # Can be "icon", "medium", "large", "xlarge", "xxlarge"

    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": KEYWORDS,
        "limit": LIMIT,
        "print_urls": True,
        "size": IMAGE_SIZE,
        "format": IMAGE_FORMAT,
        "output_directory": os.getcwd(),  # Current working directory
        "image_directory": ""             # Save directly in output_directory (no subfolder)
    }
    try:
        print(f"Starting download of {LIMIT} {KEYWORDS} images in {IMAGE_FORMAT.upper()} format...")
        paths = response.download(arguments)
        print(f"Download completed! Images saved to: {paths}")
        # If paths is a dict, extract the directory
        if isinstance(paths, dict) and paths:
            for key, value in paths.items():
                if value:
                    print(f"Images saved in: {value}")
    except Exception as e:
        print(f"An error occurred during download: {e}")
        print("Try checking your internet connection or reducing the number of images.")

if __name__ == "__main__":
    download_lake_images()