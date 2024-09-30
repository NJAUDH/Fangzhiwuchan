import pandas as pd

df = pd.read_csv('entityDetail.csv')
description_df = df[['id', 'annotated_description']].drop_duplicates()  # 提取并去重
description_df.to_csv('description.csv', index=False)
print("description.csv 文件已生成")
df['position'] = df.apply(lambda row: f"[{row['start_pos']},{row['end_pos']}]", axis=1)  # 生成position列
df.to_csv('depth_file.csv', index=False)
print("depth_file.csv 文件已生成")
relations = []


for id_val, group in df.groupby('id'):
    pro_entities = group[group['entity_type'] == 'PRO']
    for idx_pro, pro_row in pro_entities.iterrows():
        for idx_other, other_row in group[group['entity_type'] != 'PRO'].iterrows():
            relation = f"{other_row['entity_type']}-PRO"
            source = other_row['entity_name']
            target = pro_row['entity_name']
            source_start = other_row['start_pos']
            source_end = other_row['end_pos']
            target_start = pro_row['start_pos']
            target_end = pro_row['end_pos']
            source_pos = f"[{source_start},{source_end}]"
            target_pos = f"[{target_start},{target_end}]"
            whole_position = f"[{source_pos}, {target_pos}]"

            relations.append({
                'ID': id_val,
                'relation': relation,
                'source': source,
                'target': target,
                'source_start': source_start,
                'source_end': source_end,
                'target_start': target_start,
                'target_end': target_end,
                'source_pos': source_pos,
                'target_pos': target_pos,
                'whole_position': whole_position
            })

modified_first_extended_file_df = pd.DataFrame(relations)
modified_first_extended_file_df.to_csv('modified_first_extended_file.csv', index=False)
print("modified_first_extended_file.csv 文件已生成")

nodepth_pro_final_quartile_df = modified_first_extended_file_df[
    ['ID', 'relation', 'source', 'target']].drop_duplicates()
nodepth_pro_final_quartile_df.to_csv('nodepth_pro_final_quartile.csv', index=False)
print("nodepth_pro_final_quartile.csv 文件已生成")
