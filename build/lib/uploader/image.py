import os
import requests
import uuid  # For generating unique file names
from typing import List

class ImageUploader:
    
    @staticmethod
    def upload(links: list, path: str = None) -> List[str]:
        """
        Downloads images from the provided links and saves them to the specified path.
        
        Args:
            links (list): A list of image URLs to download.
            path (str): The directory where the images will be saved. Defaults to the `IMAGE_UPLOAD_PATH` environment variable.
        
        Returns:
            list[str]
        """
        upload_root = os.getenv("PROJECT_DIR")
        
        if not upload_root:
            raise ValueError("Upload root is not specified.")
        
        if not path:
            path = os.getenv("IMGAE_UPLOAD_PATH")
        
        if not path:
            raise ValueError("Upload path is not specified.")
        
        if not os.path.exists(path):
            os.makedirs(path)  # Create the directory if it doesn't exist
            
        images = []    
        
        for  link in links:
            try:
                # Get the image data
                response = requests.get(link, stream=True)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                # Determine file name and full path
                unique_name = f"{uuid.uuid4().hex}.jpg"
                file_path = os.path.join(upload_root, path, unique_name)
                
                # Write the image data to a file
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                images.append(unique_name)
                print(f"Downloaded: {unique_name}")
            except Exception as e:
                print(f"Failed to download {link}: {e}")
        return images        

# Example usage:
if __name__ == "__main__":
    os.environ["IMAGE_UPLOAD_PATH"] = "./downloads"  # Set a default path
    image_links = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
    ImageUploader.upload(image_links)
