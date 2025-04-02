from event_handler import EventHandler
from jelly_field_state import JellyFieldState

def save_game(steps, solution_time, score, player, level):
    with open('leaderboard.csv', 'a') as file:
        file.write(f"{player},{solution_time},{score},{steps},{level}\n")
        

def play():
    jellyState = JellyFieldState()
    e = EventHandler(jellyState)
    while True:
        e.display(jellyState)
        jellyState = e.handle_events(jellyState)
    #save_game(steps, solution_time, score, "Human", file.split('.')[0])

play()