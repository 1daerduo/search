import re
import openpyxl

def search_excel(file_path, key):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    result = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0] and re.search(str(key), str(row[1])):
            result.append(row[0])
    return result