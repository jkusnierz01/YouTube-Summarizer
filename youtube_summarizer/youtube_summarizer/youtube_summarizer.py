"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from reflex_motion import motion

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    """_summary_

    Returns:
        rx.Component: _description_
    """
    return rx.container(

        rx.center(
            rx.heading(
                "YouTube Summarizer",
                font_size="4em",                  # Large font size for the title
                font_weight="bold",               # Bold font for emphasis
                text_align="center",              # Center the text
                font_family="'Roboto', sans-serif",  # Use a modern, clean font
                color="transparent",              # Start with transparent text
                background_clip="text",           # Apply background gradient to text
                background_image="linear-gradient(90deg, #ff7e5f, #feb47b)",
                webkit_background_clip="text",    # Ensure compatibility across browsers
                webkit_text_fill_color="transparent",  # Ensures text color fills with gradient
                text_shadow="2px 2px 4px rgba(0, 0, 0, 0.5)",
                margin_top="2em",                 # Add margin to position the text better
                size='9',
                as_='h1',
            ),
            padding="2em",
        ),
        rx.center(
            rx.text(
                rx.text.strong("Input "), "link to YouTube video under ",
                font_size="1em",
                font_family="'Montserrat', sans-serif",
                margin_bottom = '1em'
            ),
            rx.input(
                radius='full',
                width = '50%',
                placeholder="Input url..."
            ),
            direction='column',
            justify='center',
        )
    )


app = rx.App()
app.add_page(index)
