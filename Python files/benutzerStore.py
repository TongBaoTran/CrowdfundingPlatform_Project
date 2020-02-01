import connect


class BenutzerStore:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def addUser(self, userToAdd):
        curs = self.conn.cursor()
        sqlExample = "INSERT INTO benutzer (email, name, beschreibung) VALUES(?,?,?)"
        curs.execute(sqlExample, (userToAdd.getemail(), userToAdd.getname(),userToAdd.getbeschreibung()))

    def addKonto(self, kontoToAdd):
        curs = self.conn.cursor()
        sqlExample = "INSERT INTO konto (inhaber, guthaben, geheimzahl) VALUES(?,?,?)"
        curs.execute(sqlExample, (kontoToAdd.getinhaber(), kontoToAdd.getguthaben(),kontoToAdd.getgeheimzahl()))

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
