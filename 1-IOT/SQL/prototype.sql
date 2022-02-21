#table des détails des prototype étudiés
#v1

drop TABLE `iot`.`prototype`;
CREATE TABLE `iot`.`prototype` (
`code` varchar(10), 
`libelle` varchar(50),
`marque` varchar(20),
version varchar(10) 
);

ALTER TABLE `prototype` ADD PRIMARY KEY(`code`); 

#code;libelle;marque;version;
#X46789;citronnault Pipo;citronnault;1
#X46790;Corolla;Toyota;1
#X46791;citronnault Deluxe GTX;citronnault;

# v2 ajout de Pierre pour gestion multi iots
create table prototype (
    code varchar(10),
        libelle varchar(50),
        marque varchar(10),
        version varchar(10),
        code_model varchar(10),
    model text
)
# ou avec maj
ALTER TABLE prototype ADD code_model VARCHAR(10) DEFAULT '1'; 
ALTER TABLE prototype ADD model text ; 

INSERT INTO `iot`.`prototype` values ('X46789','citronnault Pipo','citronnault','1','1','');
INSERT INTO `iot`.`prototype` values ('X46790','Corolla','Toyota','1','2','');
INSERT INTO `iot`.`prototype` values ('X46791','citronnault Deluxe GTX','citronnault','1','3','');

#insertion du modele xml dans la table prototype
update table `iot`.`prototype` set model='
### copier ici le contenu du fichier iot_X46789_model
' where code_model='1';

update table `iot`.`prototype` set model='
### copier ici le contenu du fichier iot_X46790_model
' where code_model='2';