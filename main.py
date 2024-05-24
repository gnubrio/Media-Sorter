import os, shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import pillow_heif
import cv2


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Sorter")
        self.minsize(600, 600)
        style = ttk.Style()
        style.theme_use("clam")

        self.SUPPORTED_IMAGES = (
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".svg",
            ".heic",
        )
        self.SUPPORTED_VIDEOS = (".mp4", ".mov")

        self.media_files = []
        self.current_media_index = 0
        self.destination_paths = []
        self.directory_buttons = []

        self.setup_UI()

        self.mainloop()

    def setup_UI(self):
        # Display widgets
        media_display_frame = ttk.Frame(self, border=2, relief=tk.SOLID)
        media_display_frame.place(x=0, y=0, relwidth=0.9, relheight=0.4)

        self.media_display_label = ttk.Label(media_display_frame, image=None)
        self.media_display_label.pack()

        # Menu widgets
        menu_button_frame = ttk.Frame(self, border=2, relief=tk.SOLID)
        menu_button_frame.place(relx=0.9, y=0, relwidth=0.1, relheight=1)
        
        menu_button_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        menu_button_frame.columnconfigure(0, weight=1)

        load_media_button = ttk.Button(
            menu_button_frame, text="Load Images", command=self.load_media
        )
        load_media_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=10)

        add_directories_button = ttk.Button(
            menu_button_frame, text="Add Folders", command=self.add_destinations
        )
        add_directories_button.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=10)

        clear_directories_button = ttk.Button(
            menu_button_frame,
            text="Clear Directories",
            command=self.clear_directory_buttons,
        )
        clear_directories_button.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=10)

        next_media_button = ttk.Button(
            menu_button_frame,
            text="Next File",
            command=lambda: self.change_media("next"),
        )
        next_media_button.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=10)

        previous_media_button = ttk.Button(
            menu_button_frame,
            text="Previous File",
            command=lambda: self.change_media("previous"),
        )
        previous_media_button.grid(row=4, column=0, sticky=tk.NSEW, padx=5, pady=10)

        # Directory widgets
        self.directory_button_frame = ttk.Frame(self, border=2, relief=tk.SOLID)
        self.directory_button_frame.place(x=0, rely=0.4, relwidth=0.9, relheight=0.6)

    def load_media(self):
        # Reset media files        
        self.media_files = []
        self.current_media_index = 0

        # Load all media files in directory and subdirectories
        directory = filedialog.askdirectory(title="Select Folder")

        if os.path.isdir(directory):
            for root_directory, subdirectories, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(
                        (self.SUPPORTED_IMAGES + self.SUPPORTED_VIDEOS)
                    ):
                        file_path = os.path.join(root_directory, file)
                        self.media_files.append(file_path)

        self.display_media()

    def display_media(self):
        # Repack media label and find current index
        self.media_display_label.pack()
        media = self.media_files[self.current_media_index]
        max_height = 400

        # Resize and display image files
        if media.lower().endswith(self.SUPPORTED_IMAGES):
            pillow_heif.register_heif_opener()
            img = Image.open(media)
            img.thumbnail((10000, max_height))
            self.img_tk = ImageTk.PhotoImage(image=img)

        # Resize and display video files
        elif media.lower().endswith(self.SUPPORTED_VIDEOS):
            video = cv2.VideoCapture(media)
            ret, frame = video.read()
            video.release()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, _ = frame_rgb.shape
            aspect_ratio = width / height
            new_height = min(max_height, height)
            new_width = int(new_height * aspect_ratio)
            frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
            self.img_tk = ImageTk.PhotoImage(image=Image.fromarray(frame_resized))

        # Apply media to media label
        self.media_display_label.config(image=self.img_tk)
        self.update_idletasks()

    def change_media(self, direction):
        # Seek through media in media array
        if direction == "next" and self.current_media_index < len(self.media_files) - 1:
            self.current_media_index += 1
            self.display_media()
        elif direction == "previous" and self.current_media_index > 0:
            self.current_media_index -= 1
            self.display_media()
        else:
            return

    def move_media(self, index):
        # Move media and remove from media array
        if len(self.media_files) > 0:
            shutil.move(
                self.media_files[self.current_media_index],
                self.destination_paths[index],
            )
            del self.media_files[self.current_media_index]

            # Display next, previous, or no media
            if len(self.media_files) == 0:
                self.media_display_label.pack_forget()
            elif self.current_media_index == len(self.media_files):
                self.change_media("previous")
            else:
                self.display_media()
        else:
            return

    def add_destinations(self):
        # Add subdirectories if possible, if not add selected directory
        directory = filedialog.askdirectory(title="Select Folder")

        # Search for sub directories
        if any(
            os.path.isdir(os.path.join(directory, content))
            for content in os.listdir(directory)
        ):
            # Add subdirectories
            for content in os.listdir(directory):
                content_path = os.path.join(directory, content)
                if os.path.isdir(content_path):
                    path = os.path.join(directory, content_path)
                    if path not in self.destination_paths:
                        self.destination_paths.append(path)
                    else:
                        print(f"{content} already loaded")
        # Add selected directory if not subdirectories
        else:
            if directory not in self.destination_paths:
                self.destination_paths.append(directory)
            else:
                print(f"{directory} already loaded")

        # Create buttons for directories
        if len(self.destination_paths) != 0:
            self.create_directory_buttons()

    def create_directory_buttons(self):
        # Setup buttons with amount of directories provided
        max_columns = 10
        button_count = len(self.destination_paths)
        row_count = (button_count + max_columns - 1) // max_columns

        # Sort basename of directories
        directory_names = [(os.path.basename(path), i) for i, path in enumerate(self.destination_paths)]
        sorted_directories = sorted(directory_names, key=lambda x: x[0].lower())

        # Create buttons
        for i, (directory_name, index) in enumerate(sorted_directories):
            directory_button = ttk.Button(
                self.directory_button_frame,
                text=directory_name,
                command=lambda idx=index: self.move_media(idx),
            )
            directory_button.grid(
                row=i // max_columns,
                column=i % max_columns,
                sticky=tk.EW,
                padx=5,
                pady=5,
            )

            self.directory_buttons.append(directory_button)

        # Configure buttons
        for i in range(row_count):
            self.directory_button_frame.rowconfigure(i, weight=1)
        for i in range(max_columns):
            self.directory_button_frame.columnconfigure(i, weight=1)

    def clear_directory_buttons(self):
        # Clear all directories
        for button in self.directory_buttons:
            button.destroy()

        self.directory_buttons = []
        self.destination_paths = []


if __name__ == "__main__":
    App()
