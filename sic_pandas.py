'''
An example of how to load in the data
scraped from the SIC website.

Crawl data using this command on the command line:
"scrapy crawl sic_manual -o sic_manual_nested.json"
'''

import json
import pandas as pd

data = []
with open('sic_manual_nested.jl') as f:
    for line in f:
        data.append(json.loads(line))

industries = [data[i]['data'] for i in range(len(data)) if data[i]['level']=='industry']
divisions = [data[i]['data'] for i in range(len(data)) if data[i]['level']=='division']
majors = [data[i]['data'] for i in range(len(data)) if data[i]['level']=='major']

sic = pd.DataFrame(industries)
d = pd.DataFrame(divisions)
m = pd.DataFrame(majors)
