from collections import defaultdict
from sklearn.metrics import precision_recall_fscore_support

def parse_relation_file(file_path):
    relation_data = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                identity, relation_str = line.split(': 共现关系：', 2)
                relation_str = relation_str.strip()

                relation_str = relation_str.replace("'", "\"")
                relation_entries = relation_str.split("},{")

                for entry in relation_entries:
                    entry = entry.replace("{", "").replace("}", "").strip()
                    parts = entry.split("\",")
                    if len(parts)==4:
                        position = parts[0].split(":")[1].strip() + parts[1]
                        relation = parts[2].split(":")[1].strip()
                        entities = parts[3]

                        relation_data[identity.strip()].append({
                            'relation': relation,
                            'entities': tuple(entities.split(',')),
                            'position': position
                        })

    return relation_data

def extract_relations(relation_data):
    extracted_data = defaultdict(list)
    for identity, relations in relation_data.items():
        for relation in relations:
            extracted_data[identity].append((relation['relation'], *relation['entities']))
    return extracted_data

def extract_positions(relation_data):
    extracted_data = defaultdict(list)
    for identity, relations in relation_data.items():
        for relation in relations:
            extracted_data[identity].append((relation['position'], relation['relation']))
    return extracted_data

def pad_sequences(seq1, seq2, fill_value):
    max_len = max(len(seq1), len(seq2))
    seq1.extend([1] * (max_len - len(seq1)))
    seq2.extend([0] * (max_len - len(seq2)))
    return seq1, seq2

def calculate_metrics(pred_data, true_data, relation_types, dtype):
    all_results = defaultdict(dict)
    if dtype=='entity':
     for relation_type in relation_types:
        pred_relations = []
        true_relations = []

        for identity in true_data:

            true_relations.extend([r for r in true_data[identity] if r[0] == relation_type])
            pred_relations.extend([r for r in pred_data.get(identity, []) if r[0] == relation_type])


        true_set = set(true_relations)
        pred_set = set(pred_relations)


        print(len(true_set),len(pred_set))
        tp = len(true_set & pred_set)
        fp = len(pred_set - true_set)
        fn = len(true_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        all_results[relation_type] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'correct_count': tp,
            'extra_count': fp,
            'missing_count': fn
        }
    else:
         for relation_type in relation_types:
             pred_relations = []
             true_relations = []

             for identity in true_data:
                 true_relations.extend([r for r in true_data[identity] if r[1] == relation_type])
                 pred_relations.extend([r for r in pred_data.get(identity, []) if r[1] == relation_type])
             true_set = set(true_relations)
             pred_set = set(pred_relations)

             tp = len(true_set & pred_set)
             fp = len(pred_set - true_set)
             fn = len(true_set - pred_set)

             precision = tp / (tp + fp) if (tp + fp) > 0 else 0
             recall = tp / (tp + fn) if (tp + fn) > 0 else 0
             f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

             all_results[relation_type] = {
                 'precision': precision,
                 'recall': recall,
                 'f1': f1,
                 'correct_count': tp,
                 'extra_count': fp,
                 'missing_count': fn
             }

    return all_results


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
    pred_file_path = '8_14_relation.txt'
    true_file_path = '8_14_relation_true_qc.txt'

    relation_types = ['"LOC-PRO', '"PER-PRO', '"PRO-TIM', '"BOK-PRO']


    pred_data = parse_relation_file(pred_file_path)
    true_data = parse_relation_file(true_file_path)


    pred_relations = extract_relations(pred_data)
    true_relations = extract_relations(true_data)
    pred_positions = extract_positions(pred_data)
    true_positions = extract_positions(true_data)

    relation_results = calculate_metrics(pred_relations, true_relations, relation_types,'entity')
    position_results = calculate_metrics(pred_positions, true_positions, relation_types,'pos')

    all_entity_precision,all_entity_recall,all_entity_f1=calculate_metrics_all(pred_relations,true_relations)
    all_position_precision, all_position_recall, all_position_f1 = calculate_metrics_all(pred_positions, true_positions)

    print("Relation Type Results:")
    for relation_type, metrics in relation_results.items():
        print(f"Relation Type: {relation_type}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  Correct: {metrics['correct_count']}")
        print(f"  Extra: {metrics['extra_count']}")
        print(f"  Missing: {metrics['missing_count']}")
        print()

    print("Position Results:")
    for relation_type, metrics in position_results.items():
        print(f"Relation Type: {relation_type}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  Correct: {metrics['correct_count']}")
        print(f"  Extra: {metrics['extra_count']}")
        print(f"  Missing: {metrics['missing_count']}")
        print()
    print( all_entity_precision,all_entity_recall,all_entity_f1)

    print( all_position_precision, all_position_recall, all_position_f1)
if __name__ == "__main__":
    main()
