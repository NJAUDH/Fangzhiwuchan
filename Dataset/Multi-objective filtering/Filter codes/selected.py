import pandas as pd

# 读取文件
association_rules_df = pd.read_csv('association_rules006.csv')
frequent_itemsets_df = pd.read_csv('frequent_itemsets006.csv')
original_data_df = pd.read_csv('sorted_unique_entity_pairs.csv')

# 将频繁项集中的项集列转换为frozenset格式，方便后续比较
frequent_itemsets_df['itemsets'] = frequent_itemsets_df['itemsets'].apply(lambda x: frozenset(eval(x)))

# 生成一个包含频繁项集的集合，方便查找
frequent_itemsets = set(frequent_itemsets_df['itemsets'])


# 定义一个筛选函数，检查原始数据中的关系是否属于频繁项集
def filter_relation(row):
    # 将每一行的 entity_id2 转换为 frozenset
    relation_set = frozenset([row['entity_id2']])

    # 检查这个关系是否属于频繁项集
    return relation_set in frequent_itemsets


# 在原始数据集中应用筛选
filtered_df = original_data_df[original_data_df.apply(filter_relation, axis=1)]

# 保存筛选后的结果
filtered_df.to_csv('filtered_relations006.csv', index=False)

print("筛选完成，已将符合条件的关系保存到 filtered_relations.csv 文件中。")
