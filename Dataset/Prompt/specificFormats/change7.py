import csv
import json
from collections import defaultdict, Counter

def process_third_format(file_path):
    grouped_data = defaultdict(list)
    entity_counter = Counter()

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grouped_data[row['ID']].append(row)
            entity_counter[row['entity_name']] += 1

    result = []

    for ID, items in grouped_data.items():
        labels = []
        candIDate_entities = set()


        for IDx, item in enumerate(items):
            labels.append([
                f"T{IDx + 1}",
                item['entity_type'],
                int(item['start_pos']),
                int(item['end_pos']),
                item['entity_name']
            ])

        text = items[0]['annotated_description']
        for entity in entity_counter:
            if entity in text:
                candIDate_entities.add(entity)

        result.append({
            "ID": int(ID),
            "text": text,
            "labels": labels,
            "pseudo": 0,
            "candIDate_entities": list(candIDate_entities)
        })

    return result

file_path = '../filterData.csv'
output_second_format = process_third_format(file_path)

def write_to_json(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


output_json_file_path = 'seventh.json'
write_to_json(output_second_format, output_json_file_path)
