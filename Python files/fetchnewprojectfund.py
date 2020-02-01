import connect


class Fetchnewprojectfund:
    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def spenderList(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select spender from spenden where projekt = ?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def titel_status(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select titel, status from projekt where kennung=?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def kontoinfo(self, user_email):
        curs = self.conn.cursor()
        sqlExample = """select * from konto where inhaber = ?"""
        curs.execute(sqlExample, (user_email,))
        data = curs.fetchall()
        return data

    def addSpenden(self, spendentoAdd):
        curs = self.conn.cursor()
        sqlExample = """INSERT INTO spenden (spender, projekt, spendenbetrag, sichtbarkeit) VALUES(?,?,?,?)"""
        curs.execute(sqlExample, (spendentoAdd.getspender(), spendentoAdd.getprojekt(), spendentoAdd.getspendenbetrag(),
                                  spendentoAdd.getsichtbarkeit()))

    def updatekonto(self, amount, user_email):
        curs = self.conn.cursor()
        sqlExample = """update konto set guthaben=guthaben-? where inhaber= ?"""
        curs.execute(sqlExample, (amount, user_email))

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
