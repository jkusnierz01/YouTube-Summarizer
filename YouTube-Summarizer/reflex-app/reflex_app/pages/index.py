from reflex_motion import motion
import reflex as rx
from rxconfig import config
import requests
import re


class FormInputState(rx.State):
    url: str = ""
    is_disable: bool = True
    is_process_unsuccessful: bool = False
    reason: str = None

    def change(self):
        self.is_process_unsuccessful = not (self.is_process_unsuccessful)
        self.reason = None
        
        
    def submit(self, form_data: dict):
        self.url = form_data.get("url")
        
        if self.is_process_unsuccessful:
            self.change()
        try:
            response_redirect = requests.post(
                url=f"http://backend:8080/process?url={self.url}")
            print("Response received!")
        except Exception as e:
            print(f"Exception: {e}")
            self.is_process_unsuccessful = True
            self.reason = "Unable to connect to the backend server. Please try again later."
        else:
            if response_redirect.status_code == 200:
                request_id = response_redirect.json().get('request_id')
                if request_id is not None:
                    return rx.redirect(f"http://localhost:3000/output?{request_id}")
                # If no request_id is returned
            else:
                # Handle other response codes (e.g., 400, 500)
                self.is_process_unsuccessful = True
                self.reason = response_redirect.json().get('detail', "An unknown error occurred.")

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

class CondState(rx.State):
    show_first: bool = False
    show_second: bool = False
    show_second: bool = False

    def change_first(self):
        self.show_first = not (self.show_first)

    def change_second(self):
        self.show_second = not (self.show_second)

    def change_third(self):
        self.show_second = not (self.show_second)

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
                rx.center(
                    rx.cond(
                        FormInputState.is_process_unsuccessful,
                        rx.box(
                            rx.text(
                                "Process Unsuccessful",
                                font_size="1.2em",
                                font_weight="bold",
                                color="#ff4d4f",  # Light red color
                                margin_bottom="0.5em",
                                text_align="center",
                            ),
                            rx.text(
                                FormInputState.reason,
                                font_size="1em",
                                color="#ff7875",  # Softer red color for details
                                line_height="1.5",
                                font_family="'Montserrat', sans-serif",
                                text_align="center",
                                padding="1em",
                                border="1px solid #ffa39e",
                                border_radius="8px",
                                background="#fff1f0",
                                box_shadow="0px 4px 6px rgba(0, 0, 0, 0.1)",
                                max_width="600px",  # Constrain max width of the box
                                margin="1em auto",  # Center the box and add spacing
                                word_wrap="break-word",  # Break long words to prevent overflow
                                overflow="hidden",  # Ensure no content overflows the box
                            ),
                            max_width="100%",  # Prevent the box from exceeding the parent container
                        ),
                    )
                ),
            ),
            direction="column",
            justify="center",
        ),
    )

