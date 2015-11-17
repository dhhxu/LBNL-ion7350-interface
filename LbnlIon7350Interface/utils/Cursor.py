"""
Custom implementation of Python context manager for the cursor (and
connection) objects. This implementation avoids committing queries,
unlike the default pyodbc behavior, which is to always commit.
"""

import pyodbc

class Cursor(object):
    def __init__(self, cnxn_str):
        self.cnxn = pyodbc.connect(cnxn_str)
        self.cursor = self.cnxn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        del self.cursor
        self.cnxn.close()

