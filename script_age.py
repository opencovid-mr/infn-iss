import csv
import json
import requests
import pandas as pd


step_non_cons=[197,209,221,233,245,257,269,281,293,305]

step_cons=[201,213,225,237,249,261,273,285,297,309]

age_class=['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90+']

schema=zip(age_class,step_non_cons,step_cons)

variabile='sintomatici'

def scrape(regione,variabile,data):

	url='https://covid19.infn.it/iss/plots/iss_age_date_'+regione+'_'+variabile+'.div'
		
	s=requests.get(url).text

	t=s.split(' ')

	for step in schema:
		
		datasets_c=[]
		datasets_nc=[]	
		
		j_raw_nc='{"dummy":"'+t[step[1]].split('},')[0]+'}'
		date_nc=json.loads(j_raw_nc)['x']
		dati_nc=json.loads(j_raw_nc)['y']

		datasets_nc.append(date_nc)
		datasets_nc.append(dati_nc)

		df_nc = pd.DataFrame.from_records(zip(*datasets_nc), columns=['data', step[0]]).dropna()
		
		if step[0]!='90+': j_raw_c='{"dummy":"'+t[step[2]].split('},')[0]+'}'
		else: j_raw_c='{"dummy":"'+t[step[2]].split('},')[0][:-3]+'}'

		date_c=json.loads(j_raw_c)['x']
		dati_c=json.loads(j_raw_c)['y']

		datasets_c.append(date_c)
		datasets_c.append(dati_c)

		df_c = pd.DataFrame.from_records(zip(*datasets_c), columns=['data', step[0]]).dropna()

		result = df_c.append(df_nc).drop_duplicates(subset=['data'])

		print(result)

		if (step[0]=='0-9'): df_matrix = result
		else:
			df_matrix[step[0]] = df_matrix['data'].map(result.set_index('data')[step[0]])

	print(df_matrix)

	if regione=='italia': data=df_matrix['data'].iloc[-1]

	df_matrix.to_csv('./by_age/'+regione+'_'+variabile+'_'+data[:10]+'_byage.csv', index=False)
	df_matrix.to_csv('./by_age/'+regione+'_'+variabile+'_latest_byage.csv', index=False)

	return data

variabili=['positivi','sintomatici','ricoveri','terapia_intensiva','deceduti']

f=open('regioni.csv')
regioni2 = csv.reader(f)
data='dummy'
for reg in regioni2:
	print(reg[0])
	for variabile in variabili:
		data=scrape(reg[0],variabile,data)



