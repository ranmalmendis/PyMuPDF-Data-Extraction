import fitz
import re
from datetime import datetime
import pandas as pd
from dateutil import parser

name = ""
policy_num = ""
effective_date = ""
expiry_date = ""

print(fitz.__doc__)
results = {}


def pdf_extractor(pdf_path):
    pdf = fitz.open(pdf_path)

    # Total page in the pdf
    num_of_pages = len(pdf)

    # print('The number of pages is ', len(pdf))
    # taking page for further processing

    for num in range(num_of_pages):
        page = pdf[num]

        # get all annotations on a page
        annots = page.annots()
        # looping through annotations
        highlighted_contents = []
        for a in annots:

            # checking the annotation type is 'highlighted'
            if a.type[0] == 8:
                arr = []
                highlighted_coordinates = a.rect
                arr.append(highlighted_coordinates.x0 - 4)
                arr.append(highlighted_coordinates.y0 - 4)
                arr.append(highlighted_coordinates.x1 + 4)
                arr.append(highlighted_coordinates.y1 + 4)
                text = page.get_textbox(arr)
                # get text from rectangle

                # to remove the unnecessary spaces in the start and the end of the word
                clean_txt = text.strip()
                highlighted_contents.append(clean_txt)

        name_regex = re.compile(r"^([A-Za-z \-]{2,25})+$", re.MULTILINE)
        number_regex = re.compile(r"^[-+]?[0-9]+$")
        date_regex1 = re.compile(r"^\d{4}\/\d{2}\/\d{2}")
        date_regex2 = re.compile(r"^[A-Za-z]{2,10}\s\d{2}\,\s\d{4}$")

        dates = []

        for i in highlighted_contents:
            if name_regex.match(i):
                global name
                name = i
                results['Name of Insured'] = name

            elif number_regex.match(i):
                global policy_num
                policy_num = i
                results['Policy Number'] = policy_num

            elif date_regex1.match(i):
                dates.append(i[:-1])

            elif date_regex2.match(i):
                date_time = parser.parse(i)
                # print('date time', date_time)
                strdate = str(pd.to_datetime(i))
                formated = strdate.split(' ')[0]
                dates.append(formated.replace('-', '/'))

        # print('dates are ', dates)
        date_checker(dates)

        print(f'''
        ----------------------------------------------------------------------------------------
        Sample PDF Output:
    
        Name of Insured: {results['Name of Insured']}
        Policy Number: {results['Policy Number']}
        Effective Date: {results['Effective Date']}
        Expiry Date: {results['Expiry Date']}
        ----------------------------------------------------------------------------------------
        '''
              )
        return results


def date_checker(dates):
    d1 = pd.to_datetime(dates[0])
    d2 = pd.to_datetime(dates[1])

    if d1 < d2:
        global expiry_date
        expiry_date = dates[1]
        global results
        results['Expiry Date'] = expiry_date
        global effective_date
        effective_date = dates[0]
        results['Effective Date'] = effective_date


pdf_extractor('../Resources/pdf_sample_format1.pdf')

if __name__ == '__main__':
    pass
