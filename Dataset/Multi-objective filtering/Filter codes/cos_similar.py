import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 加载Excel文件
file_path = 'depth_file.csv'  # 替换为你的文件路径
data = pd.read_csv(file_path)

# 2. 提取'id'和'bin_description'，并去重
unique_data = data[['id', 'bin_description']].drop_duplicates()

# 3. 计算'bin_description'的余弦相似度
tfidf_vectorizer = TfidfVectorizer().fit_transform(unique_data['bin_description'].fillna(''))
cosine_sim_matrix = cosine_similarity(tfidf_vectorizer)

# 4. 设定相似度阈值，并标记要删除的id
threshold = 0.8
rows_to_drop = set()

for i in range(len(cosine_sim_matrix)):
    for j in range(i + 1, len(cosine_sim_matrix)):
        if cosine_sim_matrix[i, j] > threshold:
            rows_to_drop.add(unique_data.iloc[j]['id'])

# 5. 从原始数据中删除这些id对应的行
data_cleaned = data[~data['id'].isin(rows_to_drop)]


# 6. 保存清理后的数据为新的Excel文件
output_file_path = 'final_output_cleaned-0.8.csv'  # 替换为你想保存的文件路径
data_cleaned.to_csv(output_file_path, index=False)

print(f"文件已成功保存为: {output_file_path}")
