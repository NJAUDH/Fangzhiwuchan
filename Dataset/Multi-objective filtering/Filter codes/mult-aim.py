import pandas as pd
import re

# Load the CSV file
file_path = 'final_output_cleaned-0.8.csv'
df = pd.read_csv(file_path)

# Ensure that all script values are strings and handle NaN values
df['script'] = df['bin_description'].astype(str)

# Function to detect nested brackets
def adjusted_detect_nested_brackets(script):
    nested_brackets = re.findall(r'\[[^\]]*\[[^\]]*\][^\]]*\]', script)
    return len(nested_brackets)

# Function to count non-nested entities
def count_non_nested_entities(script, nested_brackets_count):
    entities = re.findall(r'\[[^\[]+\|[^\]]+\]', script)
    non_nested_entities_count = len(entities) - nested_brackets_count
    return non_nested_entities_count

# Calculate nested brackets count
df['nested_brackets_count'] = df['script'].apply(adjusted_detect_nested_brackets)

# Calculate non-nested entities count
df['non_nested_entities_count'] = df.apply(lambda row: count_non_nested_entities(row['script'], row['nested_brackets_count']), axis=1)

# Calculate the ratio of nested to non-nested entities
df['nested_to_non_nested_ratio'] = df['nested_brackets_count'] / df['non_nested_entities_count']

# Filter rows where the ratio is greater than or equal to 2
filtered_df = df[df['nested_to_non_nested_ratio'] >= 2]

# Save the filtered dataframe to a new CSV file
filtered_output_file_path = 'filtered_nested_non_nested_analysis-0.8.csv'
filtered_df.to_csv(filtered_output_file_path, index=False)

print(f"Filtered data saved to {filtered_output_file_path}")
