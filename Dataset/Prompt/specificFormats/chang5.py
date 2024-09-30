import csv
import json


def csv_to_json(file_path, output_file):
    result = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)


        grouped_data = {}
        for row in reader:
            if row['ID'] not in grouped_data:
                grouped_data[row['ID']] = {
                    "ID": int(row['ID']),
                    "text": row['annotated_description'],
                    "entity_list": []
                }
            entity = {
                "text": row['entity_name'],
                "type": row['entity_type'],
                "char_span": [int(row['start_pos']), int(row['end_pos'])],
                "tok_span": [int(row['start_pos']), int(row['end_pos'])]  # 如果有不同的 token 范围，可以修改
            }
            grouped_data[row['ID']]["entity_list"].append(entity)


        for key in grouped_data:
            result.append(grouped_data[key])


    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)



file_path = '../filterData.csv'

output_file = 'fifth.json'


csv_to_json(file_path, output_file)

print("CSV 已成功转换为 JSON 并写入 fifth.json。")
