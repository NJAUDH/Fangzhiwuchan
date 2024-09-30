import csv
import json
import csv
import json
from collections import defaultdict


def process_first_format(file_path):
    grouped_data = defaultdict(list)


    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grouped_data[row['ID']].append(row)

    result = []

    for ID, items in grouped_data.items():
        tokens = list(items[0]['annotated_description'])  # 使用同一个 ID 下的公共 annotated_description
        entity_mentions = []

        for item in items:
            entity_mentions.append({
                "entity_type": item['entity_type'],
                "start": int(item['start_pos']),
                "end": int(item['end_pos']),
                "text": item['entity_name']
            })

        result.append({
            "tokens": tokens,
            "entity_mentions": entity_mentions
        })

    return result


file_path = '../filterData.csv'
output_first_format = process_first_format(file_path)

def write_to_json(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


output_json_file_path = 'first.json'
write_to_json(output_first_format, output_json_file_path)