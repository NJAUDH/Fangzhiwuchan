import json
import re
from sklearn.metrics import precision_score, recall_score, f1_score


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def parse_model_output(content):
    entries = content.strip().split("identity_")
    parsed_data = []
    for entry in entries[1:]:
        entry_id, assistant_value = entry.split(":", 1)
        assistant_value = assistant_value.strip()
        if "共现关系：" not in assistant_value:
            if "共现关系" in assistant_value:
                assistant_value +="：None;\n"
            else:
                assistant_value += "\n共现关系：None;\n"
        if "别名关系：" not in assistant_value:
            if "别名关系" in assistant_value:
                assistant_value += "：None;"
            elif "别名" in assistant_value:
                assistant_value+="关系：None;"

            else:
                if assistant_value[-1]=='\n':
                    assistant_value+="别名关系：None;"
                else:
                    assistant_value += "\n别名关系：None;"
        cleaned_entry = {"id": "identity_" + entry_id.strip()}
        conversations = [
            {"from": "assistant", "value": assistant_value}
        ]
        cleaned_entry["conversations"] = conversations
        parsed_data.append(cleaned_entry)
    return parsed_data


def clean_data(all_data):

    for data in all_data:

        assistant_value = data['conversations'][0]['value']

        ner,relation,word=assistant_value.split("\n",3)


        if ner.count('(') != ner.count(')'):
            p=len(ner)-1
            while(ner[p]!=")")and p>0:
                p-=1
            ner=ner[:p+1]+";"
        if relation.count("{") !=relation.count("}"):

            p=len(relation)-1
            while(relation[p]!="}" and relation[p]!="：")and p>0:
                p-=1
            relation=relation[:p+1]+";"
        newdata = "\n".join([ner, relation, word])

        data['conversations'][0]['value']=newdata

    return all_data


import re


def extract_labels(cleaned_data, true_data):
    ner_pos_true, ner_pos_pred = [], []
    ner_name_true, ner_name_pred = [], []
    ner_depth_true,ner_depth_pred=[],[]
    cooccurrence_true, cooccurrence_pred = [], []
    alias_true, alias_pred = [], []
    true_dict = {item['id']: item for item in true_data}

    for item in cleaned_data:
        item_id = item['id']
        if item_id in true_dict:
            true_item = true_dict[item_id]
            true_value = true_item['conversations'][1]['value']



            ner_name_true.append(set(re.findall(r'\(\[\d+,\s\d+\],([^,]+),([^\)]+)\)', true_value)))
            ner_pos_true.append(set(re.findall(r'\(\[(\d+,\s\d+)\],([^\)]+)\)', true_value)))
            ner_depth_true.append(set(re.findall(r'\(\[\d+,\s\d+\],([^,]+),([^\)]+)\)', true_value)))


            cooccurrence_true.append(set(re.findall(r"'position':\s*'\['\[(\d+),\s*(\d+)\]',\s*'\[(\d+),\s*(\d+)\]'\]',\s*'relation':\s*'([^']*)'", true_value)))


            alias_true.append(set(re.findall(r'\[([^\]]*)\]', true_value)))

            assistant_value = item['conversations'][0]['value']


            ner_name_pred.append(set(re.findall(r'\(\[\d+,\s\d+\],([^,]+),([^\)]+)\)', assistant_value)))
            ner_pos_pred.append(set(re.findall(r'\(\[(\d+,\s\d+)\],([^\)]+)\)', assistant_value)))
            ner_depth_pred.append(set(re.findall(r'\(\[\d+,\s\d+\],([^,]+),([^\)]+)\)', assistant_value)))


            cooccurrence_pred.append(set(re.findall(r"'position':\s*'\['\[(\d+),\s*(\d+)\]',\s*'\[(\d+),\s*(\d+)\]'\]',\s*'relation':\s*'([^']*)'", assistant_value)))

            alias_pred.append(set(re.findall(r'\[([^\]]*)\]', assistant_value)))



    return ner_name_true, ner_name_pred, ner_pos_true, ner_pos_pred, cooccurrence_true, cooccurrence_pred, alias_true, alias_pred


def calculate_metrics(true_sets, pred_sets):
    tp, fp, fn = 0, 0, 0
    true = []
    pred = []
    for true_set in true_sets:
        true.append(tuple(true_set))
    for pred_set in pred_sets:
        pred.append(tuple(pred_set))

    true = set(true)
    pred = set(pred)



    tp += len(true & pred)
    fp += len(pred - true)
    fn += len(true - pred)


    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1


def calculate_micro_macro_metrics(true_sets, pred_sets):
    all_tp, all_fp, all_fn = 0, 0, 0
    precisions, recalls, f1s = [], [], []
    count = 0
    for true_set, pred_set in zip(true_sets, pred_sets):
        true = []
        pred = []
        for true_se in true_set:
            true.append(tuple(true_se))
        for pred_se in pred_set:
            pred.append(tuple(pred_se))
        true = set(true)
        pred = set(pred)

        tp = len(true & pred)
        fp = len(pred - true)
        fn = len(true - pred)

        all_tp += tp
        all_fp += fp
        all_fn += fn

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

    precision_micro = all_tp / (all_tp + all_fp) if (all_tp + all_fp) > 0 else 0
    recall_micro = all_tp / (all_tp + all_fn) if (all_tp + all_fn) > 0 else 0
    f1_micro = 2 * (precision_micro * recall_micro) / (precision_micro + recall_micro) if (
                                                                                                      precision_micro + recall_micro) > 0 else 0

    precision_macro = sum(precisions) / len(precisions) if precisions else 0
    recall_macro = sum(recalls) / len(recalls) if recalls else 0
    f1_macro = sum(f1s) / len(f1s) if f1s else 0

    return {
        'precision_micro': precision_micro,
        'recall_micro': recall_micro,
        'f1_micro': f1_micro,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'f1_macro': f1_macro
    }



def count_missing_extra_predictions(true_sets, pred_sets):
    missing_counts, extra_counts, total_counts = 0, 0, 0

    for true_set, pred_set in zip(true_sets, pred_sets):
        missing_counts += len(true_set - pred_set)
        extra_counts += len(pred_set - true_set)
        total_counts += len(true_set)

    missing_ratio = f"{missing_counts}/{total_counts}" if total_counts > 0 else "0/0"

    return missing_counts, extra_counts, total_counts, missing_ratio


def count_missing_extra_predictions_type(true_sets, pred_sets):

    missing = true_sets - pred_sets
    extra = pred_sets - true_sets

    total_counts = len(true_sets.union(pred_sets))

    missing_counts = len(missing)
    extra_counts = len(extra)

    missing_ratio = f"{missing_counts}/{total_counts}" if total_counts > 0 else "0/0"

    return missing_counts, extra_counts, total_counts, missing_ratio


def convert_to_dict(relations_list, relation_types):
    relations_dict = {relation_type: [] for relation_type in relation_types}
    for relations in relations_list:
        for entities, relation_type in relations:
            if relation_type in relation_types:
                relations_dict[relation_type].append(tuple(entities.split(',')))

    return relations_dict
import hashlib

def hash_with_hashlib(*values):
    m = hashlib.sha256()
    for value in values:
        m.update(str(value).encode('utf-8'))
    return m.hexdigest()


def convert_to_dict_relation(relations_list, relation_types):

    relations_dict = {relation_type: [] for relation_type in relation_types}
    for relations in relations_list:
        for a,b,c,d,relation_type in relations:
            if relation_type in relation_types:
                relations_dict[relation_type].append(hash_with_hashlib(a, b, c, d))


    return relations_dict

def convert_to_dict_pos(relations_list, relation_types):
    relations_dict = {relation_type: [] for relation_type in relation_types}
    for relations in relations_list:
        for entities, relation_type in relations:
          if len(relation_type.split(","))>1:
            if relation_type.split(",")[1] in relation_types:
                relations_dict[relation_type.split(",")[1]].append(hash_with_hashlib(entities.split(",")[0],entities.split(",")[1])+relation_type.split(",")[0])
    return relations_dict

def calculate_and_print_metrics(ner_true, ner_pred,ner_pos_true,ner_pos_pred, relation_true, relation_pred):
    ner_types = ['LOC', 'PER', 'PRO', 'BOK', 'TIM']
    relation_types = ['LOC-PRO', 'PRO-TIM', 'PER-PRO', 'BOK-PRO']

    ner_true_dict = convert_to_dict(ner_true, ner_types)
    ner_pred_dict = convert_to_dict(ner_pred, ner_types)

    ner_pos_true=convert_to_dict_pos(ner_pos_true,ner_types)
    ner_pos_pred=convert_to_dict_pos(ner_pos_pred,ner_types)

    relation_true_dict = convert_to_dict_relation(relation_true, relation_types)
    relation_pred_dict = convert_to_dict_relation(relation_pred, relation_types)

    for ner_type in ner_types:
        true_set = set(ner_true_dict[ner_type])
        pred_set = set(ner_pred_dict[ner_type])

        precision, recall, f1 = calculate_metrics(true_set, pred_set)
        missing_counts, extra_counts, total_counts, missing_ratio = count_missing_extra_predictions_type(true_set,
                                                                                                         pred_set)

        print(
            f'NER NAME Type {ner_type}: Precision: {precision}, Recall: {recall}, F1: {f1}, Missing: {missing_ratio}, Extra: {extra_counts}')

    for ner_type in ner_types:
        true_set = set(ner_pos_true[ner_type])
        pred_set = set(ner_pos_pred[ner_type])

        precision, recall, f1 = calculate_metrics(true_set, pred_set)
        missing_counts, extra_counts, total_counts, missing_ratio = count_missing_extra_predictions_type(true_set,
                                                                                                         pred_set)

        print(
            f'NER POS Type {ner_type}: Precision: {precision}, Recall: {recall}, F1: {f1}, Missing: {missing_ratio}, Extra: {extra_counts}')


    for relation_type in relation_types:
        true_set = set(relation_true_dict[relation_type])
        pred_set = set(relation_pred_dict[relation_type])


        precision, recall, f1 = calculate_metrics(true_set, pred_set)

        missing_counts, extra_counts, total_counts, missing_ratio = count_missing_extra_predictions_type(true_set,
                                                                              pred_set)

        print(
            f'Relation Type {relation_type}: Precision: {precision}, Recall: {recall}, F1: {f1}, Missing: {missing_ratio}, Extra: {extra_counts}')




def main(model_output_file, true_data_file):
    model_output_content = read_file(model_output_file)
    with open(true_data_file, 'r', encoding='utf-8') as f:
        true_data = json.load(f)
    
    model_data = parse_model_output(model_output_content)
    cleaned_data = clean_data(model_data)
    
    ner_name_true, ner_name_pred, ner_pos_true, ner_pos_pred, cooccurrence_true, cooccurrence_pred, alias_true, alias_pred= extract_labels(cleaned_data, true_data)

    calculate_and_print_metrics(ner_name_true, ner_name_pred,ner_pos_true,ner_pos_pred, cooccurrence_true, cooccurrence_pred)



    ner_name_metrics = calculate_metrics(ner_name_true, ner_name_pred)
    ner_pos_metrics = calculate_metrics(ner_pos_true, ner_pos_pred)
    cooccurrence_name_metrics = calculate_metrics(cooccurrence_true, cooccurrence_pred)
  #  cooccurrence_pos_metrics = calculate_metrics(cooccurrence_pos_true, cooccurrence_pos_pred)
    alias_metrics = calculate_metrics(alias_true, alias_pred)

    ner_micro_macro_metrics = calculate_micro_macro_metrics(ner_name_true, ner_name_pred)
    ner_pos_micro_macro_metrics = calculate_micro_macro_metrics(ner_pos_true, ner_pos_pred)
    cooccurrence_name_micro_macro_metrics = calculate_micro_macro_metrics(cooccurrence_true,
                                                                          cooccurrence_pred)
 #   cooccurrence_pos_micro_macro_metrics = calculate_micro_macro_metrics(cooccurrence_pos_true, cooccurrence_pos_pred)
    alias_micro_macro_metrics = calculate_micro_macro_metrics(alias_true, alias_pred)

    ner_missing, ner_extra, ner_total, ner_missing_ratio = count_missing_extra_predictions(ner_name_true, ner_name_pred)
    cooccurrence_missing, cooccurrence_extra, cooccurrence_total, cooccurrence_missing_ratio = count_missing_extra_predictions(
        cooccurrence_true, cooccurrence_pred)
    alias_missing, alias_extra, alias_total, alias_missing_ratio = count_missing_extra_predictions(alias_true,
                                                                                                   alias_pred)

    print('NER Name Metrics: Precision:', ner_name_metrics[0], 'Recall:', ner_name_metrics[1], 'F1:',
          ner_name_metrics[2])
    print('NER Name Micro/Macro Metrics:', ner_micro_macro_metrics)

    print('NER Position Metrics: Precision:', ner_pos_metrics[0], 'Recall:', ner_pos_metrics[1], 'F1:',
          ner_pos_metrics[2])
    print('NER Position Micro/Macro Metrics:', ner_pos_micro_macro_metrics)

    print('NER Missing Predictions:', ner_missing_ratio)
    print('NER Extra Predictions:', ner_extra)

    print('Cooccurrence Name Metrics: Precision:', cooccurrence_name_metrics[0], 'Recall:',
          cooccurrence_name_metrics[1], 'F1:', cooccurrence_name_metrics[2])
    print('Cooccurrence Name Micro/Macro Metrics:', cooccurrence_name_micro_macro_metrics)
    #
    # print('Cooccurrence Position Metrics: Precision:', cooccurrence_pos_metrics[0], 'Recall:',
    #       cooccurrence_pos_metrics[1], 'F1:', cooccurrence_pos_metrics[2])
    # print('Cooccurrence Position Micro/Macro Metrics:', cooccurrence_pos_micro_macro_metrics)

    print('Cooccurrence Missing Predictions:', cooccurrence_missing_ratio)
    print('Cooccurrence Extra Predictions:', cooccurrence_extra)

    print('Alias Metrics: Precision:', alias_metrics[0], 'Recall:', alias_metrics[1], 'F1:', alias_metrics[2])
    print('Alias Micro/Macro Metrics:', alias_micro_macro_metrics)

    print('Alias Missing Predictions:', alias_missing_ratio)
    print('Alias Extra Predictions:', alias_extra)


