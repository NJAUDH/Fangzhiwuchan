from collections import defaultdict

def parse_word_file(file_path):
    word_data = defaultdict(dict)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                identity, alias_relation = line.split(': 别名关系：')
                if alias_relation.strip() == 'None;':
                    word_data[identity.strip()] = None
                else:
                    parts = alias_relation.strip().split('],')
                    positions = parts[0] + ']'
                    entities = parts[1].strip().split(',')
                    word_data[identity.strip()] = {
                        'positions': eval(positions),
                        'entities': [e[:-1].strip() for e in entities]
                    }
    return word_data

def classify_alias_relations(pred_data, true_data):
    results = {
        'not_processed': 0,
        'partially_processed': 0,
        'completely_correct': 0,
        'partially_all': 0,
        'partially_correct': 0,  # 添加部分正确计数
        'partially_details': [],
        'all_write': 0,
        'all_data': 0,
        'missing':0,
        'extra':0
    }

    for identity, true_relation in true_data.items():
        pred_relation = pred_data.get(identity, None)

        if true_relation is None or pred_relation is None:
            if true_relation is None and pred_relation is None:
                pass
            else:
                if pred_relation is None:
                    results['not_processed'] += 1
                    true_entities = set(true_relation['entities']) if true_relation else set()
                    results['all_data'] += len(true_entities)
        else:
            true_entities = set(true_relation['entities'])
            pred_entities = set(pred_relation['entities'])
            results['all_data'] += len(true_entities)
            if true_entities == pred_entities:
                results['all_write'] += len(true_entities)
                results['completely_correct'] += 1
            else:
                # 计算部分处理中正确的值
                correct = true_entities & pred_entities
                missing=true_entities-pred_entities
                extra=pred_entities-true_entities
                results['partially_all'] += len(true_entities)
                results['partially_correct'] += len(correct)

                results['all_write'] += len(correct)
                results['missing']+=len(missing)
                results['extra']+=len(extra)

                if correct:
                    results['partially_processed'] += 1
                    extra = pred_entities - true_entities
                    missing = true_entities - pred_entities
                    results['partially_details'].append({
                        'identity': identity,
                        'correct': list(correct),  # 添加正确详情
                        'extra': list(extra),
                        'missing': list(missing)
                    })
                else:
                    results['not_processed'] += 1

    # 计算Precision, Recall, F1
    precision = results['all_write'] / (results['all_write']+results['extra'])
    recall = results['all_write'] / (results['all_write']+results['missing']) if results['all_data'] > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    results['precision'] = precision
    results['recall'] = recall
    results['f1_score'] = f1_score

    return results

def main():
    pred_file_path = 'data/8_8_word.txt'
    true_file_path = 'data/8_word_true.txt'

    pred_data = parse_word_file(pred_file_path)
    true_data = parse_word_file(true_file_path)

    results = classify_alias_relations(pred_data, true_data)

    print("分类结果:")
    print(f"  完全正确的: {results['completely_correct']}")
    print(f"  没有处理出来的: {results['not_processed']}")
    print(f"  部分处理出来的: {results['partially_processed']}")

    print(f"  以实体为单位，正确数据/所有数据：{results['all_write']}/{results['all_data']}")

    print(f"\nPrecision: {results['precision']:.4f}")
    print(f"Recall: {results['recall']:.4f}")
    print(f"F1 Score: {results['f1_score']:.4f}")

    if results['partially_processed'] > 0:
        print("\n部分处理详情将被写入文件:")
        with open('partially_processed_details.txt', 'w', encoding='utf-8') as detail_file:
            detail_file.write("部分处理详情：\n")
            for detail in results['partially_details']:
                detail_file.write(f"Identity: {detail['identity']}\n")
                detail_file.write(f"  Correct: {detail['correct']}\n")  # 写入正确的详情
                detail_file.write(f"  Extra: {detail['extra']}\n")
                detail_file.write(f"  Missing: {detail['missing']}\n")
                detail_file.write("\n")  # 添加空行以分隔不同记录

        print(f"部分处理详情已写入到 'partially_processed_details.txt'")

if __name__ == "__main__":
    main()
