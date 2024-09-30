import json
import os
import re

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def parse_model_output(content):
    entries = content.strip().split("identity_")
    parsed_data = []
    for entry in entries[1:]:
        entry_id, assistant_value = entry.split(":", 1)
        assistant_value = assistant_value.strip()
        if "共现关系：" not in assistant_value:
            assistant_value += "\n共现关系：None;\n"
        assistant_value = re.sub(r'\n\s*\n', '\n', assistant_value)
        cleaned_entry = {"id": "identity_" + entry_id.strip()}
        conversations = [{"from": "assistant", "value": assistant_value}]
        cleaned_entry["conversations"] = conversations
        parsed_data.append(cleaned_entry)
    return parsed_data

def clean_data(all_data):
    for data in all_data:
        assistant_value = data['conversations'][0]['value']
        relation = assistant_value.split("\n", 2)[1]
        data['conversations'][0]['value'] = relation
    return all_data

def extract_entities(cooccurrence_sentence):
    entities = set()
    matches = re.findall(r"\s*\'entity:\'([^\']+)'", cooccurrence_sentence)
    for match in matches:
        entities.add(match)
    return entities

def extract_cooccurrences(cleaned_data, true_data):
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_dict = {item['id']: item for item in true_data}
    for item in cleaned_data:
        item_id = item['id']
        if item_id in true_dict:
            true_item = true_dict[item_id]
            true_value = true_item['conversations'][1]['value'].split(";")[1]
            cooccurrence_pred_sentence = item['conversations'][0]['value']
            true_entities = extract_entities(true_value)
            pred_entities = extract_entities(cooccurrence_pred_sentence)
            true_positive += len(true_entities & pred_entities)
            false_positive += len(pred_entities - true_entities)
            false_negative += len(true_entities - pred_entities)
    return true_positive, false_positive, false_negative

def calculate_metrics(true_positive, false_positive, false_negative):
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

def evaluate(cleaned_data, true_data):
    true_positive, false_positive, false_negative = extract_cooccurrences(cleaned_data, true_data)
    return calculate_metrics(true_positive, false_positive, false_negative)

def process_folder(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.startswith("bb_whole") and filename.endswith(".txt"):
            model_output_path = os.path.join(folder_path, filename)
            true_data_path = os.path.join(folder_path, filename.replace("bb_whole", "dataset").replace("_result.txt","_examples_test.json"))
            model_output_content = read_file(model_output_path)
            true_data_content = read_file(true_data_path)
            cleaned_data = parse_model_output(model_output_content)
            true_data = json.loads(true_data_content)
            cleaned_data = clean_data(cleaned_data)
            precision, recall, f1 = evaluate(cleaned_data, true_data)
            results.append(f"{filename}: Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}")
    return "\n".join(results)

folder_path = 'E:\\lh_data_7_23\\9_24_llm_evaluate\\pick_in_whole'
results = process_folder(folder_path)
with open('relation_result.txt', 'w', encoding='utf-8') as file:
    file.write(results)