import pandas as pd


depth_df = pd.read_csv('entity_detail.csv')
extended_words_df = pd.read_csv('extended_words.csv')
same_merge_output_df = pd.read_csv('same_merge_output.csv')
two_description_df = pd.read_csv('description_id_cast.csv')


id_mapping = two_description_df[['old_id', 'new_id']].drop_duplicates()


same_merge_output_df = same_merge_output_df.merge(id_mapping, left_on='ID', right_on='old_id', how='left')
same_merge_output_df = same_merge_output_df[['new_id', 'Words']].dropna().rename(columns={'new_id': 'ID'})



def get_positions_with_words(entity_name, id_val, depth_df):
    entity_rows = depth_df[(depth_df['id'] == id_val) & (depth_df['entity_name'] == entity_name)]
    if not entity_rows.empty:
        return entity_rows[['start_pos', 'end_pos']].values[0]
    return None, None



filtered_extended_words = []
extended_words=[]
for index, row in same_merge_output_df.iterrows():
    words = row['Words'].split(', ')
    id_val = row['ID']

    valid_words = []
    valid_positions = []

    for word in words:
        start_pos, end_pos = get_positions_with_words(word, id_val, depth_df)
        if start_pos is not None and end_pos is not None:
            valid_words.append(word)
            valid_positions.append(f'[{start_pos}, {end_pos}]')


    if len(valid_words) >= 2:
        filtered_extended_words.append({
            'ID': id_val,
            'Words': ', '.join(valid_words),
            'Words_pos': str(valid_positions)
        })
        extended_words.append(
            {
                'ID': id_val,
                'Words': ', '.join(valid_words)
            }
        )


filtered_extended_words_df = pd.DataFrame(extended_words)

filtered_extended_words_df.to_csv('same_merge_output.csv', index=False)

print("新的 extended_words.csv 已生成")

