import re

import re


def parse_model_output(content, output_file):
    entries = content.strip().split("identity_")
    parsed_data = []
    problematic_count = 0
    lengths = []

    for entry in entries[1:]:
        entry_id, assistant_value = entry.split(":", 1)
        assistant_value = assistant_value.strip()


        if "共现关系：" not in assistant_value:
            problematic_count += 1
            lengths.append(len(assistant_value))
            if "共现关系" in assistant_value:
                assistant_value += "：None;\n"
            elif "共现" in assistant_value:
                assistant_value += "关系：None;\n"
            elif assistant_value[-1] == '共':
                assistant_value += "现关系：None;\n"
            else:
                assistant_value += "\n共现关系：None;\n"


        elif "别名关系：" not in assistant_value:
            problematic_count += 1
            lengths.append(len(assistant_value))
            if "别名关系" in assistant_value:
                assistant_value += "：None;"
            elif "别名" in assistant_value:
                assistant_value += "关系：None;"
            elif assistant_value[-1] == '别' and assistant_value[-2] == '\n':
                assistant_value += "名关系：None;"
            else:
                if assistant_value[-1] == '\n':
                    assistant_value += "别名关系：None;"
                else:
                    assistant_value += "\n别名关系：None;"

        assistant_value = re.sub(r'\n\s*\n', '\n', assistant_value)
        cleaned_entry = {"id": "identity_" + entry_id.strip()}
        conversations = [
            {"from": "assistant", "value": assistant_value}
        ]
        cleaned_entry["conversations"] = conversations
        parsed_data.append(cleaned_entry)


    if lengths:
        min_length = min(lengths)
        max_length = max(lengths)
        length_range = (min_length, max_length)
        length_count = {f"{i * 10}-{(i + 1) * 10}": 0 for i in range((max_length // 10) + 1)}

        for length in lengths:
            range_key = f"{(length // 10) * 10}-{(length // 10 + 1) * 10}"
            if range_key in length_count:
                length_count[range_key] += 1


    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"有问题的句子数量: {problematic_count}\n")
        f.write(f"总句子数量: {len(entries) - 1}\n")
        f.write(f"长度范围: {length_range[0]}-{length_range[1]}\n")
        for length, count in length_count.items():
            if count!=0:
             f.write(f"长度: {length} 计数: {count}\n")

    return parsed_data




def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


prefixes = ['bb_whole', 'dataset']


for i in range(4):
    model_output_file = f'{prefixes[0]}_{i}_result.txt'
    true_data_file = f'{prefixes[1]}_{i}_examples_test.json'


    content = read_file(model_output_file)
    parse_model_output(content, "whole_output.txt")
