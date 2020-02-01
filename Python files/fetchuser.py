import connect

class Fetchuser:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def fetchvorgaenger(self, user_email):
        curs = self.conn.cursor()
        sqlExample = """select KENNUNG, titel from projekt where ersteller = ?"""
        curs.execute(sqlExample, (user_email,))
        data = curs.fetchall()
        return data

    def fetch_erstellte_project(self, user_email):
        curs = self.conn.cursor()
        sqlExample = """select kennung,kategorie, titel, sum(spendenbetrag),status from spenden, projekt
                        where spenden.projekt = projekt.kennung
                        and projekt.ersteller =  ?
                        group by kennung, titel,  status, kategorie
                        UNION
                        select kennung,kategorie, titel, 0.00 ,status from spenden, projekt
                        where projekt.ersteller = ?
                        and projekt.kennung not in (select projekt from spenden) """
        curs.execute(sqlExample, (user_email, user_email))
        data = curs.fetchall()
        return data


    def fetch_unterstutzt_project(self, user_email):
        curs = self.conn.cursor()
        sqlExample = """select kennung, kategorie, titel, finanzierungslimit, status, spendenbetrag from spenden, projekt
                        where spenden.spender= ?
                        and spenden.projekt = projekt.kennung
                        and spenden.sichtbarkeit='oeffentlich'
                        group by kennung, titel, finanzierungslimit, status, spendenbetrag, kategorie"""
        curs.execute(sqlExample, (user_email,))
        data = curs.fetchall()
        return data

    def fetch_unterstutzt_all(self, user_email):
        curs = self.conn.cursor()
        sqlExample = """select projekt from spenden  where spender= ?"""
        curs.execute(sqlExample, (user_email,))
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
