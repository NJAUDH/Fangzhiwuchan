import pandas as pd
from zhconv import convert

df = pd.read_csv('jt_corrected5.csv')

df['old_bin_description'] = df['old_bin_description'].apply(lambda x: convert(x, 'zh-hans'))
df['new_description'] = df['new_description'].apply(lambda x: convert(x, 'zh-hans'))

df.to_csv('jt_corrected5.csv', index=False)

print("繁体到简体转换完成，已保存至 converted_output.csv")
