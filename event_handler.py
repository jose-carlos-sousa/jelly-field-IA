from screens import main_menu_screen, leaderboard, game_screen, level_select, player_select, ai_game, victory, defeat
import pandas as pd
import pygame

class EventHandler:
    def __init__(self, state):
        pygame.init()
        self.screens = {'main_menu': main_menu_screen.MainMenuScreen(),
                        'level_select': level_select.LevelSelect(),
                        'player_select': player_select.PlayerSelect(),
                        'victory': victory.Victory(),
                        'defeat': defeat.Defeat()
                        }
        
        self.current_screen = "main_menu"

    def load_leaderboard(self):
        df = pd.read_csv('leaderboard.csv')
        df.set_index('Player')
        df.sort_values('Score', ascending=False, inplace=True)
        return df.head(10)

    def save_game(self, steps, solution_time, score, player, level):
        with open('leaderboard.csv', 'a') as file:
            file.write(f"{player},{solution_time},{score},{steps},{level}\n")

    def display(self, state):
        self.screens[self.current_screen].display(state)

    def tick(self, fps):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
        exit()

    def handle_events(self, state):
        if(not pygame.event.peek()):
            if not state.nextBestMove:
                state.load_next_best_move()
            return state
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
                self.quit()
        else:
                next_screen, next_state = self.screens[self.current_screen].handle_event(state, event)
                if self.current_screen == "player_select":
                    if next_screen == "game_screen":
                        self.screens['game_screen'] = game_screen.GameScreen(next_state)
                    elif next_screen == "ai_game":
                        self.screens['ai_game'] = ai_game.AIGame(next_state)
                if next_screen == "victory" and self.current_screen == "game_screen":
                    self.save_game(state.stats['steps'], state.stats['time'], state.stats['score'], state.player, state.stats['level'])
                if next_screen == "leaderboard" and self.current_screen != "leaderboard":
                    self.screens['leaderboard'] = leaderboard.Leaderboard(self.load_leaderboard())

                self.current_screen = next_screen
                return next_state
        return state
