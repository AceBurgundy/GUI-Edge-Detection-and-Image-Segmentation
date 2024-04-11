# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Program import App

from customtkinter import CTkFrame, CTkLabel, CTkSlider
from class_methods import get_instance_properties
from typing import Any, Dict, Optional, Callable
from constants import *

class FilterProperties(CTkFrame):
    """
    Manages a filters attributes
    """
    def __init__(self, master: App, *args, **kwargs) -> None:
        """
        Initializes the FilterProperties object.

        Arguments:
            parent (App): The parent CTk object.
            *args: Additional arguments to pass to the parent class
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(master=master, *args, **kwargs)
        self.parent: App = master

    def generate(self) -> None:
        """
        Generates properties to easily control image filter props.
        """
        if self.parent.current_image_filter is None:
            return

        filter_properties: Dict[str, Dict[str, Callable]] = get_instance_properties(self.parent.image_filter_reference)
        filter_properties_data = self.parent.current_image_filter.property_data

        for index, property_name in enumerate(filter_properties):
            getters_setters: Dict[str, Callable] = filter_properties[property_name]

            properties_data: Optional[Any] = filter_properties_data.get(property_name, None)
            getter: Optional[Callable] = getters_setters.get("getter", None)
            setter: Optional[Callable] = getters_setters.get("setter", None)

            min: int = properties_data.get("min") if properties_data else 0
            max: int = properties_data.get("max") if properties_data else 200

            property_card: CTkFrame = CTkFrame(self)
            property_card.grid_columnconfigure(0, weight=1)
            property_card.grid_rowconfigure(0, weight=1)
            property_card.grid(row=index, sticky="nsew", pady=BOTTOM_PADDING_ONLY)

            label: CTkLabel = CTkLabel(property_card, text=property_name.capitalize())
            label.grid(row=0, column=0, padx=(25,0), pady=(10,5), sticky="nsw")

            def slider_event(value):
                if setter:
                    setter(self.parent.current_image_filter, value)

            slider: CTkSlider = CTkSlider(property_card, from_=min, to=max, command=slider_event)
            slider.grid(row=1, column=0, sticky="nsew", pady=(0,20), padx=20)

            if getter:
                current_property_value = getter(self.parent.current_image_filter)
                slider.set(current_property_value)
