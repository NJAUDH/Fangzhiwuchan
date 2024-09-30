import pandas as pd
from tqdm import tqdm

depth_df = pd.read_csv('ccc.csv')
filtered_df = pd.read_csv('aawhole.csv')

flat_df = filtered_df[filtered_df['depth'] == -1]
nested_df = filtered_df[filtered_df['depth'] ==0]

flat_df_2 = depth_df[depth_df['depth'] == -1]
nested_df_2 = depth_df[depth_df['depth']== 0]

def compute_group_stats(df):
    grouped = df.groupby('entity_type')
    count = grouped.size()
    print(df.columns)
    avg_length = grouped['entity_name'].apply(lambda x: x.str.len().mean())
    loc_ratio = grouped.apply(lambda x: (
        x['entity_zhushi'].str.contains('LOC').sum() / x['entity_zhushi'].notnull().sum() 
        if x['entity_zhushi'].notnull().sum() > 0 else 0
    ))
    result = pd.DataFrame({
        'count': count,
        'avg_length': avg_length,
        'loc_ratio': loc_ratio
    })
    return result


flat_stats = compute_group_stats(flat_df)
nested_stats = compute_group_stats(nested_df)

flat_stats_2 = compute_group_stats(flat_df_2)
nested_stats_2 = compute_group_stats(nested_df_2)

# 合并flat和nested数据
flat_stats['group'] = 'flat'
nested_stats['group'] = 'nested'

flat_stats_2['group'] = 'flat'
nested_stats_2['group'] = 'nested'


final_stats = pd.concat([flat_stats, nested_stats]).reset_index()

final_stats_2 = pd.concat([flat_stats_2, nested_stats_2]).reset_index()

final_stats.to_csv('pick.csv', index=False)

final_stats_2.to_csv('cc_whole.csv', index=False)


print("\nFinal Entity Type Group Stats:")
print(final_stats.head())

print("处理完成，文件保存为 entity_type_group_stats.csv")
