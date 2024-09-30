import pandas as pd
import re


processed_data = pd.read_csv('final_output_cleaned-0.8.csv')
hanbiaozhu_weizhi = pd.read_csv('new_hanbiaozhu_weizhi.csv')

result = []

new_id_counter = 1

for old_id in processed_data['ID'].unique():
    entities = processed_data[processed_data['ID'] == old_id]['entity_name'].tolist()
    related_row = hanbiaozhu_weizhi[hanbiaozhu_weizhi['id'] == old_id]

    if not related_row.empty:
        bin_description = related_row['bin_description'].iloc[0]
        last_pos = 0

        for entity_name in entities:
            start_pos = bin_description.find(entity_name)
            if start_pos != -1:
                end_pos = start_pos + len(entity_name)
                split_pos = end_pos
                while split_pos < len(bin_description):
                    char = bin_description[split_pos]
                    if re.match(r'[\u4e00-\u9fa5]|\[', char):
                        break
                    split_pos += 1

                new_description = bin_description[last_pos:split_pos]
                result.append({
                    'old_id': old_id,
                    'new_id': new_id_counter,
                    'old_description': bin_description,
                    'new_description': new_description
                })

                last_pos = split_pos
                new_id_counter += 1

        if last_pos < len(bin_description):
            new_description = bin_description[last_pos:]
            result.append({
                'old_id': old_id,
                'new_id': new_id_counter,
                'old_description': bin_description,
                'new_description': new_description
            })
            new_id_counter += 1


result_df = pd.DataFrame(result)
result_df.to_csv('finalRelation.csv', index=False)

print("处理完成，结果已保存到 finalRelation.csv")
