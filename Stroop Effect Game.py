import pygame
import random
import time
import json
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


# Define a structure for game trials
@dataclass
class StroopTrial:
    word: str
    color: str
    correct_key: str
    response_time: Optional[float] = None
    user_response: Optional[str] = None
    is_correct: Optional[bool] = None


class StroopGame:
    def __init__(self, participant_id: str, screen_size=(800, 600)):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Stroop Effect Task")

        # Fonts and Colors
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)

        # Game Parameters
        self.participant_id = participant_id
        self.trials: List[StroopTrial] = []

        # Possible words and colors
        self.words = ["RED", "GREEN", "BLUE", "YELLOW"]
        self.colors = {"RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255), "YELLOW": (255, 255, 0)}
        self.color_keys = {"R": "RED", "G": "GREEN", "B": "BLUE", "Y": "YELLOW"}

    def display_text(self, text: str, color: tuple, y_offset: int = 0):
        """Display text in the center of the screen."""
        self.screen.fill(self.bg_color)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def display_instructions(self):
        """Show instructions to the user."""
        self.screen.fill(self.bg_color)
        instructions = [
            "Stroop Effect Task Instructions:",
            "- A word will appear on the screen in a color.",
            "- Press the key for the COLOR of the word, ignoring the word itself.",
            "- R = RED, G = GREEN, B = BLUE, Y = YELLOW.",
            "- Try to respond as quickly and accurately as possible.",
            "Press SPACE to begin."
        ]

        y_pos = 150
        for line in instructions:
            text = self.small_font.render(line, True, self.text_color)
            self.screen.blit(text, (50, y_pos))
            y_pos += 40

        pygame.display.flip()

        # Wait for space to start
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def generate_trial(self) -> StroopTrial:
        """Generate a single Stroop trial."""
        word = random.choice(self.words)
        color = random.choice(list(self.colors.keys()))
        correct_key = [k for k, v in self.color_keys.items() if v == color][0]
        return StroopTrial(word=word, color=color, correct_key=correct_key)

    def run_trial(self, trial: StroopTrial):
        """Run a single trial and record the response."""
        self.display_text(trial.word, self.colors[trial.color])

        start_time = time.time()
        response = None

        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    response = pygame.key.name(event.key).upper()
                    if response in self.color_keys:
                        end_time = time.time()
                        trial.response_time = end_time - start_time
                        trial.user_response = response
                        trial.is_correct = response == trial.correct_key
                    else:
                        response = None  # Ignore invalid keys

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def save_data(self):
        data_dir = Path("stroop_data")
        data_dir.mkdir(exist_ok=True)

        trial_data = [asdict(trial) for trial in self.trials]

        # Save JSON
        json_path = data_dir / f"{self.participant_id}_stroop_results.json"
        with open(json_path, "w") as f:
            json.dump(trial_data, f, indent=2)

        # Save CSV
        csv_path = data_dir / f"{self.participant_id}_stroop_results.csv"
        df = pd.DataFrame(trial_data)
        df.to_csv(csv_path, index=False)

    def run(self, num_trials=40):
        """Run the Stroop game."""
        self.display_instructions()

        for _ in range(num_trials):
            trial = self.generate_trial()
            self.trials.append(trial)
            self.run_trial(trial)
            pygame.time.wait(500)  # Pause between trials

        self.save_data()
        pygame.quit()


if __name__ == "__main__":
    # Set participant ID
    participant_id = input("Enter participant ID:")

    # Create and run the game
    game = StroopGame(participant_id)
    game.run(num_trials=40)