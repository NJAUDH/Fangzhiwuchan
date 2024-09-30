import json
import random
import os


def split_data(input_file, output_dir, train_ratio=0.7, dev_ratio=0.15, test_ratio=0.15):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    random.shuffle(data)
    total_size = len(data)
    train_size = int(total_size * train_ratio)
    dev_size = int(total_size * dev_ratio)

    train_data = data[:train_size]
    dev_data = data[train_size:train_size + dev_size]
    test_data = data[train_size + dev_size:]

    base_name = os.path.splitext(os.path.basename(input_file))[0]

    with open(os.path.join(output_dir, f'{base_name}_train.json'), 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_dir, f'{base_name}_dev.json'), 'w', encoding='utf-8') as f:
        json.dump(dev_data, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_dir, f'{base_name}_test.json'), 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)


json_files = ['seventh.json']
output_directory = 'output_split'


os.makedirs(output_directory, exist_ok=True)


for json_file in json_files:
    split_data(json_file, output_directory)

print("数据集拆分完成。")
