import sys
import json
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import xml.etree.ElementTree as ET

#IP MySQL server de données agregeant les données
ipMySQL='127.0.0.1';#ipMySQL='172.19.90.21';#accès distant test
loginMySQL='formation';
passMySQL='formation';
baseMySQL='iot';

# usage pour test / développement
xmlstring="""
<?xml version="1.0"?>
<resultset statement="desc iot.X46789" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
	<field name="Field">code</field>
	<field name="Type">varchar(10)</field>
	<field name="Null">NO</field>
	<field name="Key"></field>
	<field name="Default">X46789</field>
	<field name="Extra"></field>
  </row>
</resultset>
"""
helpStr="""
Controle d'intégrité et création d'un nouveau prototype véhicule.
#paramètres passés en arguments :
# [paramètre #1] (obligatoire) Le fichier du schéma XML des métriques en entrée.
# si seul, simple controle d'intégrité.
# structure du type : 
# <?xml version="1.0"?>
# <resultset>
#  <row>
#    <field name="Field">code</field>
#    <field name="Type">varchar(10)</field>
#    <field name="Null">NO</field>
#    <field name="Default">X46789</field>
#  </row> (...)
# </resultset>

# [paramètre #2] (facultatif) Le code du prototype en entrée. Si renseigné crée la # table des métriques.
""";

if len(sys.argv)>=3:
	pass
else:
	print (helpStr)
	exit(1)

fichierSchema=""

prototype=""
try:
  prototype=sys.argv[2];
except:
  prototype=""

fichierSchema=sys.argv[1];


root=None;
#on est en mode test
if fichierSchema=="":
  root = ET.ElementTree(ET.fromstring(xmlstring.strip()))
else:
#fichier du modèle, on va controler l'intégrité
  root = ET.parse(fichierSchema).getroot() #exemple 'iot_X46789_model.xml'

sqlstring = "create table "
if prototype=="":
  sqlstring+=" temporary temptable "

sqlstring+=prototype+" ("

#pour chaque ligne une colonne sql
#schema dateHour datetime(6) is null default ''
# nom type (is null) (default 'valeur')
sqlstringField = " {valueField} {valueType} {valueNull} {valueDefault} " 
for type_tagRow in root.findall('row'):
  #print(type_tagRow)    
  sqlstring+=","
  #inspection des attributs de ce champ
  for type_tagField in type_tagRow.findall('field'):
    #print(type_tag2)    
    valueField=""
    valueType=""
    valueNull=""
    valueDefault=""
    valueName = type_tagField.get('name')
    #print(type_tagField.text);    exit()
    if (valueName=="Field"):
      valueField=type_tagField.text
    elif (valueName=="Type"):
      valueType=type_tagField.text
    elif (valueName=="Null"):
      valueNull= "NULL" if type_tagField.text == "YES" else "NOT NULL";
    elif (valueName=="Default"):   
      valueDefault= "" if type_tagField.text == "" or str(type_tagField.text) == "None" else "default \""+str(type_tagField.text)+"\"";      
    sqlstring+= f" {valueField} {valueType} {valueNull} {valueDefault} " 

sqlstring=sqlstring.replace("(,", "(")
sqlstring += ")" 

#travail sur la base de données
cnx = create_engine('mysql+pymysql://'+loginMySQL+':'+passMySQL+'@'+ipMySQL+'/'+baseMySQL)


#table_exists=false
df=None;
#récupération des données du prototype passé en argeument 
try:
  # PROCEDURE sp_checkCreateTable(
  #paramètres : nome de la table à créer table_name VARCHAR(100),
  # sql de creation 
  # la créee ou temporary juste pour test en session
  # code de réussite 1 ok 0 nok
  
  #insertion des détails prototype
  schemaXML='<? xml version="1.0"?>'+ET.tostring(root,encoding='unicode',method='xml');
  schemaXML='';
  sqlxml='insert into prototype (code,libelle,marque,version,code_model,model) select "'+prototype+'","libellé '+prototype+'","marque '+prototype+'","1",max(code_model)+1,'+"'"+schemaXML+"' from prototype;";
  
  sqlsp='call sp_checkCreateTable("'+prototype+'","'+sqlstring+'"'+',true,@table_exists);'  
  df=pd.read_sql(sqlsp+sqlxml,cnx)
 
except:	
	print('Prototype inexistant, veuillez au préalable définir le modèle XML, assurez vous que la table éxiste.');
	exit(-3)

resuJson = df.to_json(orient='records') #df dataframe resultat en vue mode records
jsonParsed = json.loads(resuJson);#contenu parsé

#if not table_exists:
try:
  if str(jsonParsed[0]['@table_exists_ret'])!="1":
      print("ERROR création du prototype, vérifiez que votre modèle est valide, ou que le prototype n'existe pas déjà.")
  else:
    print("SUCCES prototype et table : "+prototype)
except:
    print("Problème de communication avec le serveur.")

