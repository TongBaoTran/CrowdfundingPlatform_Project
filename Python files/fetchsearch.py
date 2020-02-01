import connect

class Fetchsearch:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def projects(self, keyword):
        curs = self.conn.cursor()
        sqlExample = """select kennung, titel from projekt where titel like ?"""
        curs.execute(sqlExample, (keyword.title()+"%",))
        data = curs.fetchall()
        return data

    def projectinfo(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select KENNUNG, kategorie, titel, benutzer.name, sum(spendenbetrag), status
                        from spenden, projekt, benutzer
                        where  projekt.kennung=spenden.projekt
                        and projekt.kennung=?
                        and projekt.ersteller=benutzer.email
                        group by KENNUNG, kategorie, titel, ersteller, benutzer.name, status
                        UNION  
                        select KENNUNG, kategorie, titel, benutzer.name, 0, status 
                        from spenden, projekt, benutzer
                        where KENNUNG not in (select projekt from spenden)
                        and projekt.ersteller=benutzer.email
                        and projekt.kennung= ?"""
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
