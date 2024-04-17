# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from Program import App

from filters import GrayscaleConverter, BoxBlurFilter, SobelEdgeDetector, CannyEdgeDetector, GlobalSegmentation, KMeansSegmentation
from save import open_file_dialog, save_file_dialog
from custom_types import IMAGE_FILTER_TYPES
from JoinedFilters import JoinedFilters
from CTkToast import CTkToast
from constants import *

from customtkinter import CTkFrame, CTkButton, CTkImage
from cv2 import COLOR_RGB2BGR, cvtColor, imwrite
from cv2.typing import MatLike
from numpy import array

class Navigation(CTkFrame):

    def __init__(self, parent: App, **kwargs):
        """
        Initializes the Navigation object.

        Arguments:
            parent (App): The parent CTk object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.

        Raises:
            TypeError: If the list of buttons is empty.
        """
        super().__init__(parent, **kwargs)
        self.parent: App = parent
        self.create_filter_buttons()

        def open_joined_canvas() -> None:
            """
            Stops the app and opens a new window containing all canvas and options
            """
            self.parent.destroy()
            JoinedFilters().mainloop()

        def load_image() -> None:
            """
            Loads an image instead of showing the camera
            """
            image_path: Optional[str] = open_file_dialog()
            self.parent.loaded_image = image_path

        def clear_loaded_image() -> None:
            """
            Clears the loaded image and any image operations used which automatically reverts back to the camera.
            """
            self.parent.image_filter_reference = None
            self.parent.current_image_filter = None
            self.parent.loaded_image = None

            for widget in self.parent.filter_properties.winfo_children():
                widget.destroy()

        def save_image() -> None:
            """
            Save the image displayed on self.canvases.result_canvas using cv2.imwrite()
            """
            ctk_image_instance: CTkImage = self.parent.canvases.result_canvas.cget("image")
            file_path: Optional[str] = save_file_dialog()

            if file_path is None:
                CTkToast.toast("No path given")
                return

            if ctk_image_instance is None:
                CTkToast.toast("No image to save")
                return

            # Convert the image to OpenCV format (RGB)
            img_data: MatLike = ctk_image_instance.cget("light_image").convert("RGB")
            img_data = cvtColor(array(img_data), COLOR_RGB2BGR)
            imwrite(file_path, img_data)

        buttons: List[Tuple[CTkButton, str]] = [
            (CTkButton(self, width=50, command=clear_loaded_image), "Camera"),
            (CTkButton(self, width=50, command=open_joined_canvas), "All"),
            (CTkButton(self, width=50, command=load_image), "Load"),
            (CTkButton(self, width=50, command=save_image), "Save")
        ]

        if len(buttons) >= 0:
            for button, text in buttons:
                button.configure(text=text)
                button.pack(side="left", padx=DEFAULT_PADDING, pady=(10, 0))

    def create_filter_buttons(self):
        """
        Creates the image option buttons for the canvas
        """
        def set_operation(operation: IMAGE_FILTER_TYPES) -> None:
            """
            Sets the program image operation to be used
            """
            self.parent.image_filter_reference = operation

        operations: List[Tuple[str, IMAGE_FILTER_TYPES]] = [
            ("Grayscale", GrayscaleConverter),
            ("Box Blur", BoxBlurFilter),
            ("Sobel Edge Detection", SobelEdgeDetector),
            ("Canny Edge Detection", CannyEdgeDetector),
            ("Global Segmentation", GlobalSegmentation),
            ("K-Means Segmentation", KMeansSegmentation)
        ]

        for index, (text, operation) in enumerate(operations):
            button: CTkButton = CTkButton(self, text=text, command=lambda op=operation: set_operation(op), width=50)
            button.pack(side="left", padx=(20, DEFAULT_PADDING) if index == 0 else DEFAULT_PADDING, pady=(10, 0))
