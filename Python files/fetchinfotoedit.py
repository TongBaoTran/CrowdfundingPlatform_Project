import connect

class Fetchinfotoedit:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None


    def titel_status(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select titel, status from projekt where kennung=?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def vorgaengerList(self, user_email, itsown):
        curs = self.conn.cursor()
        sqlExample = """select KENNUNG, titel from projekt where ersteller = ? and kennung <> ?"""
        curs.execute(sqlExample, (user_email,itsown))
        data = curs.fetchall()
        return data

    def previousinfo(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """SELECT kennung, kategorie, titel, ersteller, CAST(beschreibung AS VARCHAR(200)) AS Beschreibung,  finanzierungslimit, status from projekt where kennung=?"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data

    def previous_vorgaenger(self, kennung):
        curs = self.conn.cursor()
        sqlExample = """select p1.vorgaenger, p2.titel
                        from projekt p1, projekt p2
                        where p1.kennung=?
                        and p1.vorgaenger = p2.kennung"""
        curs.execute(sqlExample, (kennung,))
        data = curs.fetchall()
        return data


    def updateProject1(self, projectToUpdate):
        curs = self.conn.cursor()
        sqlExample = """UPDATE  projekt
                        SET 
                            titel = ?, 
                            beschreibung = ?, 
                            finanzierungslimit = ?,
                            vorgaenger = ?,
                            kategorie = ?
                        WHERE kennung = ?"""
        curs.execute(sqlExample,(projectToUpdate.gettitel(),projectToUpdate.getbeschreibung(), projectToUpdate.getfinanzierungslimit(), projectToUpdate.getvorgaenger(), projectToUpdate.getkategorie(), projectToUpdate.getkennung()))

    def setnullfirst(self,kennung):
        curs = self.conn.cursor()
        sqlExample = """UPDATE  projekt
                        SET  vorgaenger = NULL
                        WHERE kennung = ?"""
        curs.execute(sqlExample,(kennung,))

    def updateProject2(self, projectToUpdate):
        curs = self.conn.cursor()
        sqlExample = """UPDATE  projekt
                        SET 
                            titel = ?, 
                            beschreibung = ?, 
                            finanzierungslimit = ?,
                            kategorie = ?
                        WHERE kennung = ?"""
        curs.execute(sqlExample,(projectToUpdate.gettitel(),projectToUpdate.getbeschreibung(), projectToUpdate.getfinanzierungslimit(), projectToUpdate.getkategorie(), projectToUpdate.getkennung()))

    # def updateProject3(self, titel, beschreibung, limit, kategorie, kennung):
    #     curs = self.conn.cursor()
    #     sqlExample = """UPDATE  projekt
    #                     SET
    #                         titel = ?,
    #                         beschreibung = ?,
    #                         finanzierungslimit = ?,
    #                         kategorie = ?
    #                     WHERE kennung = ?"""
    #     curs.execute(sqlExample,(titel,beschreibung,limit,kategorie,kennung))

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
