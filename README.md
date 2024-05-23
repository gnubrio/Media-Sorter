Image Sorter

The Image Sorter is a Python application built using the Tkinter library, designed to help users organize their image and video files into designated folders. It allows users to load images and videos from a selected directory, display them one by one, and move them to predefined destination folders.
Features:

    Load Images: Users can select a folder containing image and video files to load into the application.

    Display Media: Loaded media files are displayed one by one in the application window, allowing users to view and manage them.

    Move Media: Users can move displayed media files to predefined destination folders by clicking on corresponding directory buttons.

    Add Destination Folders: Users can add destination folders where they want to move the media files.

    Clear Directories: Users can clear all added destination folders from the application.

The application supports the following file formats:

    Images: .jpg, .jpeg, .png, .bmp, .svg, .heic
    Videos: .mp4, .mov

How to Use:

    Load Images:
        Click the "Load Images" button.
        Select the folder containing the images and videos you want to organize.

    View and Manage Media:
        Use the "Next File" and "Previous File" buttons to navigate through loaded media files.
        Media files are displayed in the application window.
        Click on the "Add Folders" button to add destination folders where you want to move the media files.

    Move Media:
        Once loaded, click on the directory buttons to move the displayed media file to the corresponding destination folder.

    Clear Directories:
        Click the "Clear Directories" button to remove all added destination folders.

Requirements:

    Python 3.x
    Tkinter (Included in standard Python library)
    PIL (Python Imaging Library)
    pillow-heif (HEIC file support for PIL)
    OpenCV (For video file support)

Installation:

    Clone the repository or download the provided Python script.
    Install the required dependencies using pip:

    $pip install pillow pillow-heif opencv-python-headless

Run the Python script:

    $python image_sorter.py
