"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from reflex_motion import motion

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.center(
            motion(
                rx.button(
                    "Click me"
                ),
                while_hover={"scale": 1.2},
                while_tap={"scale": 0.9},
                transition={"type": "spring", "stiffness": 400, "damping": 17},
            )
        ),
        )
    )


app = rx.App()
app.add_page(index)
