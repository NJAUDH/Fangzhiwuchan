import pandas as pd

# 定义所有提供的CSV文件路径
files = [
    'relations_BOK.csv',
    'relations_JOB.csv',
    'relations_LOC.csv',
    'relations_MIS.csv',
    'relations_PER.csv',
    'relations_PRO.csv',
    'relations_ORG.csv',
    'relations_TIM.csv'
]

# 读取文件并提取每个文件中的 'entity_id1', 'entity_id2' 和 'relation_id' 列
dataframes = [pd.read_csv(file) for file in files]

# 将所有数据合并为一个DataFrame
combined_df = pd.concat([df[['entity_id1', 'entity_id2', 'relation_id']] for df in dataframes])

# 去除 relation_id 重复的记录，不考虑 entity_id1 和 entity_id2 的顺序
unique_pairs = combined_df.drop_duplicates(subset=['relation_id'])

# 对结果进行排序：先按 entity_id1 升序排列，再按 entity_id2 升序排列
sorted_unique_pairs_df = unique_pairs.sort_values(by=['entity_id1', 'entity_id2']).reset_index(drop=True)

# 将排序后的去重数据保存为新的CSV文件
output_file = 'sorted_unique_entity_pairs_relation_id_only.csv'
sorted_unique_pairs_df.to_csv(output_file, index=False)

print(f"新的CSV文件已生成: {output_file}")
