from collections import defaultdict
from sklearn.metrics import precision_recall_fscore_support
from collections import defaultdict

def parse_ner_file(file_path):
    ner_data = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                identity, ner_str = line.split(': ner：', 1)
                entities = ner_str.strip().split('),')
                for entity in entities:
                    if entity.endswith(')'):
                        entity = entity[:-1]
                    parts = entity.split(',')

                    if len(parts) == 5:
                        ner_data[identity.strip()].append({
                            'position': parts[0].strip() + parts[1].strip(),
                            'entity': parts[2].strip(),
                            'type': parts[3].strip()

                        })
    return ner_data

def extract_positions(ner_data):
    extracted_data = defaultdict(list)
    for identity, entities in ner_data.items():
        for entity in entities:
            extracted_data[identity].append((entity['position'], entity['entity']))
    return extracted_data

def calculate_accuracy(pred_positions, true_positions):
    correct = 0
    total = 0

    for identity in true_positions:
        true_set = set(true_positions[identity])
        pred_set = set(pred_positions.get(identity, []))

        correct += len(true_set & pred_set)
        total += len(true_set)

    accuracy = correct / total if total > 0 else 0
    return accuracy

def parse_ner_file(file_path):
    ner_data = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                identity, ner_str = line.split(': ner：',1)
                entities = ner_str.strip().split('),')
                for entity in entities:
                    if entity.endswith(')'):
                        entity = entity[:-1]
                    parts = entity.split(',')

                    if len(parts) == 5:
                     ner_data[identity.strip()].append({
                        'position': parts[0].strip()+ parts[1].strip(),
                        'entity': parts[2].strip(),
                        'type': parts[3].strip()
                    })


    return ner_data

def extract_entities(ner_data):
    extracted_data = defaultdict(list)
    for identity, entities in ner_data.items():
        for entity in entities:
            extracted_data[identity].append((entity['entity'], entity['type']))
    return extracted_data

def extract_positions(ner_data):
    extracted_data = defaultdict(list)
    for identity, entities in ner_data.items():
        for entity in entities:
            extracted_data[identity].append((entity['position'], entity['type']))
    return extracted_data

def calculate_metrics_1(pred_data, true_data, entity_types):
    all_results = defaultdict(dict)
    for entity_type in entity_types:
        pred_entities = []
        true_entities = []

        for identity in true_data:
            true_entities.extend([e for e in true_data[identity] if e[1] == entity_type])
            pred_entities.extend([e for e in pred_data.get(identity, []) if e[1] == entity_type])



        true_set = set(true_entities)
        pred_set = set(pred_entities)

        correct = true_set & pred_set
        extra = pred_set - true_set
        missing = true_set - pred_set

        tp = len(true_set & pred_set)
        fp = len(pred_set - true_set)
        fn = len(true_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0



        all_results[entity_type] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'correct_count': len(correct),
            'extra_count': len(extra),
            'missing_count': len(missing)
        }

    return all_results


def calculate_metrics_2(pred_data, true_data, relation_types):
    all_results = defaultdict(dict)

    y_true_all = []
    y_pred_all = []

    precision_macro = []
    recall_macro = []
    f1_macro = []

    for relation_type in relation_types:
        pred_relations = []
        true_relations = []

        for identity in true_data:
            true_relations.extend([r for r in true_data[identity] if r[0] == relation_type])
            pred_relations.extend([r for r in pred_data.get(identity, []) if r[0] == relation_type])

        true_set = set(true_relations)
        pred_set = set(pred_relations)

        tp = len(true_set & pred_set)
        fp = len(pred_set - true_set)
        fn = len(true_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        # 累积所有的预测和真实标签，用于后续计算micro平均
        y_true_all.extend([1] * tp + [1] * fn + [0] * fp)
        y_pred_all.extend([1] * tp + [0] * fn + [1] * fp)

        precision_macro.append(precision)
        recall_macro.append(recall)
        f1_macro.append(f1)

        all_results[relation_type] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'correct_count': tp,
            'extra_count': fp,
            'missing_count': fn
        }

    # 计算micro平均
    micro_precision, micro_recall, micro_f1, _ = precision_recall_fscore_support(
        y_true_all, y_pred_all, average='binary'
    )

    # 计算macro平均
    macro_precision = sum(precision_macro) / len(precision_macro)
    macro_recall = sum(recall_macro) / len(recall_macro)
    macro_f1 = sum(f1_macro) / len(f1_macro)

    overall_results = {
        'micro_precision': micro_precision,
        'micro_recall': micro_recall,
        'micro_f1': micro_f1,
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'macro_f1': macro_f1
    }

    return all_results, overall_results

def calculate_metrics_all(true_sets, pred_sets):
    tp, fp, fn = 0, 0, 0

    true_relations=[]
    pred_relations=[]
    for identity in true_sets:
        true_relations.extend([r for r in true_sets[identity]])
        pred_relations.extend([r for r in pred_sets.get(identity, [])])

  #  for true_relation, pred_relation in zip(true_relations, pred_relations):

        # print(true_relation)
        # print(pred_relation)


    true_set = set(true_relations)
    pred_set = set(pred_relations)


    tp += len(true_set & pred_set)
    fp += len(pred_set - true_set)
    fn += len(true_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0


    return precision, recall, f1



def main():
    pred_file_path = 'data/8_11_ner.txt'
    true_file_path = 'data/8_ner_true.txt'

    entity_types = ['LOC', 'PRO', 'PER', 'TIM', 'BOK']

    pred_data = parse_ner_file(pred_file_path)
    true_data = parse_ner_file(true_file_path)

    pred_entities = extract_entities(pred_data)
    true_entities = extract_entities(true_data)
    pred_positions = extract_positions(pred_data)
    true_positions = extract_positions(true_data)


    entity_results = calculate_metrics_1(pred_entities, true_entities, entity_types)
    entity_pos_results = calculate_metrics_1(pred_positions, true_positions,entity_types)

    all_precision,all_recall,all_f1=calculate_metrics_all(pred_entities,true_entities)
    all_pos_precision, all_pos_recall, all_pos_f1 = calculate_metrics_all(pred_positions, true_positions)


    print("Entity Type Results:")
    for entity_type, metrics in entity_results.items():
        print(f"Entity Type: {entity_type}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  Correct: {metrics['correct_count']}")
        print(f"  Extra: {metrics['extra_count']}")
        print(f"  Missing: {metrics['missing_count']}")
        print()
    print(f"Precision:{all_precision}")
    print(f"Recall:{all_recall}")
    print(f"F1:{all_f1}")

    print("Position Type Results:")
    for entity_type, metrics in entity_pos_results.items():
        print(f"Entity Type: {entity_type}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  Correct: {metrics['correct_count']}")
        print(f"  Extra: {metrics['extra_count']}")
        print(f"  Missing: {metrics['missing_count']}")
        print()
    print(f"Precision:{all_pos_precision}")
    print(f"Recall:{all_pos_recall}")
    print(f"F1:{all_pos_f1}")




if __name__ == "__main__":
    main()
