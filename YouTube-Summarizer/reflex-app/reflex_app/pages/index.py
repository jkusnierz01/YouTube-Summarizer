from reflex_motion import motion
import reflex as rx
from rxconfig import config
import requests
import re

class FormInputState(rx.State):
    url: str = ""
    is_disable: bool = True
        
        
    def submit(self, form_data: dict):
        self.url = form_data.get("url")

        try:
            response_redirect = requests.post(
                        url="http://backend:8080/process",
                        json={"url": self.url}  # Sending as JSON in the body
                    )
        except Exception as e:
            return rx.window_alert(f"Unable to connect to the backend server. Please try again later. Exception - {e}")
        else:
            if response_redirect.status_code == 200:
                request_id = response_redirect.json().get('request_id')
                if request_id is not None:
                    return rx.redirect(f"http://localhost:3000/output?{request_id}")
            else:
                # Handle other response codes (e.g., 400, 500)
                reason = response_redirect.json().get('detail', "An unknown error occurred.")
                return rx.window_alert(f"Status code: {response_redirect.status_code} - {reason}")


    def check_regex(self, url_: str):
        self.url = url_
        regex = r"https://www\.youtube\.com/watch\?v=(.+)"
        try:
            if re.search(regex, self.url) is not None:
                self.is_disable = False
            else:
                self.is_disable = True
        except:
            pass


def index() -> rx.Component:
    """Main page component with form and loading bar."""

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
                "link to YouTube video below",
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
                            on_change=FormInputState.check_regex
                        ),
                        motion(
                            rx.button("Submit", type='submit', align='center',
                                      color_scheme='tomato', disabled=FormInputState.is_disable),
                            while_hover={"scale": 1.2},
                            while_tap={"scale": 0.9},
                            transition={"type": "spring",
                                        "stiffness": 400, "damping": 17},
                        ),
                        width='100%',
                        align='center'
                    ),
                    on_submit=FormInputState.submit,
                    reset_on_submit=True
                ),
            ),
            direction="column",
            justify="center",
        ),
    )

