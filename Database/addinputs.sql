-- Importieren mit: 
-- db2start
-- db2 "connect to funder" (Angenommen, die Datenbank heißt 'funder')
-- db2 -vtf inputs.sql

INSERT INTO benutzer (email, name, beschreibung) VALUES
	('alex@john.com', 'alexjohn', 'I love reading'),
	('fun@gmail.com', 'Fin', 'I love thinking'),
	('jeni@gmail.com', 'Jenifer', 'I love philosophy'),
	('camy@gmail.com', 'Camy', 'I love tech')
;

INSERT INTO konto (inhaber, guthaben, geheimzahl) VALUES
	('alex@john.com', 20002.56, '102542'),
	('fun@gmail.com', 10000.00, '301245'),
	('jeni@gmail.com', 30125.21, '201364'),
	('camy@gmail.com', 21451.87, '321445')      
;

INSERT INTO kommentar (id, text, sichtbarkeit) VALUES
	(4, 'Ich love Ubuntu Touch Pro', 'oeffentlich'),
	(5, 'The idea is very nice', 'privat'),
	(6, 'This will be great for my blog', 'oeffentlich'),
	(7, 'Look interesting!!!', 'oeffentlich'),
        (8, 'Robot foods..ehhhh', 'oeffentlich'),
        (9, 'No Robots in education!!!', 'oeffentlich')
;

INSERT INTO spenden (spender, projekt, spendenbetrag, sichtbarkeit) VALUES
	('alex@john.com', 4, 11000, 'privat'),
	('fun@gmail.com', 5, 1000, 'oeffentlich'),
	('camy@gmail.com', 6, 2000, 'privat'),
	('dummy@dummy.com', 7, 15000, 'oeffentlich')
;

INSERT INTO schreibt (benutzer, projekt, kommentar) VALUES
	('alan@turing.com', 2, 4),
	('fun@gmail.com', 4, 5),
	('jeni@gmail.com', 6, 6),
	('camy@gmail.com', 2, 7),
	('alan@turing.com', 5, 8),
	('camy@gmail.com', 3, 9)
;
	
