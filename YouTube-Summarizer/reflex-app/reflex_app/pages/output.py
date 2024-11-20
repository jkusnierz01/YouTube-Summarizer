import reflex as rx
import requests
import re


class State(rx.State):
    transcription: str
    is_received: bool = False
    
    def get_summary(self):
        match = re.search(rf"^/output/\?(?P<request_id>[A-Za-z0-9].+)", self.router_data['asPath'])
        request_id = match.group('request_id')
        try:
            transcription = requests.get(f"http://backend:8080/get_transcription?request_id={request_id}")
            self.transcription = transcription.json()['transcription']
            self.is_received = True
        except Exception as e:
            print(e)


@rx.page(route='/output', on_load=State.get_summary)
def output() -> rx.Component:
    return rx.container(
        # Add button at the top left corner
        rx.link(
            rx.button(
                "Go to Home",
                background_color="#ff7e5f",  # Button color
                color="white",  # Text color
                _hover={"background_color": "#feb47b"},  # Hover effect
                border_radius="5px",  # Rounded corners
                padding="10px 20px",  # Padding inside the button
                position="absolute",  # Position the button absolutely
                top="10px",  # 10px from the top
                left="10px",  # 10px from the left
                font_family="'Roboto', sans-serif",  # Button font style
                font_weight="bold",  # Bold font for the button
                font_size="1em",  # Size of the font
            ),
            href="http://localhost:3000",  # The redirection link
        ),
        rx.center(
            rx.heading(
                "Summary:",
                font_size="3em",  # Large font size for the title
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
                size="12",
                as_="h1",
                line_height=1.2
            ),
            padding="2em",
        ),
        rx.center(
            rx.cond(
                State.is_received,
                rx.text(
                    State.transcription, 
                    font_size="lg", 
                    line_height="1.6", 
                    color="white", 
                    font_family="'Montserrat', sans-serif",
                    text_align="center",
                    max_width="600px"
                ),
            )
        ),
        padding="20px",
    )
