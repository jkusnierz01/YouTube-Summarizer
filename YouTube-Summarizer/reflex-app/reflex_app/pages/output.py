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
            transcription = requests.get(f"http://0.0.0.0:80//get_transcription?request_id={request_id}")
            self.transcription = transcription.json()['transcription']
            self.is_received = True
        except Exception as e:
            print(e)

@rx.page(route='/output', on_load=State.get_summary)
def output() -> rx.Component:
    return rx.container(
        rx.center(
            rx.cond(State.is_received, rx.text(State.transcription))
        )
    )