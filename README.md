
### Challenge of the [2018 Wikidata Hackathon Zurich](https://www.wikidata.org/wiki/Wikidata:Events/Wikidata_Zurich_Hackathon): "Visualizing Data on Wikidata"

1. Get data out of Wikidata

```sparql
SELECT ?muni ?muniLabel ?district ?districtLabel (COUNT(DISTINCT ?p) as ?properties) (COUNT(?o) as ?statements) ?population
WHERE 
{
  ?muni wdt:P771 ?municode ;
        wdt:P31/wdt:P279* wd:Q486972 ;
        wdt:P131 wd:Q11943 ;
        ?p ?o .
  MINUS { ?muni rdfs:label ?o }
  OPTIONAL { ?muni wdt:P1082 ?population }
  OPTIONAL { ?muni wdt:P131 ?district.
            ?district p:P31 ?statement .
            ?statement ps:P31 wd:Q15644465 . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
GROUP BY ?muni ?muniLabel ?population ?district ?districtLabel
ORDER BY DESC(?properties)
```

[http://tinyurl.com/ybsttdr2](http://tinyurl.com/ybsttdr2)

2. Manually add the district of Zurich to the city of Zurich

before: `http://www.wikidata.org/entity/Q72,Zürich,,,171,2488,415682`

after: `http://www.wikidata.org/entity/Q72,Zürich,http://www.wikidata.org/entity/Q660732,Zurich District,171,2488,415682`

3. Convert the CSV to JSON

```python
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
        m['statements'] = row['statements']
        m['properties'] = row['properties']
        m['population'] = row['population']
        o['children'].append(m)

with open('data.json', 'w') as outfile:
    json.dump(t, outfile, ensure_ascii=False)
```

4. Adjust the D3.js Treemap example

before: [https://bl.ocks.org/mbostock/4063582](https://bl.ocks.org/mbostock/4063582)

after: [https://birk.github.io/wikidatazhhack-challenge4/](https://birk.github.io/wikidatazhhack-challenge4/)


