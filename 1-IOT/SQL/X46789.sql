
# création de table
CREATE TABLE `iot`.`X46789` (
`dateHour` DATETIME(6), 
`gpsSpeed` DECIMAL(18,15), 
`gpsSatCount` DECIMAL(4,1), 
`Gear` DECIMAL(4,1), 
`Brake_pedal` DECIMAL(4,1), 
`Accel_pedal` DECIMAL(4,1), 
`Machine_Speed_Mesured` DECIMAL(4,1), 
`AST_Direction` DECIMAL(3,1), 
`Ast_HPMB1_Pressure_bar` DECIMAL(3,1), 
`Ast_HPMA_Pressure_bar` DECIMAL(3,1), 
`Pressure_HighPressureReturn` DECIMAL(6,1), 
`Pressure_HighPressure` DECIMAL(6,1), 
`Oil_Temperature` DECIMAL(4,1), 
`Ast_FrontAxleSpeed_Rpm` DECIMAL(6,1), 
`Pump_Speed` DECIMAL(5,1)
) 
ENGINE=InnoDB;

# ajout à la table des métriques pour jointure avec avec le détails du véhicule prototype
ALTER TABLE `X46789` ADD `code` VARCHAR(10) NOT NULL DEFAULT 'X46789' FIRST; 
ALTER TABLE `X46789`     ADD CONSTRAINT FOREIGN KEY (code)    REFERENCES prototype(code);
# idem pour autres métriques d'autres modèle
ALTER TABLE `X46790` ADD `code` VARCHAR(10) NOT NULL DEFAULT 'X46790' FIRST; 
ALTER TABLE `X46790`     ADD CONSTRAINT FOREIGN KEY (code)    REFERENCES prototype(code);
ALTER TABLE `X46791`     ADD CONSTRAINT FOREIGN KEY (code)    REFERENCES prototype(code);

#au début pour se familliariser avec le datetime microseconde et perdre le moins de données précisions possible
#INSERT INTO `X46789` (`dateHourStr`, `dateHourDate`, `dateHourTime`, `gpsSpeed`, `gpsSatCount`, `Gear`, `Brake_pedal`, `Accel_pedal`, `Machine_Speed_Mesured`, `AST_Direction`, `Ast_HPMB1_Pressure_bar`, `Ast_HPMA_Pressure_bar`, `Pressure_HighPressureReturn`, `Pressure_HighPressure`, `Oil_Temperature`, `Ast_FrontAxleSpeed_Rpm`, `Pump_Speed`) VALUES ('2018-01-19 09:19:0.967413', '2018-01-19 09:19:0.967413', '2018-01-19 09:19:0.967413', '10.01', '1', '2', '1', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3'); 
#INSERT INTO `X46789` (`dateHour`, `gpsSpeed`, `gpsSatCount`, `Gear`, `Brake_pedal`, `Accel_pedal`, `Machine_Speed_Mesured`, `AST_Direction`, `Ast_HPMB1_Pressure_bar`, `Ast_HPMA_Pressure_bar`, `Pressure_HighPressureReturn`, `Pressure_HighPressure`, `Oil_Temperature`, `Ast_FrontAxleSpeed_Rpm`, `Pump_Speed`) VALUES ('2018-01-19 09:19:0.967413',  '10.01', '1', '2', '1', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3'); 
