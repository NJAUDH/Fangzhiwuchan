import pandas as pd
from tqdm import tqdm
from itertools import combinations
import multiprocessing as mp

df = pd.read_csv('hanbiaozhu_zw.csv')
unique_entities = df[['id', 'entity_name']].drop_duplicates()


unique_entities = unique_entities.merge(df[['entity_name', 'entity_type']], on='entity_name')
unique_entities = unique_entities.drop_duplicates(subset=['id', 'entity_name','entity_type'])

unique_entities['word_id'] = unique_entities.index + 1


for entity_type, group in tqdm(unique_entities.groupby('entity_type'), desc='Creating CSV files by entity_type'):
    entity_type_str = str(entity_type)
    group.to_csv(f'{entity_type_str}.csv', index=False)
    tqdm.write(f'Written to {entity_type_str}.csv')


relation_data = []


entity_word_id_map = unique_entities.set_index('entity_name')['word_id'].to_dict()


for sentence_id, group in tqdm(df.groupby('id'), desc='Processing sentences', total=df['id'].nunique()):
    entities = group[['entity_name', 'entity_type']]
    for entity1, entity2 in combinations(entities.itertuples(index=False), 2):
        relation_data.append({
            'sentence_id': sentence_id,
            'entity_name1': entity1.entity_name,
            'entity_type1': entity1.entity_type,
            'entity_id1': entity_word_id_map[entity1.entity_name],  # 使用缓存的word_id
            'entity_name2': entity2.entity_name,
            'entity_type2': entity2.entity_type,
            'entity_id2': entity_word_id_map[entity2.entity_name],  # 使用缓存的word_id
            'relation_id': len(relation_data) + 1,  # 关系ID自增
            'relation_name': f'{entity1.entity_name}-{entity2.entity_name}',
        })

relation_df = pd.DataFrame(relation_data)

def write_relation_to_csv(entity_type, group):
    filename = f'relations_{entity_type}.csv'
    group.to_csv(filename, index=False)
    print(f'Written to {filename}')

with mp.Pool(mp.cpu_count()) as pool:
    pool.starmap(write_relation_to_csv, relation_df.groupby('entity_type1'))














# import pandas as pd
# from tqdm import tqdm
# from itertools import combinations

# # 其他导入和代码保持不变

# # 读取CSV文件
# df = pd.read_csv('hanbiaozhu_zw.csv')

# # 去除重复的id和entity_name
# unique_entities = df[['id', 'entity_name']].drop_duplicates()

# # 提取唯一的entity_name和entity_type，并分配word_id
# unique_entities = unique_entities.merge(df[['entity_name', 'entity_type']], on='entity_name')
# unique_entities['word_id'] = unique_entities.index + 1

# # 为每个entity_type创建CSV文件，并添加进度条
# for entity_type, group in tqdm(unique_entities.groupby('entity_type'), desc='Creating CSV files by entity_type'):
#     # 确保entity_type是字符串，以防它是其他类型
#     entity_type_str = str(entity_type)
#     group.to_csv(f'{entity_type_str}.csv', index=False)
#     tqdm.write(f'Written to {entity_type_str}.csv')  # 输出写入的文件名，以便跟踪进度
# # 初始化存储关系的数据框
# relation_data = []


# # 遍历每个sentence_id，获取对应的entity_name组合，并添加进度条
# for sentence_id, group in tqdm(df.groupby('id'), desc='Processing sentences', total=df['id'].nunique()):
#     entities = group[['entity_name', 'entity_type']]
#     # 由于combinations生成的组合数量是固定的，这里不使用tqdm
#     for entity1, entity2 in combinations(entities.itertuples(index=False), 2):
#         relation_data.append({
#             'sentence_id': sentence_id,
#             'entity_name1': entity1.entity_name,
#             'entity_type1': entity1.entity_type,
#             # 确保word_id正确获取，需要先筛选出entity_name匹配的行
#             'entity_id1': unique_entities.loc[unique_entities['entity_name'] == entity1.entity_name, 'word_id'].iloc[0],
#             'entity_name2': entity2.entity_name,
#             'entity_type2': entity2.entity_type,
#             'entity_id2': unique_entities.loc[unique_entities['entity_name'] == entity2.entity_name, 'word_id'].iloc[0],
#             'relation_id': len(relation_data) + 1,  # 关系ID自增
#             'relation_name': f'{entity1.entity_name}-{entity2.entity_name}',
#             # 假设一个关系类型
#         })

# # 创建关系数据框
# relation_df = pd.DataFrame(relation_data)

# # 按照entity_type1分类写入不同的CSV文件，并添加进度条
# for entity_type, group in tqdm(relation_df.groupby('entity_type1'), desc='Writing relations to separate CSV files'):
#     filename = f'relations_{entity_type}.csv'
#     group.to_csv(filename, index=False)
#     tqdm.write(f'Written to {filename}')  # 输出写入的文件名，以便跟踪进度
#