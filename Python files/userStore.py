import connect


class UserStore:

    def __init__(self):
        #dbUtil = connect.DBUtil().getExternalConnection("testdb")
        self.conn = connect.DBUtil().getExternalConnection("testdb")
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    # PREPARED STATEMENT (WITH PLACEHOLDERS)
    def addUser(self, userToAdd):
        curs = self.conn.cursor()
        sqlExample = "INSERT INTO USER (firstname, lastname) VALUES(?, ?)"
        curs.execute(sqlExample, (userToAdd.getFirstName(), userToAdd.getLastName()))

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
