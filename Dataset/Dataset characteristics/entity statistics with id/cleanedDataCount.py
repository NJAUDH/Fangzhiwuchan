import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def merge_excel_files(excel_folder, files):
    all_data = pd.DataFrame()
    for file in files:
        file_path = os.path.join(excel_folder, file)
        df = pd.read_excel(file_path)
        df['source_file'] = os.path.splitext(file)[0]
        all_data = pd.concat([all_data, df], ignore_index=True)
    return all_data


def process_and_split_data(all_data):
    all_data = all_data.sort_values(by='entity_name.xlsx', key=lambda x: x.str.len(), ascending=False)
    to_keep = []
    for entity in all_data['entity_name.xlsx']:
        if not any(entity in kept for kept in to_keep):
            to_keep.append(entity)
    filtered_data = all_data[all_data['entity_name.xlsx'].isin(to_keep)]
    split_data = {file: filtered_data[filtered_data['source_file'] == file].drop(columns=['source_file'])
                  for file in filtered_data['source_file'].unique()}
    return split_data


def process_single_file(file_path):
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    cleaned_data = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = df[df['entity_name.xlsx'].str[0] == '[']
        cleaned_data[sheet_name] = df

def process_multiple_files(excel_folder, files):
    all_cleaned_data = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_single_file, os.path.join(excel_folder, file)): file for file in files}
        for future in tqdm(futures, desc="Processing files"):
            all_cleaned_data[futures[future]] = future.result()
    return all_cleaned_data


def write_to_excel(excel_path, split_data):
    with pd.ExcelWriter(excel_path, mode='w', engine='openpyxl') as writer:
        for sheet_name, data in split_data.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"文件已保存到 '{excel_path}'")


def main():
    excel_folder = 'excel_files'
    files = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]


    all_data = merge_excel_files(excel_folder, files)


    split_data = process_and_split_data(all_data)


    cleaned_data = process_multiple_files(excel_folder, files)


    output_excel_path = 'processed_entity_data.xlsx'
    write_to_excel(output_excel_path, split_data)


if __name__ == "__main__":
    main()
