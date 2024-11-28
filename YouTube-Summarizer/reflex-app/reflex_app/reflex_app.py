import reflex as rx
from .pages.index import index
from .pages.output import output

app = rx.App()
app.add_page(index)