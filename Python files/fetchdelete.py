import connect

class Fetchdelete:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def titel_creator(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select titel, ersteller from projekt where kennung=?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def childList(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select kennung from projekt where vorgaenger=?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def updateVorgaenger(self, childList):
        curs = self.conn.cursor()
        sqlExample = """UPDATE  projekt SET  vorgaenger = NULL WHERE kennung = ?"""
        for row in childList:
            curs.execute(sqlExample, (row[0],))

    def spenderList(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select * from spenden where projekt = ?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def kommentaridList(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select kommentar from schreibt  where projekt=?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def payback(self, amount, donor):
        curs = self.conn.cursor()
        sqlExample = """UPDATE konto SET guthaben = guthaben + ? WHERE inhaber=?"""
        curs.execute(sqlExample, (amount,donor))

    def deletespenden(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """DELETE FROM spenden WHERE  projekt = ? """
        curs.execute(sqlExample, (kennung,))

    def deleteschreibt(self,kommentarid):
        curs = self.conn.cursor()
        sqlExample = """DELETE FROM schreibt WHERE  kommentar = ?"""
        curs.execute(sqlExample, (kommentarid,))

    def deletekommentar(self,id):
        curs = self.conn.cursor()
        sqlExample = """DELETE FROM kommentar WHERE  id = ?"""
        curs.execute(sqlExample, (id,))

    def deleteproject(self,kennung):
        curs = self.conn.cursor()
        sqlExample = """DELETE from projekt where kennung = ? """
        curs.execute(sqlExample, (kennung,))


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
