-- Importieren mit: 
-- db2start
-- db2 "connect to funder" (Angenommen, die Datenbank heißt 'funder')
-- db2 -vtf inputs.sql
-- Hinweis : Terminal soll im gleichen Verzeichnes geöffnet werden, wo die inputs.sql Datei liegt. 
-- Die Tabellen müssen bereits erstellt worden und leer sein.

INSERT INTO benutzer (email, name, beschreibung) VALUES
	('dummy@dummy.com', 'DummyUser', 'I am a dummy user!'),
	('alan@turing.com', 'Alan Turing', 'I like computers'),
	('donald@eKnuth.com', 'DonaldEKnuth', 'I like techn innovations'),
	('tim@bernersLee.com', 'Tim Berners Lee', 'I love the WWW')
;

INSERT INTO konto (inhaber, guthaben, geheimzahl) VALUES
	('dummy@dummy.com', 4555.89, '123456'),
	('alan@turing.com', 1000000, '654321'),
	('donald@eKnuth.com', 2000000, '00000'),
	('tim@bernersLee.com', 3000000.56, '42')
;

INSERT INTO kategorie (id, name, icon) VALUES
	(1, 'Health & Wellness', 'pfad/icons/health.png'),
	(2, 'Art & Creative Works', 'pfad/icons/art.png'),
	(3, 'Education', 'pfad/icons/education.png'),
	(4, 'Tech & Innovation', 'pfad/icons/tech.png')
;

INSERT INTO projekt (kennung, titel, beschreibung, finanzierungslimit, ersteller, vorgaenger, kategorie)  VALUES
	(1, 'Ubuntu Touch', 'Very firtst Ubunu Smartphone!', 50000, 'dummy@dummy.com', NULL, 4),
	(2, 'Ubuntu Touch Pro', 'Ubunu Smartphone with new Features and larger in Size', 80000, 'dummy@dummy.com', 1, 4),
	(3, 'Ubuntu Touch Light', 'Ubunu Smartphone with ', 80000, 'dummy@dummy.com', 1, 4),
	(4, 'Windows Touch', 'Windows OS Smartphone', 40000, 'alan@turing.com', NULL, 4),
	(5, 'Cooking Robot', 'Robot that cooks more than 1000 dishes for you', 90500.45, 'alan@turing.com', NULL, 1),
	(6, 'Chameleon Fineliners', 'Instantly blend color for all your writing, journaling, drawing, coloring, and more!', 3060.45, 'donald@eKnuth.com', NULL, 2),
	(7, 'Educational Robot', 'Teach robotics and programming to children aged 5 to 12.', 2495.01, 'tim@bernersLee.com', NULL, 3)
;

INSERT INTO kommentar (id, text, sichtbarkeit) VALUES
	(1, 'Ich hoffe das neuen Ubuntu Touch Pro toppt den Vorgänger', 'oeffentlich'),
	(2, 'Mal sehen ob es das Geld auch wert ist...', 'oeffentlich'),
	(3, 'Ich muss nie wieder kochen :)', 'oeffentlich')
;

INSERT INTO spenden (spender, projekt, spendenbetrag, sichtbarkeit) VALUES
	('alan@turing.com', 1, 15000, 'privat'),
	('donald@eKnuth.com', 2, 1500.56, 'oeffentlich'),
	('tim@bernersLee.com', 3, 90000, 'oeffentlich')
;

INSERT INTO schreibt (benutzer, projekt, kommentar) VALUES
	('alan@turing.com', 1, 1),
	('donald@eKnuth.com', 1, 2),
	('tim@bernersLee.com', 7, 3)
;
	
