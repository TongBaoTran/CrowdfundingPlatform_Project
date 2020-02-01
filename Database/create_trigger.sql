-- Importieren mit: db2 -td@ -v -f create_trigger.sql
CREATE TRIGGER statusupdate
AFTER INSERT ON spenden
REFERENCING NEW AS neu
FOR EACH ROW MODE DB2SQL
BEGIN ATOMIC
	DECLARE finanzierungslimit DECIMAL(10,2);
	DECLARE aktuelleSpendenSumme DECIMAL(10,2);
	SET finanzierungslimit = (select finanzierungslimit from projekt p where p.kennung = neu.projekt);
	SET aktuelleSpendenSumme = (select sum(spendenbetrag) from spenden s where s.projekt = neu.projekt);
	IF aktuelleSpendenSumme >= finanzierungslimit THEN
		UPDATE projekt SET status = 'geschlossen' where kennung = neu.projekt;
	END IF;
END@
