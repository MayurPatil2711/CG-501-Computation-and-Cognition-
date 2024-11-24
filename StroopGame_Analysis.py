import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from CSV file
participant_id = input("Enter participant ID to analyze: ")
csv_path = f"stroop_data/{participant_id}_stroop_results.csv"

# Read the data into a DataFrame
df = pd.read_csv(csv_path)

# Display basic statistics about the data
print("Data Overview:")
print(df.describe())

# 1. Accuracy over trials
accuracy = df["is_correct"].mean()
print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

# 2. Response time analysis
avg_response_time = df["response_time"].mean()
print(f"Average Response Time: {avg_response_time:.2f} seconds")

# 3. Accuracy and response time by trial number
plt.figure(figsize=(10, 5))

# Accuracy over trials
plt.subplot(1, 2, 1)
sns.lineplot(x=df.index, y=df["is_correct"], marker='o', color="blue")
plt.title("Accuracy Over Trials")
plt.xlabel("Trial Number")
plt.ylabel("Accuracy")
plt.ylim(-0.1, 1.1)

# Response time over trials
plt.subplot(1, 2, 2)
sns.lineplot(x=df.index, y=df["response_time"], marker='o', color="red")
plt.title("Response Time Over Trials")
plt.xlabel("Trial Number")
plt.ylabel("Response Time (seconds)")

plt.tight_layout()
plt.show()

# 4. Accuracy by Word-Color Combination
accuracy_by_word_color = df.groupby(["word", "color"])["is_correct"].mean().reset_index()
print("\nAccuracy by Word-Color Combination:")
print(accuracy_by_word_color)

# Plot Accuracy by Word-Color
plt.figure(figsize=(8, 6))
sns.barplot(x="word", y="is_correct", hue="color", data=accuracy_by_word_color)
plt.title("Accuracy by Word-Color Combination")
plt.xlabel("Word")
plt.ylabel("Accuracy")
plt.show()

# 5. Response time by Word-Color Combination
response_time_by_word_color = df.groupby(["word", "color"])["response_time"].mean().reset_index()
print("\nAverage Response Time by Word-Color Combination:")
print(response_time_by_word_color)

# Plot Response Time by Word-Color
plt.figure(figsize=(8, 6))
sns.barplot(x="word", y="response_time", hue="color", data=response_time_by_word_color)
plt.title("Average Response Time by Word-Color Combination")
plt.xlabel("Word")
plt.ylabel("Average Response Time (seconds)")
plt.show()

# 6. Distribution of Response Times
plt.figure(figsize=(8, 6))
sns.histplot(df["response_time"], kde=True, bins=15, color="green")
plt.title("Distribution of Response Times")
plt.xlabel("Response Time (seconds)")
plt.ylabel("Frequency")
plt.show()

# 7. Response Time and Accuracy Correlation
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["response_time"], y=df["is_correct"], color="purple")
plt.title("Response Time vs Accuracy")
plt.xlabel("Response Time (seconds)")
plt.ylabel("Accuracy (1 = Correct, 0 = Incorrect)")
plt.show()