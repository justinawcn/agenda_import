import xlrd
from db_table import db_table

"""
book = xlrd.open_workbook("agenda.xls")
print("The number of worksheets is {0}".format(book.nsheets))
print("Worksheet name(s): {0}".format(book.sheet_names()))
sh = book.sheet_by_index(0)
print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
print(sh.row(15))
item = []
for elem in sh.row(15):
    print(str(elem).split("'")[1])
# for rx in range(14, sh.nrows):
    # print(sh.row(rx))
"""


class parse_xls:

    TABLE_NAME = "agenda"
    SCHEMA = {"id": "integer primary key autoincrement",
              "date": "text not null",
              "time_start": "text not null",
              "time_end": "text not null",
              "session_or_sub": "text not null",
              "title": "text not null",
              "location": "text",
              "description": "text",
              "speakers": 'text',
              "parent_id": "integer, foreign key(parent_id) references 'agenda'(id) on delete cascade"
              }
    COLUMNS_QUERY = "date, time_start, time_end, session_or_sub, title, location, description, speakers"
    SUBSESSION_QUERY = "date, time_start, time_end, session_or_sub, title, location, description, speakers, parent_id"
    

    def __init__(self, fileName):
        # expecting one file at a time
        try:
            book = xlrd.open_workbook(fileName)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)=}")
            raise

        self.book = book
        self.fileName = self.book.sheet_names()[0]
        self.sheet = self.book.sheet_by_index(0)
        self.table = None

        self.importToDb()


    def importToDb(self):
        self.table = db_table(self.TABLE_NAME, self.SCHEMA)
        id = 0
        for rowidx in range(15, self.sheet.nrows):
            item = []
            for elem in self.sheet.row(rowidx):
                data = str(elem).split("'")[1]
                item.append(data)
                if data == "Session":
                    id = rowidx - 14
            if item[3] == "Session":
                self.table.insert(self.COLUMNS_QUERY, item)
            elif item[3] == "Sub":
                item.append(id)
                self.table.insert(self.SUBSESSION_QUERY, item)
            else:
                raise RuntimeError("invalid data for session/sub-session type.")
            


# """

if __name__=="__main__":
    agenda = parse_xls("agenda.xls")