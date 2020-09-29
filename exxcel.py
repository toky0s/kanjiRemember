import xlrd 
  
loc = ("excel_kanji.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
print(sheet.row_values(2)) 