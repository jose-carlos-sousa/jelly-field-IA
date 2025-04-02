from screens import main_menu_screen, leaderboard, game_screen, level_select, player_select
import pandas as pd
import pygame

class EventHandler:
    def __init__(self, state):
        pygame.init()
        self.screens = {'main_menu': main_menu_screen.MainMenuScreen(),
                        'leaderboard': leaderboard.Leaderboard(self.load_leaderboard()),
                        'level_select': level_select.LevelSelect(),
                        'player_select': player_select.PlayerSelect()
                        }
        
        self.current_screen = "main_menu"

    def load_leaderboard(self):
        df = pd.read_csv('leaderboard.csv')
        df.set_index('Player')
        df.sort_values('Score', ascending=False, inplace=True)
        return df.head(10)

    def display(self, state):
        self.screens[self.current_screen].display(state)

    def tick(self, fps):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
        exit()

    def handle_events(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            else:
                next_screen, next_state = self.screens[self.current_screen].handle_event(state, event)
                if self.current_screen == "player_select" and next_screen == "game_screen":
                    self.screens['game_screen'] = game_screen.GameScreen(next_state)
                self.current_screen = next_screen
                return next_state
        return state
