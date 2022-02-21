

#CODE - table_name prototype
#details - détails du prototype étudié
#code model - code modele pour les consumer kafka
#model - schema modele xml
#limit 50 - nombre limite d'enregistrement
use iot; 
drop  PROCEDURE if EXISTS sp_trameIOT;

DELIMITER //
use iot; //
CREATE PROCEDURE sp_trameIOT(in code VARCHAR(20),in bdetails boolean,in bcodemodel boolean,in bmodel boolean,in ilimite int) 
BEGIN
    #SET @err = 0;
    declare table_name varchar(20) DEFAULT '';
    declare sql_query varchar(300) DEFAULT '';
    declare sql_details varchar(50) DEFAULT '';
    declare sql_codemodel varchar(20) DEFAULT '';
    declare sql_model varchar(20) DEFAULT '';
    declare sql_limit varchar(20) DEFAULT '';
    
    SET @table_name = code;# le code prototype est le nom de la table de stockage
    
    #si on veux les détails du prototype
    IF bdetails THEN
       SET @sql_details =' p.code as codep,p.libelle,p.marque,p.version, ';
    ELSE
       SET @sql_details ='';
    END IF; 
    
    #si on veux le code model pour consumer kafka
    IF bcodemodel THEN
       SET @sql_codemodel =' p.code_model, ';
    ELSE
       SET @sql_codemodel ='';
    END IF;     
    
    #si on veux les model xml pour gestion
    IF bmodel THEN
       SET @sql_model =' p.model, ';
    ELSE
       SET @sql_model ='';
    END IF;    

    #si on veux des données partielles - limit sql
    IF ilimite>=0 THEN
       SET @sql_limit =concat(' limit ',ilimite);
    ELSE
       SET @sql_limit ='';
    END IF;    

	#construction de la requete demandée
    SET @sql_query =concat('select ',@sql_codemodel,@sql_details,@sql_model,' * from ',@table_name,' x inner join prototype p on x.code=p.code where p.code = "', @table_name,'" ',@sql_limit);
    
    #exécution projection
    PREPARE stmt FROM @sql_query;
    EXECUTE stmt;
    #INSERT into log values (@sql_query); # ++dd debug for trace
    #print @sql_query

END //
DELIMITER ;