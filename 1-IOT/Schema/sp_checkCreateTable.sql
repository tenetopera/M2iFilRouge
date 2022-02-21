use iot; 
drop  PROCEDURE if EXISTS sp_checkCreateTable;
DELIMITER //
use iot; //
CREATE PROCEDURE sp_checkCreateTable(
in table_name VARCHAR(100),
in sql_create text,
in creation boolean,
inout table_exists int
) 
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02' SET @err = 1;
    SET @err = 0;
    SET @table_name = table_name;
    SET @sql_create = sql_create;

    IF (creation is true) THEN	    
    	PREPARE stmtcrea FROM @sql_create;    
    	EXECUTE stmtcrea ;
    END IF;

    SET @sql_query_test = CONCAT('SELECT 1 FROM ',@table_name);
    PREPARE stmttest FROM @sql_query_test;

    IF (@err = 1) THEN
        SET table_exists = 0;
    ELSE
		SET table_exists = 1;
        DEALLOCATE PREPARE stmttest;
    END IF;
	SET @table_exists_ret = table_exists;    

select @table_exists_ret;

END //
DELIMITER ;   
