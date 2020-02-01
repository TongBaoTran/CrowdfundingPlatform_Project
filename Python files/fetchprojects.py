import connect

class Fetchprojects:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def fetchopenprojects(self):
        curs = self.conn.cursor()
        sqlExample = """select KENNUNG, kategorie, titel, benutzer.email,  benutzer.name, sum(spendenbetrag) 
                        from spenden, projekt, benutzer
                        where spenden.projekt = projekt.kennung
                        and projekt.ersteller=benutzer.email
                        and status ='offen'
                        group by KENNUNG, kategorie, titel, benutzer.email, benutzer.name
                        UNION  
                        select KENNUNG, kategorie, titel, benutzer.email, benutzer.name, 0.00 
                        from spenden, projekt, benutzer
                        where KENNUNG not in (select projekt from spenden)
                        and projekt.ersteller=benutzer.email
                        and status = 'offen'"""
        curs.execute(sqlExample)
        data = curs.fetchall()
        return data

    def fetchcloseprojects(self):
        curs = self.conn.cursor()
        sqlExample = """select KENNUNG, kategorie, titel, benutzer.email,  benutzer.name, sum(spendenbetrag)
                        from spenden, projekt, benutzer
                        where spenden.projekt = projekt.kennung
                        and projekt.ersteller=benutzer.email
                        and status ='geschlossen'
                        group by KENNUNG, kategorie, titel, benutzer.email, benutzer.name"""

        curs.execute(sqlExample)
        data = curs.fetchall()
        return data

    def completion(self):
        self.complete = True

    def close(self):
        if self.conn is not None:
            try:
                if self.complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                print(e)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    print(e)
