import reflex as rx
from .pages.index import index
from .pages.output import output
# from .utils import setup_logging
# import logging


# setup_logging("fronted-reflex", log_file ='frontend.log')
# logger = logging.getLogger(__name__)

app = rx.App()
app.add_page(index)