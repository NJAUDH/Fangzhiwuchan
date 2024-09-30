import csv
import json


csv_file = '../filterData.csv'
json_output = []

entity_type_queries = {
    "PER": "人名",
    "LOC":"地点",
    "TIM":"时间",
    "MIS":"MIS",
    "JOB":"职业",
    "BOK":"书籍",
    "PRO":"物品"
}

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    grouped_data = {}

    for row in reader:
        ID = row['ID']
        entity_type = row['entity_type']

        if ID not in grouped_data:
            grouped_data[ID] = {}

        if entity_type not in grouped_data[ID]:
            grouped_data[ID][entity_type] = {
                "context": "（" + " ".join(row['annotated_description']) + "）",
                "end_position": [],
                "entity_label": entity_type,
                "impossible": False,
                "qas_ID": f"{ID}.1",
                "query": entity_type_queries.get(entity_type, ""),
                "span_position": [],
                "start_position": []
            }

        start_pos = int(row['start_pos'])
        end_pos = int(row['end_pos'])
        grouped_data[ID][entity_type]["start_position"].append(start_pos)
        grouped_data[ID][entity_type]["end_position"].append(end_pos)
        grouped_data[ID][entity_type]["span_position"].append(f"{start_pos};{end_pos}")

    for ID, entities in grouped_data.items():
        for i, entity_type in enumerate(entities.keys(), start=1):
            entities[entity_type]["qas_ID"] = f"{ID}.{i}"
            json_output.append(entities[entity_type])

json_file = 'sixth.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

print("JSON文件已生成")
