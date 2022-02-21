import sys
import ssl
import csv
import json
import requests
import time
import datetime
import pandas as pd
import pymysql
from sqlalchemy import create_engine

#paramètres 

	#exemple JSON a transmettre
jsonDict = '' #{"key": "value"};

	#IP JSON à envoyer
ipBroadCast=''#'172.19.90.23';

	#IP MySQL server de données agregeant les données
ipMySQL='127.0.0.1';#ipMySQL='172.19.90.21';#accès distant test
loginMySQL='formation';
passMySQL='formation';
baseMySQL='iot';

	#paramétrage du formatage des datetime à la microseconde
datetimestring = '%Y-%m-%d %H:%M:%S.%f'	

#main

helpStr="""
SOAP API POST REST Producer 2-> Ingress # usage ->
#paramètres passés en arguments :
# [paramètre #1] (obligatoire) le prototype ou le topic ou métrique (exemple X46789)
# (paramètre #2) (facultatif) fréquence d'émission / sampling en ms millisecondes (exemple, défaut 100 ms)
# (paramètre #3) (facultatif) ingress hote à contacter hote (exemple, défault 172.19.90.17)
# (paramètre #4) (facultatif) ingress hote à contacter port (exemple, défaut 5000)
""";

#print (len(sys.argv))
if len(sys.argv)>=2 and len(sys.argv)<=5 :
	pass
else:
	print (helpStr)
	exit(1)

prototype=sys.argv[1];

try:
	freq=sys.argv[2];
except:
	freq=200
try:
	ipBroadCast=sys.argv[3];
except:
	ipBroadCast='172.19.90.17';
try:
	hostBroadPort=sys.argv[4];
except:
	hostBroadPort='5500'

#connexion MySQL
try:
	cnx = create_engine('mysql+pymysql://'+loginMySQL+':'+passMySQL+'@'+ipMySQL+'/'+baseMySQL)
	#, pool_recycle=3600)#optimisation pool connexions
except:
	print('Erreur de connexion, veuillez réessayer plus tard ou vérififer le serveur MySQL.');
	exit(-2)
		
#récupération des données du prototype passé en argeument 
try:
	#df = pd.read_sql('SELECT * FROM '+prototype+' order by dateHour asc', cnx) #version 0 dataframe resultat
	#paramètres : code du prototype 
	#puis détails true/false, 
	#le code model alias code dataset true/false
	#export du modèle xml true/false
	#nombre de lignes limité à nombre passé en paramètre ... -si 1 -> toutes les données
	df=pd.read_sql('call sp_trameIOT("'+prototype+'",true,true,false,-1);',cnx) 
except:	
	print('Prototype inexistant, veuillez au préalable en définit le modèle XML, assurez vous que la table éxiste.');
	exit(-3)
	


recordsJson = df.to_json(orient='records') #df dataframe resultat en vue mode records
jsonParsed = json.loads(recordsJson);#contenu parsé

for jsonRow in jsonParsed:
	#on réactualise la mesure -> up2date
	jsonRow['dateHour']=datetime.datetime.now().strftime(datetimestring)
	jsonRow['@timestamp']=datetime.datetime.now().isoformat()
	time.sleep(freq/1000)
	
	jsonRow2 = {"DatasetType" : jsonRow["code_model"], "data" : jsonRow }

	
	#API rest POST Json
	r = requests.post('http://'+ipBroadCast+':'+hostBroadPort+'/search/results', json=jsonRow2);
	
	#print(jsonRow2);
	#exit(-9);
	
	#print(jsonRow)
	if (r.status_code != 200): #code 200 http OK
		#sinon log anomalie
		print(jsonRow['dateHour']+' ERROR '+r.status_code+' '+jsonRow)

#code retour ok
exit(0);


##cnx.close()#fermeture connexion


