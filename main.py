from event_handler import EventHandler
from jelly_field_state import JellyFieldState

def play():
    jellyState = JellyFieldState()
    e = EventHandler(jellyState)
    while True:
        e.display(jellyState)
        jellyState = e.handle_events(jellyState)

play()