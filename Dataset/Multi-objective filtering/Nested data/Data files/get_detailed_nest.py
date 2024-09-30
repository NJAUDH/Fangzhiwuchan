import pandas as pd
from itertools import combinations


df = pd.read_csv('updated_depth.csv')
results = []

for id, group in df.groupby('id'):
    group = group.sort_values(by='start')
    entities = group[['entity_name', 'entity_type', 'start', 'end', 'entity_id']].values.tolist()

    for i, (name1, type1, start1, end1, id1) in enumerate(entities):
        nested_entities = []
        for name2, type2, start2, end2, id2 in entities[i + 1:]:
            if start1 <= start2 and end1 >= end2:
                nested_entities.append((name2, type2, id2))

        if nested_entities:
            for entity in nested_entities:
                results.append([id, name1, type1, id1, entity[0], entity[1], entity[2]])
            for combo in combinations(nested_entities, 2):
                results.append([id, combo[0][0], combo[0][1], combo[0][2], combo[1][0], combo[1][1], combo[1][2]])

nested_df = pd.DataFrame(results, columns=['id', 'entity_name1', 'entity_type1', 'entity_name_id1', 'entity_name2',
                                           'entity_type2', 'entity_name_id2'])
nested_df.drop_duplicates(inplace=True)
nested_df.to_csv('nested_entities.csv', index=False)

for entity_type, group in df.groupby('entity_type'):
    group.to_csv(f'entities_{entity_type}.csv', index=False, columns=['id', 'entity_name', 'entity_type', 'entity_id'])

nested_df = nested_df.drop_duplicates()
nested_df['relation_id'] = nested_df.groupby(
    ['id', 'entity_name1', 'entity_type1', 'entity_name2', 'entity_type2']).ngroup()


nested_df.to_csv('nested_entities_with_relations.csv', index=False)


for entity_type, group in nested_df.groupby('entity_type1'):
    group.to_csv(f'nested_entities_{entity_type}.csv', index=False,
                 columns=['id', 'entity_name1', 'entity_type1', 'entity_name_id1', 'entity_name2', 'entity_type2',
                          'entity_name_id2', 'relation_id'])
