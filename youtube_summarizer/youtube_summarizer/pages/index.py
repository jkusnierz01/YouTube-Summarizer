from reflex_motion import motion
import reflex as rx
from rxconfig import config
from pipeline.full import pipeline



class FromInputState(rx.State):
    """_summary_

    Args:
        rx (_type_): _description_
    """
    url: str = ""
    
    def submit(self,form_data:dict):
        self.url = form_data.get("url")
        pipeline(self.url)
        
    

def index() -> rx.Component:
    """_summary_

    Returns:
        rx.Component: _description_
    """
    return rx.container(
        rx.center(
            rx.heading(
                "YouTube Summarizer",
                font_size="4em",  # Large font size for the title
                font_weight="bold",  # Bold font for emphasis
                text_align="center",  # Center the text
                font_family="'Roboto', sans-serif",  # Use a modern, clean font
                color="transparent",  # Start with transparent text
                background_clip="text",  # Apply background gradient to text
                background_image="linear-gradient(90deg, #ff7e5f, #feb47b)",
                webkit_background_clip="text",  # Ensure compatibility across browsers
                webkit_text_fill_color="transparent",  # Ensures text color fills with gradient
                text_shadow="2px 2px 4px rgba(0, 0, 0, 0.5)",
                margin_top="2em",  # Add margin to position the text better
                size="9",
                as_="h1",
            ),
            padding="2em",
        ),
        rx.center(
            rx.text(
                rx.text.strong("Input "),
                "link to YouTube video under ",
                font_size="1em",
                font_family="'Montserrat', sans-serif",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.form(
                    rx.vstack(
                    rx.input(
                        name='url',
                        radius="full",
                        width="200%",
                        placeholder="Input url...",
                        required=True,
                        ),
                    motion(
                        rx.button("Submit",type='submit',align='center',color_scheme='tomato'),
                        while_hover={"scale": 1.2},
                        while_tap={"scale": 0.9},
                        transition={"type": "spring", "stiffness": 400, "damping": 17},
                        ),
                    width = '100%',
                    align='center'
                    ),
                    on_submit=FromInputState.submit,
                    reset_on_submit=True
                ),
            ),
            direction="column",
            justify="center",
        ),
    )