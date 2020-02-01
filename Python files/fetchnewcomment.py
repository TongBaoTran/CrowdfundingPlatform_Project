import connect

class Fetchnewcomment:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def titel(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select titel from projekt where kennung = ?"""
        curs.execute(sqlExample,(kennung,))
        data = curs.fetchall()
        return data


    def maxid(self):
        curs = self.conn.cursor()
        sqlExample = """select max(id) from kommentar"""
        curs.execute(sqlExample)
        data = curs.fetchall()
        return data

    def addKommentar(self, kommentartoAdd):
        curs = self.conn.cursor()
        sqlExample = """INSERT INTO kommentar (id, text, sichtbarkeit) VALUES (?, ?, ?)"""
        curs.execute(sqlExample, (kommentartoAdd.getid(), kommentartoAdd.gettext(),kommentartoAdd.getsichtbarkeit()))

    def addSchreibt(self, schreibttoAdd):
        curs = self.conn.cursor()
        sqlExample = """INSERT INTO schreibt (benutzer, projekt, kommentar) VALUES (?, ?, ?)"""
        curs.execute(sqlExample, (schreibttoAdd.getbenutzer(), schreibttoAdd.getprojekt(), schreibttoAdd.getkommentar()))

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
