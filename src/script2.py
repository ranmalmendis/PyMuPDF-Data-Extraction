import fitz
import re
from datetime import datetime
import pandas as pd

# The dictionary that we are going to store the extracted texts
results = {}


def pdf_extractor(pdf_path):
    pdf = fitz.open(pdf_path)

    # Total page in the pdf
    num_of_pages = len(pdf)

    for num in range(num_of_pages):
        page = pdf[num]

        # checking the pdf format
        pdf_format = format_checker(page)

        #calling the get_data method to extract the texts based on the pdf format
        get_data(page, pdf_format)

        #printing the results
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


def get_data(page, doc_format):

    #extracting the texts with pymupdf's get_text method
    extrated_text = page.get_text("blocks")

    global results
    for item in extrated_text:
        neighbour = item[4]

        if doc_format == 1:

            if neighbour == "Policy Expiry Date (yyyy/mm/dd) & Time  \n(hh:mm)\n":
                string = extrated_text[extrated_text.index(item) + 1][4]
                results['Policy Number'] = string.split('\n')[0].strip()
                print("The poicy number extracted from the lcation is", results['Policy Number'])

                results['Effective Date'] = string.split('\n')[1][:-10].strip()
                print("Effective Date extracted from the location is", results['Effective Date'])

                results['Expiry Date'] = string.split('\n')[2][:-10].strip()
                print("Expiry Date extracted from the location is", results['Expiry Date'])

            if neighbour == "Named Insured and Postal Address\n":
                string = extrated_text[extrated_text.index(item) + 1][4]
                results['Name of Insured'] = string.split('\n')[0].strip()
                print("Named Insured extracted from the location is", results['Name of Insured'])

        if doc_format == 2:
            if neighbour == "Underwritten by\nDefinity Insurance Company\n":
                string = extrated_text[extrated_text.index(item) + 1][4]
                results['Policy Number'] = string.split(' ')[2].strip()
                print("The poicy number extracted from the lcation is", results['Policy Number'])

            if neighbour.find("Overland Water") != -1:
                string = extrated_text[extrated_text.index(item) + 1][4]
                results['Name of Insured'] = string.split('\n')[0].strip()
                print("Named Insured extracted from the location is", results['Name of Insured'])

            if neighbour == "POLICY INFORMATION\n":
                string = extrated_text[extrated_text.index(item) + 1][4]
                effective_date = string.split('\nFrom ')[1].split('to')[0]
                str_effective_date = str(pd.to_datetime(effective_date.strip()))
                formated_effective_date = str_effective_date.split(' ')[0]

                results['Effective Date'] = formated_effective_date.replace('-', '/')
                print("Effective Date extracted from the location is", results['Effective Date'])

                expiry_date = string.split('to ')[1][:-10]
                str_expiry_date = str(pd.to_datetime(expiry_date.strip()))
                formated_expiry_date = str_expiry_date.split(' ')[0]
                results['Expiry Date'] = formated_expiry_date.replace('-', '/')
                print("Expiry Date extracted from the location is", results['Expiry Date'])


def format_checker(page):
    search_string1 = page.search_for("Economical Mutual Insurance Company")
    search_string2 = page.search_for("Definity Insurance Company")

    if len(search_string1) != 0:
        pdf_format = 1
        return pdf_format

    elif len(search_string2) != 0:
        pdf_format = 2
        return pdf_format


def date_checker(dates):
    d1 = pd.to_datetime(dates[0])
    d2 = pd.to_datetime(dates[1])

    if d1 < d2:
        expiry_date = dates[1]
        global results
        results['Expiry Date'] = expiry_date
        effective_date = dates[0]
        results['Effective Date'] = effective_date


pdf_extractor('../Resources/pdf_sample_format2.pdf')

if __name__ == '__main__':
    pass
