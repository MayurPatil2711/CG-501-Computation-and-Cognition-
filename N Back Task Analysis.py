import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path


def load_data(participant_id: str, data_folder="N Back Data") -> pd.DataFrame:
    """Load both JSON and CSV data for the given participant from the specified folder."""
    json_file = Path(data_folder) / f"participant_{participant_id}_cognitive_suite.json"
    csv_file = Path(data_folder) / f"participant_{participant_id}_cognitive_suite.csv"

    if csv_file.exists():
        # Load data from the CSV file
        df = pd.read_csv(csv_file)
    elif json_file.exists():
        # Load data from the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)
        # Convert the JSON data into a DataFrame
        df = pd.DataFrame(data)
    else:
        raise FileNotFoundError(f"Data for participant {participant_id} not found in {data_folder}")

    return df


def analyze_data(df: pd.DataFrame):
    """Perform analysis on the loaded data."""
    # Calculate the overall accuracy
    total_trials = len(df)
    correct_trials = df["is_correct"].sum()
    accuracy = (correct_trials / total_trials) * 100
    print(f"Overall Accuracy: {accuracy:.2f}%")

    # Calculate response time statistics
    response_times = df["response_time"].dropna()
    avg_response_time = response_times.mean()
    min_response_time = response_times.min()
    max_response_time = response_times.max()
    print(f"Average Response Time: {avg_response_time:.2f} seconds")
    print(f"Min Response Time: {min_response_time:.2f} seconds")
    print(f"Max Response Time: {max_response_time:.2f} seconds")

    # Plot a histogram of response times
    plt.figure(figsize=(10, 6))
    plt.hist(response_times, bins=30, edgecolor='black', alpha=0.7)
    plt.title("Distribution of Response Times")
    plt.xlabel("Response Time (seconds)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    # Plot the accuracy over trials
    accuracy_per_trial = df["is_correct"].astype(int)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(df) + 1), accuracy_per_trial, marker='o', linestyle='-', color='b')
    plt.title("Accuracy Over Trials")
    plt.xlabel("Trial Number")
    plt.ylabel("Accuracy (Correct = 1, Incorrect = 0)")
    plt.grid(True)
    plt.show()


def main():
    participant_id = input("Enter the participant ID to analyze: ")
    try:
        # Load the data
        df = load_data(participant_id)

        # Analyze the data
        analyze_data(df)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()