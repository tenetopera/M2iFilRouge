MYSQL
-----
Tutoriel installation de MySQL, quasi dernière version la 8... sur la dernière version d'Ubuntu 21-10.
https://technowikis.com/44399/how-to-install-mysql-on-ubuntu-21-10

# Base de données MySQL survival commands $> (invite de commandes)
# démarrage du service
$> sudo systemctl start mysql
# stop du service
$> sudo systemctl stop mysql
# connexion à la console 
$> sudo mysql
# éventuellement avec -u utilisateur -p MotDePasse
$> sudo mysql iot -u utilisateur -p MotDePasse
$>mysql> exit;
# base de données de travail du projet fil rouge iot

EXISTANT CSV
------------

1 - 1er jeu de données IOT code X46789

Suite à des problèmes techniques, l'existant des métriques est assez maigre.
Il se compose d'un seul véhicule ou prototype sous mesures.
Les métriques se compose d'une grosse dizaine de fichiers (13) relevant des mesures de périodicité de l'ordre des 100 millisecondes avec une précision
de l'ordre de la microseconde.
S'étalant sur 2 jours des petites plages de 10 secondes toutes les 2 heures les matins.

* exemple d'un fichier, son nom est de la structure suivante : 
				X46789_2018-01-19T05-37-42.612Z
	CODE-VEHICULE-OU-PROTOTYPE _+ DATE DE LA METRIQUE AAAA-MM-JJ TIME HH-MM-SS + SS
(la seconde donne la seconde de la dernière mesure, la partie décimal donne la décimal de la première mesure, mais les contenus métriques des fichiers est tout de même tronqué à une plage de 10 secondes)

FORMAT CODE-VEHICULE X46789 AAAA-MM-JJ TIME HH-MM-SS  - portition en gros DER SECONDE . 1er micro mesure exemple 42 612z

Les données ont bien été importé, le schéma n'ayant pas été fourni, nous avons pu le déduire basiquement grace à MySQL.
La grosse difficulté a été de conserver la précision de l'horodatage de la métrique à la microseconde, mais MySQL le permet dès la version 5.7 avec le type datetime(6).

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

L'exploitation des données ne s'est pas avéré concluante, le jeu initial étant assez cahotique.
Il a finalement été abandonné pour une autre jeu plus clair dans la signification des données et dans sa qualité

2 - 2eme jeu de données IOT code X46790 - la Toyota Corolla

Nous avons pu trouver sur internet, un jeu de métriques sur un trajet de 200 km de 2h30 d'un Toyota Corolla en soirée.
Les métriques sont des l'ordre de la secondes avec une précision de la milliseconde (la précision microseconde est conservée, existant déja ou pour des iots futurs plus exigeants)
Ces métriques ont été obtenus par un dump des logs de Torque OBD.
https://play.google.com/store/apps/details?id=org.prowl.torque&hl=fr&gl=US

OBD
https://fr.wikipedia.org/wiki/Diagnostic_embarqué_(automobile) 
Est un système de diagnostic embarqué — en anglais On-Board Diagnostics, abrégé OBD ou système OBD) — sont un ensemble de capacités de diagnostic matériel qui est embarqué dans la plupart des véhicules à moteur thermique 
produits depuis les années 2000. Le règlement 83 parle également de systèmes d' autodiagnostic

Ce jeu de données est intéressant :
signifiant (type colonnes bien renseignés et données cohérentes)
continu, non segmentés (permet de tester un véhicule comme en conditions réels)

Afin de de démontrer la chaine de traitement IOT.
Ce jeu de données est pris pour base d'émission, il sera : 
- redressé à la date courante 
- et réémis avec la même périodicité ou du même ordre, toutes les 100 ms ou 200 ms 


BATCH
-----

datetime(6) stockage de date à la microsecondes
structure base de données cf 
X46789.sql

Après fusion des différents fichiers csv cf script bash
fusionIOT.sh

il existe 2 manière d'importer relativemement facilement des données tabulaires sur mysql

vi le script en mode shell (peut-être plus rapide) qui peut être monté dans la crontab (plannificateur : exécution automatique)
du système pour un mode batch régulier

ou vi la console (plus de suivi des blocages log erreur in live)

1-
#howto - https://learntutorials.net/fr/mysql/topic/5215/mysqlimport (liens bien faits)
http://sylvain.benest.free.fr/Documentation%20APACHE_PHP_MYSQL/Manuel%20MYSQL/Manuel%20html/mysqlimport.html
https://www.thegeekstuff.com/2008/10/import-and-upload-data-to-mysql-tables-using-mysqlimport/

exemple de commande mysqlimport shell
$>mysqlimport --ignore-lines=1 \ #ignorer l'entête
--fields-terminated-by=; \ #séparateur
--local \ #local
-C \ #compress si peu
-f \ #force, continue même si erreurs
-i \ #si doublons ignorer
-s \ #silent mode - pas bavard en log
X46789 \ #base de données cibles
X46789_2018-01-19T05-37-42.612Z.csv #fichier csv

commande réellement utilisé pour le 1er iot X46789, on note qu'il peut être préférable d'effacer la table et de la verouiller le temps de l'injection
des données (mode silent et verbose incompatible)
sudo mysqlimport --ignore-lines=1 --delete --lock-tables --verbose --fields-terminated-by='\;'\ --local -C -f  -i  -s  iot X46789.csv 

note : lorsque MySQL est configuré de manière sécurisé pour l'injection de données
les fichiers csv à injecter sont à positonner dans le datadir (répertoire de stockage des fichiers de la base de données)
généralement sous /var/lib/mysql/
ou ici notre cas : /var/lib/mysql/iot

2-
la méthode par la console permet un suivit plus rigoureux des bloquants le temps que la commande soit la bonne.
la syntaxe est généralement 
LOAD DATA INFILE 'X46789.csv' INTO TABLE X46789 FIELDS TERMINATED BY ';' IGNORE 1 LINES;
#ignore 1 lines pour l'entête de structure du fichier csv, la structure est déterminé dans notre cas par la table d'accueil.


Note : la possibilité d'importer des fichiers de données tabulaire de n'importe où, peut-être levée avec la variable d'environnement MySQL
secure_file_priv=NULL
usuellement dans le fichier de configuration : /etc/mysql/mysql.conf.d/mysql.cnd
section [mysqld]

Note SGBDR et version de mysql utilisée
---------------------------------------
Note MySQL :
version 5.7 support json en natif, type
avant manipulation complexe via expressions régulières
depuis MySQL 5.6 gestion des datetime possible jusuqu'à la microsecondes
https://dev.mysql.com/doc/refman/8.0/en/fractional-seconds.html 
MySQL has fractional seconds support for TIME, DATETIME, and TIMESTAMP values, with up to microseconds (6 digits) precision: 

Note MariaDB : 
gestion des bases de donnés temporelles gros + comme influxDB gros +
gestion de table lié à des fichiers xml, configuré par des expressions de mappages gros +



DONNEES CONSOLIDEES USAGE
-------------------------

Centralisé dans une sgbdr, l'usage est grandement simplifié, pour cause : 

# donne la liste des mesures ordonnées dans le temps en microsecondes
select * from X46789 order by dateHour asc;
# rapatriement de tout les éléments du model citrono pipo 1
select * from X46789 x inner join prototype p on x.code=p.code where p.code = 'X46789';

le data-modèle de ces métriques seras quant à lui fournit sous format XML, dit le sujet

# on peut en déduire un facilement en gardant le formalisme xml par défaut supportés par mysql, avec la commande qui suit
$> sudo mysql -e "desc iot.X46789;" --xml >> iot_X46789_model.xml
# table d'enrichissement des métriques 
#Les données récoltées doivent être enrichies en les croisant avec des informations sur le produit (nom du produit, type du produit, composantes internes du produit,…) 
#puis de mettre l’information finale dans des tables afin qu’elles puissent être exploitées. 
$> sudo mysql -e "desc iot.prototype;" --xml >> iot_prototype_model.xml


# on peut facilement copier un prototype pour base pour en faire un autre
create table X46790 as select * from X46789;
create table X46790 like X46789;

# contrainte de gestion : change la valeur par défaut du code prototype attaché
ALTER TABLE `X46790` CHANGE `code` `code` VARCHAR(10) NOT NULL DEFAULT 'X46790'; 
ALTER TABLE `X46791` CHANGE `code` `code` VARCHAR(10) NOT NULL DEFAULT 'X46791'; #...
ALTER TABLE `X46790` ADD `code` VARCHAR(10) NOT NULL DEFAULT 'X46790' FIRST; 
ALTER TABLE `X46790`     ADD CONSTRAINT FOREIGN KEY (code)    REFERENCES prototype(code);

sauvegarde du système simplifié : 
mysqldump iot prototype --fields-terminated-by=;
cf https://learntutorials.net/fr/mysql/topic/604/sauvegarde-avec-mysqldump

INTERACTION AVEC L'INTERFACE SOAP qui communique avec kafka
----------------------------------------

via le script producer.py

qui exploitre une procédure stockée, qui à l'avantage de masquer le modèle de donner et de simplifier le codage.

cf sp_trameIOT.sql
	#paramètres : code du prototype 
	#puis détails true/false, 
	#le code model alias code dataset true/false
	#export du modèle xml true/false
	#nombre de lignes limité à nombre passé en paramètre ... -si 1 -> toutes les données
	df=pd.read_sql('call sp_trameIOT("'+prototype+'",true,true,false,-1);',cnx) 



GESTION MULTI IOTS
------------------

Avec les script 
controlCreatePrototype.py
qui prend en paramètre le schéma XML (fichier .xml) du nouvel IOT et son code gestion et
crée toute la structure nécessaire en base









# "humour" ... un peu le sujet ?
# 3 nouveaux moterur bionic multisoupapes citronnault Pipo
# c'est très cher et y a pas pire
#info marketing
#https://www.youtube.com/watch?v=SXEDeTN8rXg