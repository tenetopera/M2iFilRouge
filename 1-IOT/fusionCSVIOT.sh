#!/bin/bash

#parcours de tout les fichiers csv
for fileNAME in ls *.csv
do
	#purge de l'entete du csv
	sed 1d $fileNAME -i
	#récupération du nom de l iot
	iotNAME=`echo "$fileNAME" | cut -d'_' -f1`
	#concaténation des sous fichiers de l iot dans un fichier général
	printf "\n"  >> $iotNAME.csv
	cat $fileNAME >> $iotNAME.csv
done
#suppression des lignes vides
grep . $iotNAME.csv >> $iotNAME.tmp.csv
mv -f $iotNAME.tmp.csv $iotNAME.csv
#copies dans le mysql datadir (seul lieu d'import en conf mysql sécurisé)
sudo cp $iotNAME.csv /var/lib/mysql
sudo cp $iotNAME.csv /var/lib/mysql/iot
