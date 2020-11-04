import openpyxl
def generateQuestions(n=1628):

    if(n > 1628):
        n = 1628

    questions={}
    book = openpyxl.load_workbook('questions.xlsx')
    sheet = book.active

    for i in range(2, n):
        questions[sheet['A' + str(i)].value] = sheet['B' + str(i)].value
        questions[sheet['D' + str(i)].value] = sheet['E' + str(i)].value
        questions[sheet['G' + str(i)].value] = sheet['H' + str(i)].value
    
    return questions