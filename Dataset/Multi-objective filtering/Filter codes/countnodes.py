# Load the uploaded filtered_relations file
import pandas as pd

filtered_relations_path = 'filtered_relations0.csv'
filtered_relations_df = pd.read_csv(filtered_relations_path)

# Count the number of unique IDs (including both entity_id1 and entity_id2)
unique_ids = pd.concat([filtered_relations_df['entity_id1'], filtered_relations_df['entity_id2']]).nunique()

print(unique_ids)
