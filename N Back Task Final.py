import pygame
import random
import time
import json
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from pathlib import Path
from enum import Enum
from collections import deque


class TaskType(Enum):
    FLANKER = "flanker"
    N_BACK = "n_back"
    PATTERN_MEMORY = "pattern_memory"
    STROOP = "stroop"
    MENTAL_ROTATION = "mental_rotation"


@dataclass
class CognitiveTask:
    task_type: TaskType
    trial_number: int
    stimulus: Any
    correct_response: Any
    response_time: Optional[float] = None
    user_response: Optional[Any] = None
    is_correct: Optional[bool] = None
    additional_data: Optional[Dict] = None


class CognitiveSuite:
    def __init__(self, screen_size=(1024, 768)):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Cognitive Science Suite")

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.trials: List[CognitiveTask] = []
        self.participant_id: Optional[str] = None

        self.n_back_sequence = deque(maxlen=3)
        self.pattern_grid_size = (4, 4)
        self.current_pattern = None

    def display_instructions(self, instructions: List[str]) -> None:
        """Display task instructions."""
        self.screen.fill((255, 255, 255))
        y_pos = 200
        for line in instructions:
            text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text, (100, y_pos))
            y_pos += 50
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def generate_n_back_trial(self) -> CognitiveTask:
        digit = random.randint(1, 9)
        is_target = False

        if len(self.n_back_sequence) >= 2:
            is_target = random.random() < 0.3
            if is_target:
                digit = self.n_back_sequence[-2]

        self.n_back_sequence.append(digit)

        return CognitiveTask(
            task_type=TaskType.N_BACK,
            trial_number=len(self.trials),
            stimulus=digit,
            correct_response=is_target,
            additional_data={"sequence": list(self.n_back_sequence)})

    def run_n_back_trial(self, task: CognitiveTask) -> None:
        """Run a single N-back trial."""
        self.screen.fill((255, 255, 255))
        digit_text = self.font.render(str(task.stimulus), True, (0, 0, 0))
        self.screen.blit(digit_text, (self.screen_size[0] // 2 - 20, self.screen_size[1] // 2 - 20))
        pygame.display.flip()

        start_time = time.time()
        response = None

        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        response = True
                    elif event.key == pygame.K_n:
                        response = False

        task.response_time = time.time() - start_time
        task.user_response = response
        task.is_correct = response == task.correct_response

    def save_data(self) -> None:
        """Save trial data to JSON and CSV formats."""
        if not self.participant_id:
            raise ValueError("Participant ID not set")

        # Define directories for saving data
        data_dirs = ["data", "N Back Data"]
        for directory in data_dirs:
            data_dir = Path(directory)
            data_dir.mkdir(exist_ok=True)

            trial_data = []
            for trial in self.trials:
                trial_dict = {
                    "participant_id": self.participant_id,
                    "task_type": trial.task_type.value,
                    "trial_number": trial.trial_number,
                    "response_time": trial.response_time,
                    "is_correct": trial.is_correct
                }
                if trial.additional_data:
                    trial_dict.update(trial.additional_data)

                trial_data.append(trial_dict)

            # Save as JSON
            json_path = data_dir / f"participant_{self.participant_id}_cognitive_suite.json"
            with open(json_path, 'w') as f:
                json.dump(trial_data, f, indent=2, default=str)

            # Save as CSV
            df = pd.DataFrame(trial_data)
            csv_path = data_dir / f"participant_{self.participant_id}_cognitive_suite.csv"
            df.to_csv(csv_path, index=False)


def run_n_back_task(participant_id: str, ntasks_per_type: int = 20):
    """Run only the N-back task."""
    suite = CognitiveSuite()
    suite.participant_id = participant_id

    instructions = [
        "N-back Memory Task Instructions:",
        "- A sequence of digits will appear on the screen.",
        "- Press SPACE if the current digit matches the one 2-back.",
        "- Press N if it does not match.",
        "Press SPACE to start."
    ]
    suite.display_instructions(instructions)

    for _ in range(ntasks_per_type):
        task = suite.generate_n_back_trial()
        suite.trials.append(task)
        suite.run_n_back_trial(task)
        pygame.time.wait(500)

    suite.save_data()
    pygame.quit()


if __name__ == "__main__":
    ID = input("Enter Participant ID:")
    run_n_back_task(f"{ID}")
