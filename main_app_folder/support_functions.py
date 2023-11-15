from PIL import Image
import os


class SupportMainApp():
    """
    This class hods supports functions for the main app
    """

    def get_first_png_image_in_folder(folder_path: str):
        # Get a list of all files in the folder
        files = os.listdir(folder_path)

        # Filter only image files (you can customize this condition)
        image_files = [file for file in files if file.lower().endswith(('.png'))]

        if not image_files:
            print("No image files found in the folder.")
            return None

        # Get the first image file
        first_image_path = os.path.join(folder_path, image_files[0])

        # Open the image using Pillow
        image = Image.open(first_image_path)

        return image
    

    def remove_png_files(folder_path):
        # Get a list of all files in the folder
        files = os.listdir(folder_path)

        # Filter only PNG files
        png_files = [file for file in files if file.lower().endswith('.png')]

        # Remove each PNG file
        for png_file in png_files:
            file_path = os.path.join(folder_path, png_file)
            os.remove(file_path)
            print(f"Removed: {file_path}")

