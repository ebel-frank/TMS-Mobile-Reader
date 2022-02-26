import sqlite3
import datetime


class TmsDatabase:
    def __init__(self, path):
        """creates a database in the specified path
        """
        self.path = path
        con = None
        try:
            con = sqlite3.connect(path + "TMS_database.db")
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tmsTable(filename TEXT, open_count INT, timestamp TEXT, starred BOOL)
                """)
            con.commit()
        except sqlite3.Error:
            if con:
                print("Error! Rolling back changes")
                con.rollback()
        finally:
            if con:
                con.close()

    def get_file_names(self, sort_type: int):
        """
        :param sort_type: 0 to sort alphabetically or 1 to sort by date
        :return: a list of all filename and its timestamp
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        if sort_type:
            statement = "SELECT filename, timestamp FROM tmsTable ORDER BY filename ASC"
        else:
            statement = "SELECT filename, timestamp FROM tmsTable ORDER BY timestamp ASC"
        data = con.cursor().execute(statement).fetchall()
        con.close()
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][1] = get_time(data[i][1])
        return data

    def get_starred_files(self):
        """
        :return: a list of all filenames that are starred
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        data = con.cursor().execute("SELECT filename FROM tmsTable WHERE starred = 1").fetchall()
        con.close()
        return data

    def set_timestamp(self, filename):
        """ updates the timestamp of the filename to the current time
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        con.cursor().execute(
            f"UPDATE tmsTable SET timestamp = ?, open_count = open_count + ? WHERE filename = ?",
            (str(datetime.datetime.today()).split('.')[0], 1, filename)
        )
        con.commit()
        con.close()

    def set_starred(self, filename):
        con = sqlite3.connect(self.path + "TMS_database.db")
        con.cursor().execute(
            f"UPDATE tmsTable SET starred = CASE WHEN open_count > 15 THEN 1 ELSE NOT starred END WHERE filename = ?",
            filename
        )
        con.commit()
        con.close()

    def sync_db(self, filenames):
        """
        Inserts a filename into database that is not in database file and removes a filename
        from database file that is not in filenames
        :param filenames: a list of filenames
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        cur = con.cursor()
        filename = ["%s" % x for x in cur.execute("SELECT filename FROM tmsTable").fetchall()]
        for i in filenames:
            if i not in filename:
                cur.execute("INSERT INTO tmsTable VALUES(?,?,?,?)",
                            (i, 0, str(datetime.datetime.today()).split('.')[0], 0))
        con.commit()
        filename = ["%s" % x for x in cur.execute("SELECT filename FROM tmsTable").fetchall()]
        for i in filename:
            if i not in filenames:
                cur.execute("DELETE FROM tmsTable WHERE filename = ?", (i,))
        con.commit()
        con.close()

    def insert_files(self, filenames):
        """
        Inserts a list of filenames into database
        :param filenames: a list of filenames
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        for i in filenames:
            con.cursor().execute(
                "INSERT INTO tmsTable VALUES(?,?,?,?)", (i, 0, str(datetime.datetime.today()).split('.')[0], 0)
            )
        con.commit()
        con.close()

    def remove_file(self, filename):
        """ Removes the given filename from the database
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        con.cursor().execute(f"DELETE FROM tmsTable WHERE filename = ?", (filename,))
        con.commit()
        con.close()


def get_time(timestamp):
    d1 = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.datetime.today()
    diff = (d2 - d1).days
    if diff == 0:
        return "Today"
    elif diff == 1:
        return "Yesterday"
    elif diff > 7:
        return "A long time ago"
    else:
        return f"{diff} days ago"


# if __name__ == "__main__":
#     val = TmsDatabase("dev/")
