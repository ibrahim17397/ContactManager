import xlsxwriter

def writeXlsx(ucontacts,filename):

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    contacts = [
        ['First Name','Last Name', 'Phone Number', 'Address']
    ]

    contacts.extend(ucontacts)

    row = 0
    col = 0


    for contact in (contacts):

        for col in range(4):
            worksheet.write(row, col, contact[col])
        row += 1

    workbook.close()
