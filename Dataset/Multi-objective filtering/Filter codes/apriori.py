import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 读取CSV文件
file_path = 'sorted_unique_entity_pairs.csv'
df = pd.read_csv(file_path)

# 将每个entity_id1分组，并将对应的entity_id2作为事务项集
transactions = df.groupby('entity_id1')['entity_id2'].apply(list).tolist()

# 使用TransactionEncoder将事务集转换为one-hot编码
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# 使用Apriori算法，设置最小支持度为0.1
frequent_itemsets = apriori(df_encoded, min_support=0.006, use_colnames=True)

# 生成关联规则，基于Lift进行筛选
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.5)

# 输出频繁项集和关联规则
print("频繁项集：")
print(frequent_itemsets)

print("\n关联规则：")
print(rules)


frequent_itemsets.to_csv("frequent_itemsets006.csv", index=False)
rules.to_csv("association_rules006.csv", index=False)
