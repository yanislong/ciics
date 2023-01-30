#!/usr/bin/env python3

import xlrd

def read():
    wb = xlrd.open_workbook(filename='./excel/interfacedata.xlsx')
    print(wb.sheet_names())
    s1 = wb.sheet_by_index(0)
    for i in range(s1.nrows):
        row = s1.row_values(i)
        print(row)
#    col = s1.col_values(1)
    print(row)
#    print(col)
#    print(s1.ncols)

if __name__ == "__main__":
    read()
