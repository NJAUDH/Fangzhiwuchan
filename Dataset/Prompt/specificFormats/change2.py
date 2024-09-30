import csv
import json
from collections import defaultdict


def process_second_format(file_path):
    grouped_data = defaultdict(list)

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grouped_data[row['ID']].append(row)

    result = []

    for ID, items in grouped_data.items():
        entities = []

        for item in items:
            entities.append({
                "start_IDx": int(item['start_pos']),
                "end_IDx": int(item['end_pos']),
                "type": item['entity_type'],
                "entity": item['entity_name']
            })

        result.append({
            "text": items[0]['annotated_description'],  # 使用同一个 ID 下的公共 annotated_description
            "entities": entities
        })

    return result


file_path = '../filterData.csv'
output_second_format = process_second_format(file_path)

def write_to_json(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


output_json_file_path = 'second.json'
write_to_json(output_second_format, output_json_file_path)