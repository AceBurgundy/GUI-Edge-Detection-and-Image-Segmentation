from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, imread
from customtkinter import CTk, CTkImage
from cv2.typing import MatLike
from typing import Optional
from PIL import Image

from custom_types import IMAGE_FILTER_TYPES, IMAGE_FILTERS
from Properties import FilterProperties
from Navigation import Navigation
from Canvases import Canvases
from CTkToast import CTkToast
from constants import *

class App(CTk):
    """
    The main process of the app.
    """
    def __init__(self) -> None:
        """
        Initializes the App object.
        """
        super().__init__()
        window_width: int = 1280
        window_height: int = 720
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()

        x_position: float = (screen_width - window_width) // 2
        y_position: float = (screen_height - window_height) // 2

        self.image_filter_reference: Optional[IMAGE_FILTER_TYPES] = None
        self.current_image_filter: Optional[IMAGE_FILTERS] = None
        self.loaded_image: Optional[str] = None

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.title("Edge Detection and Image Segmentation by: Sam Adrian P. Sabalo")
        self.iconbitmap(ICON_PATH)

        self.navigation: Navigation = Navigation(parent=self, fg_color="transparent", bg_color="transparent")
        self.navigation.grid(row=0, column=0, sticky="nsew")

        self.canvases: Canvases = Canvases(self, fg_color="transparent", bg_color="transparent")
        self.canvases.grid(row=1, column=0, sticky="nsew")

        self.filter_properties: FilterProperties = FilterProperties(self, fg_color="transparent", bg_color="transparent")
        self.filter_properties.grid_columnconfigure(0, weight=1)
        self.filter_properties.grid(row=2, column=0, sticky="nsew", padx=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.capture: VideoCapture = VideoCapture(0)
        self.after_id: str = self.after(10, self.update_frames)

        CTkToast(master=self)

    def update_frames(self):
        """
        Updates each frame on the canvas to make it look like a camera
        """
        frame_returned, frame = self.capture.read()

        if not frame_returned:
            self.after_id = self.after(10, self.update_frames)
            return

        frame: MatLike = cvtColor(frame, COLOR_BGR2RGB)
        image: CTkImage = CTkImage(light_image=Image.fromarray(frame), size=DEFAULT_CANVAS_SIZE)

        if self.loaded_image is not None:
            image = CTkImage(light_image=Image.open(self.loaded_image), size=DEFAULT_CANVAS_SIZE)

        # Shows the unfiltered camera to the original_canvas
        self.canvases.original_canvas.configure(image=image)

        # Shows the unfiltered camera to the result canvas too if no filters was selected
        if self.image_filter_reference is None:
            self.canvases.result_canvas.configure(image=image)
            self.after_id = self.after(10, self.update_frames)
            return

        # Image filter option not used yet
        if self.current_image_filter is None:
            # Sets the filter to the instance of the filter the user had chosen
            self.current_image_filter = self.image_filter_reference()
            self.filter_properties.generate()

        # If the camera filter used has been replaced
        if self.current_image_filter and self.image_filter_reference.__name__ != self.current_image_filter.__class__.__name__:
            # Sets the filter to the instance of the filter the user had chosen
            self.current_image_filter = self.image_filter_reference()

            for widget in self.filter_properties.winfo_children():
                widget.destroy()

            self.filter_properties.generate()

        def process_image(image_data: MatLike) -> None:
            """
            Loads the image data to the canvas
            """
            loaded_image_data: MatLike = cvtColor(image_data, COLOR_BGR2RGB) # type: ignore

            if self.current_image_filter is None:
                return

            processed_image: MatLike = self.current_image_filter.apply(loaded_image_data)
            processed_image = cvtColor(processed_image, COLOR_BGR2RGB)

            image: Image.Image = Image.fromarray(processed_image)
            ctk_image: CTkImage = CTkImage(light_image=image, size=DEFAULT_CANVAS_SIZE)
            self.canvases.result_canvas.configure(image=ctk_image)

        if self.loaded_image is not None:
            image_data: MatLike = imread(self.loaded_image)
            process_image(image_data)
        else:
            image_data: MatLike = self.current_image_filter.apply(frame)
            process_image(image_data)

        self.after_id = self.after(10, self.update_frames)

if __name__ == '__main__':
    App().mainloop()
