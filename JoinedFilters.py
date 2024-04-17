from filters_functions import grayscale, box_blur, sobel_edge_detection, canny_edge_detection, global_segmentation, kmeans_segmentation
from customtkinter import CTk, CTkLabel, CTkImage, CTkFrame
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from typing import List, Callable, Tuple, Optional
from cv2.typing import MatLike
from constants import *
from PIL import Image

class JoinedFilters(CTk):
    """
    A window containing canvases for each image filter
    """
    def __init__(self) -> None:
        """
        Initializes the JoinedFilters object.
        """
        super().__init__()
        window_width: int = 600
        window_height: int = 710
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()

        x_position: float = (screen_width - window_width) // 2
        y_position: float = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.title("Edge Detection and Image Segmentation All Options by: Sam Adrian P. Sabalo")
        self.iconbitmap(ICON_PATH)

        operations: List[Tuple[str, Optional[Callable]]] = [
            ("Main Camera", None),
            ("Grayscale", grayscale),
            ("Box Blur", box_blur),
            ("Sobel Edge Detection", sobel_edge_detection),
            ("Canny Edge Detection", canny_edge_detection),
            ("Global Segmentation", global_segmentation),
            ("K-Means Segmentation", kmeans_segmentation)
        ]

        self.capture: VideoCapture = VideoCapture(0)
        self.canvas_list = []

        self.top_container: CTkFrame = CTkFrame(self)
        self.top_container.grid(row=0, column=0)

        self.bottom_container: CTkFrame = CTkFrame(self)
        self.bottom_container.configure(fg_color="transparent")
        self.bottom_container.grid(row=1, column=0, sticky="nsew")

        for index, (text, filter) in enumerate(operations):

            canvas_card: CTkFrame = CTkFrame(self.top_container if index == 0 else self.bottom_container)

            canvas: CTkLabel = CTkLabel(canvas_card, text="")
            canvas.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")

            canvas_title: CTkLabel = CTkLabel(canvas_card, text=text)
            canvas_title.grid(row=1, column=0, sticky="nsew")

            if index == 0:
                canvas_card.grid(padx=5, pady=5, row=0, column=0, sticky="ew")
            else:
                canvas_card.grid(padx=5, pady=5, row=0 if index - 1 < 3 else 1, column=index % 3, sticky="nsew")

            self.canvas_list.append([canvas, filter])

        self.after_id: str = self.after(1, self.update_frames)

    def update_frames(self):
        """
        Updates each frame on the canvas to make it look like a camera
        """
        frame_returned, frame = self.capture.read()

        if frame_returned:
            for canvas, filter in self.canvas_list:
                frame: MatLike = cvtColor(frame, COLOR_BGR2RGB)

                if filter is None:
                    image: CTkImage = CTkImage(light_image=Image.fromarray(frame), size=(365, 280))
                    canvas.configure(image=image)
                    continue

                processed_image = filter(frame)
                processed_image: MatLike = cvtColor(processed_image, COLOR_BGR2RGB)
                image: CTkImage = CTkImage(light_image=Image.fromarray(processed_image), size=(180, 140))
                canvas.configure(image=image)

        self.after_id = self.after(1, self.update_frames)
