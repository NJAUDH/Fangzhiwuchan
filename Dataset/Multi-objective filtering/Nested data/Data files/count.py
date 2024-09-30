import csv
import os
from collections import Counter
import pandas as pd

with open('filtered_relations00014.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    filtered_relations = {tuple(row) for row in reader}

all_data = []

for filename in os.listdir('.'):
    if filename.startswith('nested_entities'):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entity_pair = (row['entity_name_id1'], row['entity_name_id2'])
                if entity_pair in filtered_relations or (entity_pair[1], entity_pair[0]) in filtered_relations:
                    all_data.append(row)

relation_counter = Counter()
entity_counter=Counter()
with open('filtered_entities.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'entity_name1', 'entity_type1', 'entity_name_id1', 'entity_name2', 'entity_type2', 'entity_name_id2', 'relation_id'])
    for row in all_data:
        writer.writerow([row['id'], row['entity_name1'], row['entity_type1'], row['entity_name_id1'], row['entity_name2'], row['entity_type2'], row['entity_name_id2'], row['relation_id']])
        relation_counter[(row['entity_name1'], row['entity_name2'])] += 1
        entity_counter[(row['entity_name1'],row['entity_type1'])]+=1
        entity_counter[(row['entity_name2'],row['entity_type2'])] += 1

sorted_relation_counter = sorted(relation_counter.items(), key=lambda item: item[1], reverse=True)

sorted_entity_counter = sorted(entity_counter.items(), key=lambda item: item[1], reverse=True)

df_relation = pd.DataFrame(sorted_relation_counter, columns=['Relation', 'Count'])

df_entity = pd.DataFrame(sorted_entity_counter, columns=['Entity', 'Count'])

relation_excel_filename = 'relation_output.xlsx'
entity_excel_filename = 'entity_output.xlsx'

df_relation.to_excel(relation_excel_filename, index=False)
df_entity.to_excel(entity_excel_filename, index=False)

print(f"Data written to {relation_excel_filename} and {entity_excel_filename}")