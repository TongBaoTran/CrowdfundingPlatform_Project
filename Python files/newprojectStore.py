import connect


class NewprojectStore:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def maxkennung(self):
        curs = self.conn.cursor()
        sqlExample = "select max(kennung) from projekt"
        curs.execute(sqlExample)
        data = curs.fetchall()
        return data

    def addProject1(self, projectToAdd):
        curs = self.conn.cursor()
        sqlExample = "INSERT INTO projekt (kennung, titel, beschreibung, finanzierungslimit, ersteller, vorgaenger, kategorie) VALUES (?, ?, ?, ?, ?, ?, ?)"
        curs.execute(sqlExample, (projectToAdd.getkennung(), projectToAdd.gettitel(), projectToAdd.getbeschreibung(), projectToAdd.getfinanzierungslimit(), projectToAdd.getersteller(), projectToAdd.getvorgaenger(), projectToAdd.getkategorie()))

    def addProject2(self, projectToAdd):
        curs = self.conn.cursor()
        sqlExample = "INSERT INTO projekt (kennung, titel, beschreibung, finanzierungslimit, ersteller, kategorie) VALUES (?, ?, ?, ?, ?, ?)"
        curs.execute(sqlExample, (projectToAdd.getkennung(), projectToAdd.gettitel(), projectToAdd.getbeschreibung(), projectToAdd.getfinanzierungslimit(), projectToAdd.getersteller(), projectToAdd.getkategorie()))

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
