import csv
import json
import requests
import pandas as pd

f=open('regioni.csv')
regioni = csv.reader(f)

for regione in regioni:
	datasets_c=[]
	datasets_nc=[]

	url='https://covid19.infn.it/iss/plots/iss_bydate_'+regione[0]+'_ricoveri.div'

	s=requests.get(url).text

	t=s.split(' ')

	j_c='{"dummy":"'+t[196].strip()[:-54]
	date_cons=json.loads(j_c)['x']
	dati_cons=json.loads(j_c)['y']

	j_nc='{"dummy":"'+t[205].strip()[:-2]

	date_notcons=json.loads(j_nc)['x']
	dati_notcons=json.loads(j_nc)['y']

	datasets_nc.append(date_notcons)
	datasets_nc.append(dati_notcons)
	
	datasets_c.append(date_cons)
	datasets_c.append(dati_cons)

	df_nc = pd.DataFrame.from_records(zip(*datasets_nc), columns=['data', 'ricoveri']).dropna()

	df_c = pd.DataFrame.from_records(zip(*datasets_c), columns=['data','ricoveri']).dropna()

	result = df_c.append(df_nc).drop_duplicates(subset=['data'])

	if (regione[0]=='italia'): df_matrix = result
	else:
		df_matrix[regione[0]] = df_matrix['data'].map(result.set_index('data')['ricoveri'])
		df_matrix[regione[0]] = df_matrix[regione[0]].astype('Int64')

data=df_matrix['data'].iloc[-1]

df_matrix.to_csv('./ricoveri/ricoveri_italia_'+data[:10]+'.csv', index=False)
df_matrix.to_csv('./ricoveri/ricoveri_italia_latest.csv', index=False)
