from pypdf import PdfReader
import logging
from page_parser import DividendPageParser

betterment_pdf = "TaxStatement_2022_1099B_DIV.pdf"
reader = PdfReader(betterment_pdf)
number_of_pages = len(reader.pages)

dividend_pages = []

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pdfconvert")

for page_num in range(number_of_pages):
    page = reader.pages[page_num]
    if "Dividends and Distributions (Detail)" in page.extract_text():
        log.info("Div page: %s", page_num +1)
        dividend_pages.append(page)

all_rows = []
for page in dividend_pages:
    rows = DividendPageParser(page).rows
    all_rows.extend(rows)

for row in all_rows:
    print(",".join(row))
