import connect

class Fetchinfo:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def info_projekt(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select kategorie, titel, benutzer.email, benutzer.name,  CAST(projekt.beschreibung AS VARCHAR(200)) AS Beschreibung,finanzierungslimit, status  
                        from  projekt, benutzer
                        where projekt.kennung = ?
                        and projekt.ersteller=benutzer.email"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def info_vorgaenger(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select p1.vorgaenger, p2.titel
                        from projekt p1, projekt p2
                        where p1.kennung=?
                        and p1.vorgaenger = p2.kennung"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def info_sumspenden(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select sum(spendenbetrag) from spenden where projekt = ? """
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data


    def info_spendenlist(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select * 
                        from (select s.projekt, b.name, s.spendenbetrag
                        from spenden s, benutzer b
                        where  s.projekt = ?
                        and s.spender=b.email
                        and s.sichtbarkeit = 'oeffentlich'
                        UNION
                        select s.projekt, 'Anonym', s.spendenbetrag
                        from spenden s, benutzer b
                        where s.projekt = ?
                        and s.sichtbarkeit = 'privat'
                        and s.spender=b.email) spendList
                        order by spendList.spendenbetrag DESC"""
        curs.execute(sqlExample, (kennung,kennung))
        data = curs.fetchall()
        return data

    def info_from_kommentar(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select * 
                        from (select k.id, b.name, CAST(k.text AS VARCHAR(200)) AS Text  
                        from schreibt s , kommentar k, benutzer b
                        where s.kommentar= k.id and s.benutzer=b.email and s.projekt = ?
                        and k.sichtbarkeit = 'oeffentlich'
                        UNION
                        select k.id, 'Anonym', CAST(k.text AS VARCHAR(200)) AS Text  
                        from schreibt s , kommentar k, benutzer b
                        where s.kommentar= k.id and s.benutzer=b.email and s.projekt = ?
                        and k.sichtbarkeit = 'privat') comments
                        order by comments.id DESC"""
        curs.execute(sqlExample, (kennung,kennung))
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
