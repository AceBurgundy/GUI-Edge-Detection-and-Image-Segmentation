# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Program import App

from customtkinter import CTkFrame, CTkLabel

class Canvases(CTkFrame):
    """
    Container for both before and after image canvases
    """
    def __init__(self, master: App, *args, **kwargs) -> None:
        """
        Initializes the Canvases object.

        Arguments:
            parent (App): The parent CTk object.
            *args: Additional arguments to pass to the parent class
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.original_canvas: CTkLabel = CTkLabel(self, text="")
        self.original_canvas.grid(padx=20, pady=10, row=0, column=0, sticky="nsew")

        self.result_canvas: CTkLabel = CTkLabel(self, text="")
        self.result_canvas.grid(padx=(0, 20), pady=10, row=0, column=1, sticky="nsew")