"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from .pages.index import index
from pipeline.transcribe import load__model




app = rx.App()
app.add_page(index)
