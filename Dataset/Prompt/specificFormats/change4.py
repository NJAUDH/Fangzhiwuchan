import csv
import json
from collections import defaultdict

def process_fourth_format(file_path):
    grouped_data = defaultdict(list)

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grouped_data[row['ID']].append(row)

    result = []

    for ID, items in grouped_data.items():
        label = defaultdict(lambda: defaultdict(list))

        for item in items:
            label[item['entity_type']][item['entity_name']].append([int(item['start_pos']), int(item['end_pos'])])

        result.append({
            "text": items[0]['annotated_description'],  # 使用同一个 ID 下的公共 annotated_description
            "label": {k: dict(v) for k, v in label.items()}  # 将嵌套的 defaultdict 转换为普通字典
        })

    return result

file_path = '../filterData.csv'
output_fourth_format = process_fourth_format(file_path)

def write_to_json(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

output_json_file_path = 'fourth.json'
write_to_json(output_fourth_format, output_json_file_path)
