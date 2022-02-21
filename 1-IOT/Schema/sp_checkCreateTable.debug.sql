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
insert into logs(log) values(concat('creation ',creation)); 
insert into logs(log) values(concat('sql cre ',sql_create));         
    	PREPARE stmtcrea FROM @sql_create;    
insert into logs(log) values(concat('sql cre ',sql_create));                 
    	EXECUTE stmtcrea ;
insert into logs(log) values(concat('sql cre ',sql_create));                 
    END IF;

insert into logs(log) values(concat('tabel name ',table_name));         
insert into logs(log) values(concat('tabel name ',@table_name));         
    SET @sql_query_test = CONCAT('SELECT 1 FROM ',@table_name);
insert into logs(log) values(concat('sql_query_test ',@sql_query_test));         
    PREPARE stmttest FROM @sql_query_test;
insert into logs(log) values(concat('sql_query_test ',@sql_query_test));         

    IF (@err = 1) THEN
insert into logs(log) values(concat('table_exists 0-',@table_exists));             
        SET table_exists = 0;
    ELSE
insert into logs(log) values(concat('table_exists 1-',@table_exists));             
		SET table_exists = 1;
        DEALLOCATE PREPARE stmttest;
    END IF;
	SET @table_exists_ret = table_exists;    
insert into logs(log) values(concat('table_exists ',@table_exists));         

select @table_exists_ret;
END //
DELIMITER ;   