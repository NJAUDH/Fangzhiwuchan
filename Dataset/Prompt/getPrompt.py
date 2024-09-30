import pandas as pd
import json
from sklearn.model_selection import train_test_split

def read_csv(file_path):
    return pd.read_csv(file_path)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def split_data(data, test_size=0.3, random_state=42):
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
    return train_data, test_data

def generate_examples(df, example_count):
    if example_count == 0:
        return df
    elif example_count >= 1:
        examples = [
            "问题：本草云種出梁州故名梁有紅殻黑殻二種紅糯白黏皆可炊飯釀酒稍可縛帚莖可織箔席編籬供爨最為民利在諸梁中最為高大土人名曰高梁\n输出： ner：([0,1],本草,BOK,0),([5,6],梁州,LOC,0),([5,5],梁,PRO,1),([26,26],酒,PRO,0),([56,57],高梁,PRO,0);\n共现关系：{'position': '[[0,1], [5,5]]', 'relation': 'BOK-PRO','entity:'本草,梁'},{'position': '[[5,6], [5,5]]', 'relation': 'LOC-PRO','entity:'梁州,梁'},{'position': '[[0,1], [26,26]]', 'relation': 'BOK-PRO','entity:'本草,酒'},{'position': '[[5,6], [26,26]]', 'relation': 'LOC-PRO','entity:'梁州,酒'},{'position': '[[0,1], [56,57]]', 'relation': 'BOK-PRO','entity:'本草,高梁'},{'position': '[[5,6], [56,57]]', 'relation': 'LOC-PRO','entity:'梁州,高梁'};\n别名关系：None；"
        ]
        if example_count == 2:
            examples.append("问题：宋濂曰瓜產西域\n输出: ner：([0,1],宋濂,PER,0),([3,3],瓜,PRO,0),([5,6],西域,LOC,0);\n共现关系：{'position': '[[0,1], [3,3]]', 'relation': 'PER-PRO','entity:'宋濂,瓜'},{'position': '[[5,6], [3,3]]', 'relation': 'LOC-PRO','entity:'西域,瓜'};\n别名关系：None；")
        elif example_count == 3:
            examples.extend([
                "问题：出利川土人呼繡球白菜蓋菘類\n输出：ner：([1,2],利川,LOC,0),([6,9],繡球白菜,PRO,0),([6,7],繡球,PRO,1),([8,9],白菜,PRO,0),([11,11],菘,PRO,0);\n共现关系：{'position': '[[1,2], [6,9]]', 'relation': 'LOC-PRO','entity:'利川,繡球白菜'},{'position': '[[1,2], [6,7]]', 'relation': 'LOC-PRO','entity:'利川,繡球'},{'position': '[[1,2], [8,9]]', 'relation': 'LOC-PRO','entity:'利川,白菜'},{'position': '[[1,2], [11,11]]', 'relation': 'LOC-PRO','entity:'利川,菘'};\n别名关系：None；",
            ])
        df['examples'] = '例子: ' + ' '.join(examples)
    return df

def convert_csv_to_json(first_csv_path, pos_csv_path, extended_words_csv_path, description_csv_path, example_count):
    df = read_csv(first_csv_path)
    pos_df = read_csv(pos_csv_path)
    words_df = read_csv(extended_words_csv_path)
    description_df = read_csv(description_csv_path)

    unique_ids = df['ID'].unique()
    full_data = []

    for unique_id in unique_ids:
        sub_df = df[df['ID'] == unique_id]
        sub_pos_df = pos_df[pos_df['id'] == unique_id]
        sub_description_df = description_df[description_df['id'] == unique_id]

        sentence = sub_description_df.iloc[0]['annotated_description'] if not sub_description_df.empty else ''
        sentence = ''.join([char for char in sentence if '\u4e00' <= char <= '\u9fff'])

        question = (
            f"您是命名实体识别和抽取关系三元组的专家; "
            f"任务是对于给定的句子进行命名实体识别、抽取共现关系、抽取别名关系; "
            f"其中实体类型有:BOK,LOC,PER,PRO,TIM,JOB,ORG,MIS; "
            f"其中抽取共现关系,只抽取四种共现关系{{'BOK-PRO','LOC-PRO','PER-PRO','TIM-PRO','MIS-PRO','JOB-PRO','ORG-PRO'}}"
            f"输出格式为([start_pos, end_pos],entity_name,entity_type,depth),depth指的是嵌套实体识别中实体的深度"
            f"其中抽取别名关系,抽取PRO-PRO之间的别名关系,可能有超过两个的PRO为别名关系;"
            f"问题：{sentence}"
        )

        # Add examples if example_count > 0
        if example_count > 0:
            examples = [
                "举例问题1：本草云種出梁州故名梁有紅殻黑殻二種紅糯白黏皆可炊飯釀酒稍可縛帚莖可織箔席編籬供爨最為民利在諸梁中最為高大土人名曰高梁\n举例输出回答： ner：([0,1],本草,BOK,0),([5,6],梁州,LOC,0),([5,5],梁,PRO,1),([26,26],酒,PRO,0),([56,57],高梁,PRO,0);\n共现关系：{'position': '[[0,1], [5,5]]', 'relation': 'BOK-PRO','entity:'本草,梁'},{'position': '[[5,6], [5,5]]', 'relation': 'LOC-PRO','entity:'梁州,梁'},{'position': '[[0,1], [26,26]]', 'relation': 'BOK-PRO','entity:'本草,酒'},{'position': '[[5,6], [26,26]]', 'relation': 'LOC-PRO','entity:'梁州,酒'},{'position': '[[0,1], [56,57]]', 'relation': 'BOK-PRO','entity:'本草,高梁'},{'position': '[[5,6], [56,57]]', 'relation': 'LOC-PRO','entity:'梁州,高梁'};\n别名关系：None\n"
            ]
            if example_count == 2:
                examples.append("举例问题2：宋濂曰瓜產西域\n举例输出回答: ner：([0,1],宋濂,PER,0),([3,3],瓜,PRO,0),([5,6],西域,LOC,0);\n共现关系：{'position': '[[0,1], [3,3]]', 'relation': 'PER-PRO','entity:'宋濂,瓜'},{'position': '[[5,6], [3,3]]', 'relation': 'LOC-PRO','entity:'西域,瓜'};\n别名关系：None\n")
            elif example_count == 3:
                     examples.extend([
                    "举例问题3：出利川土人呼繡球白菜蓋菘類\n举例输出回答：ner：([1,2],利川,LOC,0),([6,9],繡球白菜,PRO,0),([6,7],繡球,PRO,1),([8,9],白菜,PRO,0),([11,11],菘,PRO,0);\n共现关系：{'position': '[[1,2], [6,9]]', 'relation': 'LOC-PRO','entity:'利川,繡球白菜'},{'position': '[[1,2], [6,7]]', 'relation': 'LOC-PRO','entity:'利川,繡球'},{'position': '[[1,2], [8,9]]', 'relation': 'LOC-PRO','entity:'利川,白菜'},{'position': '[[1,2], [11,11]]', 'relation': 'LOC-PRO','entity:'利川,菘'};\n别名关系：None\n",
                ])
            question += '接下去我将给你举一些例子：' + ' '.join(examples)
            question+=f" 你需要回答的问题是：{sentence}"
        try:
            entity_recognition = ','.join(
                [f"({row['position']},{row['entity_name']},{row['entity_type']},{row['depth']})" for _, row in sub_pos_df.iterrows()]
            )
        except IndexError:
            entity_recognition = None

        try:
            cooccurrence_relations = ','.join(
                [f"{{'position': '{row['whole_position']}', 'relation': '{row['relation']}','entity:'{row['source']},{row['target']}'}}" for _, row in sub_df.iterrows()]
            )
        except IndexError:
            cooccurrence_relations = None

        try:
            alias_relations = words_df[words_df['ID'] == unique_id]['Words_pos'].values[0]+','+words_df[words_df['ID'] == unique_id]['Words'].values[0]
        except IndexError:
            alias_relations = None

        triples_str = f"ner：{entity_recognition};\n共现关系：{cooccurrence_relations};\n别名关系：{alias_relations}；"

        conversation = {
            "id": f"identity_{unique_id}",
            "conversations": [
                {
                    "from": "user",
                    "value": question
                },
                {
                    "from": "assistant",
                    "value": triples_str
                }
            ]
        }

        full_data.append(conversation)

    return full_data

def process_all_datasets(first_csv_path, pos_csv_path, extended_words_csv_path, description_csv_path):
    for example_count in [0, 1, 2, 3]:
        data = convert_csv_to_json(first_csv_path, pos_csv_path, extended_words_csv_path, description_csv_path, example_count)

        full_output_file = f'dataset_{example_count}_examples.json'
        save_json(data, full_output_file)

        train_data, test_data = split_data(data)
        train_file = f'dataset_{example_count}_examples_train.json'
        test_file = f'dataset_{example_count}_examples_test.json'


        save_json(train_data, train_file)
        save_json(test_data, test_file)

        print(f'{example_count}个例子数据集已生成并拆分为训练集和测试集。')

