import pandas as pd
import json

df = pd.read_csv('result.csv')
df.fillna(0, inplace=True)

t = dict()
t['name'] = 'top'
t['children'] = []
for d in df.districtLabel.unique():
    o = dict()
    o['name'] = d
    o['statements'] = 0
    o['properties'] = 0
    o['population'] = 0
    o['children'] = []
    t['children'].append(o)
    for idx, row in df[df.districtLabel == d].iterrows():
        m = dict()
        m['name'] = row['muniLabel']
        m['statements'] = row['object']
        m['properties'] = row['properties']
        m['population'] = row['population']
        o['children'].append(m)

with open('data.json', 'w') as outfile:
    json.dump(t, outfile, ensure_ascii=False)
