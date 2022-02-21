MYSQL
-----
Tutoriel installation de MySQL, quasi derni�re version la 8... sur la derni�re version d'Ubuntu 21-10.
https://technowikis.com/44399/how-to-install-mysql-on-ubuntu-21-10

# Base de donn�es MySQL survival commands $> (invite de commandes)
# d�marrage du service
$> sudo systemctl start mysql
# stop du service
$> sudo systemctl stop mysql
# connexion � la console 
$> sudo mysql
# �ventuellement avec -u utilisateur -p MotDePasse
$> sudo mysql iot -u utilisateur -p MotDePasse
$>mysql> exit;
# base de donn�es de travail du projet fil rouge iot

EXISTANT CSV
------------

1 - 1er jeu de donn�es IOT code X46789

Suite � des probl�mes techniques, l'existant des m�triques est assez maigre.
Il se compose d'un seul v�hicule ou prototype sous mesures.
Les m�triques se compose d'une grosse dizaine de fichiers (13) relevant des mesures de p�riodicit� de l'ordre des 100 millisecondes avec une pr�cision
de l'ordre de la microseconde.
S'�talant sur 2 jours des petites plages de 10 secondes toutes les 2 heures les matins.

* exemple d'un fichier, son nom est de la structure suivante : 
				X46789_2018-01-19T05-37-42.612Z
	CODE-VEHICULE-OU-PROTOTYPE _+ DATE DE LA METRIQUE AAAA-MM-JJ TIME HH-MM-SS + SS
(la seconde donne la seconde de la derni�re mesure, la partie d�cimal donne la d�cimal de la premi�re mesure, mais les contenus m�triques des fichiers est tout de m�me tronqu� � une plage de 10 secondes)

FORMAT CODE-VEHICULE X46789 AAAA-MM-JJ TIME HH-MM-SS  - portition en gros DER SECONDE . 1er micro mesure exemple 42 612z

Les donn�es ont bien �t� import�, le sch�ma n'ayant pas �t� fourni, nous avons pu le d�duire basiquement grace � MySQL.
La grosse difficult� a �t� de conserver la pr�cision de l'horodatage de la m�trique � la microseconde, mais MySQL le permet d�s la version 5.7 avec le type datetime(6).

$> sudo mysql -e "desc iot.X46789;" --xml >> iot_X46789_model.xml
Extrait : 
<?xml version="1.0"?>
<resultset statement="desc iot.X46789" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
	<field name="Field">dateHour</field>
	<field name="Type">datetime(6)</field>
	<field name="Null">YES</field>
	<field name="Key"></field>
	<field name="Default" xsi:nil="true" />
	<field name="Extra"></field>
  </row>
...

L'exploitation des donn�es ne s'est pas av�r� concluante, le jeu initial �tant assez cahotique.
Il a finalement �t� abandonn� pour une autre jeu plus clair dans la signification des donn�es et dans sa qualit�

2 - 2eme jeu de donn�es IOT code X46790 - la Toyota Corolla

Nous avons pu trouver sur internet, un jeu de m�triques sur un trajet de 200 km de 2h30 d'un Toyota Corolla en soir�e.
Les m�triques sont des l'ordre de la secondes avec une pr�cision de la milliseconde (la pr�cision microseconde est conserv�e, existant d�ja ou pour des iots futurs plus exigeants)
Ces m�triques ont �t� obtenus par un dump des logs de Torque OBD.
https://play.google.com/store/apps/details?id=org.prowl.torque&hl=fr&gl=US

OBD
https://fr.wikipedia.org/wiki/Diagnostic_embarqu�_(automobile) 
Est un syst�me de diagnostic embarqu� � en anglais On-Board Diagnostics, abr�g� OBD ou syst�me OBD) � sont un ensemble de capacit�s de diagnostic mat�riel qui est embarqu� dans la plupart des v�hicules � moteur thermique 
produits depuis les ann�es 2000. Le r�glement 83 parle �galement de syst�mes d' autodiagnostic

Ce jeu de donn�es est int�ressant :
signifiant (type colonnes bien renseign�s et donn�es coh�rentes)
continu, non segment�s (permet de tester un v�hicule comme en conditions r�els)

Afin de de d�montrer la chaine de traitement IOT.
Ce jeu de donn�es est pris pour base d'�mission, il sera : 
- redress� � la date courante 
- et r��mis avec la m�me p�riodicit� ou du m�me ordre, toutes les 100 ms ou 200 ms 


BATCH
-----

datetime(6) stockage de date � la microsecondes
structure base de donn�es cf 
X46789.sql

Apr�s fusion des diff�rents fichiers csv cf script bash
fusionIOT.sh

il existe 2 mani�re d'importer relativemement facilement des donn�es tabulaires sur mysql

vi le script en mode shell (peut-�tre plus rapide) qui peut �tre mont� dans la crontab (plannificateur : ex�cution automatique)
du syst�me pour un mode batch r�gulier

ou vi la console (plus de suivi des blocages log erreur in live)

1-
#howto - https://learntutorials.net/fr/mysql/topic/5215/mysqlimport (liens bien faits)
http://sylvain.benest.free.fr/Documentation%20APACHE_PHP_MYSQL/Manuel%20MYSQL/Manuel%20html/mysqlimport.html
https://www.thegeekstuff.com/2008/10/import-and-upload-data-to-mysql-tables-using-mysqlimport/

exemple de commande mysqlimport shell
$>mysqlimport --ignore-lines=1 \ #ignorer l'ent�te
--fields-terminated-by=; \ #s�parateur
--local \ #local
-C \ #compress si peu
-f \ #force, continue m�me si erreurs
-i \ #si doublons ignorer
-s \ #silent mode - pas bavard en log
X46789 \ #base de donn�es cibles
X46789_2018-01-19T05-37-42.612Z.csv #fichier csv

commande r�ellement utilis� pour le 1er iot X46789, on note qu'il peut �tre pr�f�rable d'effacer la table et de la verouiller le temps de l'injection
des donn�es (mode silent et verbose incompatible)
sudo mysqlimport --ignore-lines=1 --delete --lock-tables --verbose --fields-terminated-by='\;'\ --local -C -f  -i  -s  iot X46789.csv 

note : lorsque MySQL est configur� de mani�re s�curis� pour l'injection de donn�es
les fichiers csv � injecter sont � positonner dans le datadir (r�pertoire de stockage des fichiers de la base de donn�es)
g�n�ralement sous /var/lib/mysql/
ou ici notre cas : /var/lib/mysql/iot

2-
la m�thode par la console permet un suivit plus rigoureux des bloquants le temps que la commande soit la bonne.
la syntaxe est g�n�ralement 
LOAD DATA INFILE 'X46789.csv' INTO TABLE X46789 FIELDS TERMINATED BY ';' IGNORE 1 LINES;
#ignore 1 lines pour l'ent�te de structure du fichier csv, la structure est d�termin� dans notre cas par la table d'accueil.


Note : la possibilit� d'importer des fichiers de donn�es tabulaire de n'importe o�, peut-�tre lev�e avec la variable d'environnement MySQL
secure_file_priv=NULL
usuellement dans le fichier de configuration : /etc/mysql/mysql.conf.d/mysql.cnd
section [mysqld]

Note SGBDR et version de mysql utilis�e
---------------------------------------
Note MySQL :
version 5.7 support json en natif, type
avant manipulation complexe via expressions r�guli�res
depuis MySQL 5.6 gestion des datetime possible jusuqu'� la microsecondes
https://dev.mysql.com/doc/refman/8.0/en/fractional-seconds.html 
MySQL has fractional seconds support for TIME, DATETIME, and TIMESTAMP values, with up to microseconds (6 digits) precision: 

Note MariaDB : 
gestion des bases de donn�s temporelles gros + comme influxDB gros +
gestion de table li� � des fichiers xml, configur� par des expressions de mappages gros +



DONNEES CONSOLIDEES USAGE
-------------------------

Centralis� dans une sgbdr, l'usage est grandement simplifi�, pour cause : 

# donne la liste des mesures ordonn�es dans le temps en microsecondes
select * from X46789 order by dateHour asc;
# rapatriement de tout les �l�ments du model citrono pipo 1
select * from X46789 x inner join prototype p on x.code=p.code where p.code = 'X46789';

le data-mod�le de ces m�triques seras quant � lui fournit sous format XML, dit le sujet

# on peut en d�duire un facilement en gardant le formalisme xml par d�faut support�s par mysql, avec la commande qui suit
$> sudo mysql -e "desc iot.X46789;" --xml >> iot_X46789_model.xml
# table d'enrichissement des m�triques 
#Les donn�es r�colt�es doivent �tre enrichies en les croisant avec des informations sur le produit (nom du produit, type du produit, composantes internes du produit,�) 
#puis de mettre l�information finale dans des tables afin qu�elles puissent �tre exploit�es. 
$> sudo mysql -e "desc iot.prototype;" --xml >> iot_prototype_model.xml


# on peut facilement copier un prototype pour base pour en faire un autre
create table X46790 as select * from X46789;
create table X46790 like X46789;

# contrainte de gestion : change la valeur par d�faut du code prototype attach�
ALTER TABLE `X46790` CHANGE `code` `code` VARCHAR(10) NOT NULL DEFAULT 'X46790'; 
ALTER TABLE `X46791` CHANGE `code` `code` VARCHAR(10) NOT NULL DEFAULT 'X46791'; #...
ALTER TABLE `X46790` ADD `code` VARCHAR(10) NOT NULL DEFAULT 'X46790' FIRST; 
ALTER TABLE `X46790`     ADD CONSTRAINT FOREIGN KEY (code)    REFERENCES prototype(code);

sauvegarde du syst�me simplifi� : 
mysqldump iot prototype --fields-terminated-by=;
cf https://learntutorials.net/fr/mysql/topic/604/sauvegarde-avec-mysqldump

INTERACTION AVEC L'INTERFACE SOAP qui communique avec kafka
----------------------------------------

via le script producer.py

qui exploitre une proc�dure stock�e, qui � l'avantage de masquer le mod�le de donner et de simplifier le codage.

cf sp_trameIOT.sql
	#param�tres : code du prototype 
	#puis d�tails true/false, 
	#le code model alias code dataset true/false
	#export du mod�le xml true/false
	#nombre de lignes limit� � nombre pass� en param�tre ... -si 1 -> toutes les donn�es
	df=pd.read_sql('call sp_trameIOT("'+prototype+'",true,true,false,-1);',cnx) 



GESTION MULTI IOTS
------------------

Avec les script 
controlCreatePrototype.py
qui prend en param�tre le sch�ma XML (fichier .xml) du nouvel IOT et son code gestion et
cr�e toute la structure n�cessaire en base









# "humour" ... un peu le sujet ?
# 3 nouveaux moterur bionic multisoupapes citronnault Pipo
# c'est tr�s cher et y a pas pire
#info marketing
#https://www.youtube.com/watch?v=SXEDeTN8rXg