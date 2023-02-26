from pypdf import PdfReader
import logging
import re


betterment_pdf = "TaxStatement_2022_1099B_DIV.pdf"
reader = PdfReader(betterment_pdf)
number_of_pages = len(reader.pages)

dividend_page_list = []

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pdfconvert")

for page_num in range(number_of_pages):
    page = reader.pages[page_num]
    if "Dividends and Distributions (Detail)" in page.extract_text():
        print(page_num +1)
        dividend_page_list.append(page.extract_text())
page = reader.pages[20]
text = page.extract_text()
#print(text)





class DividendPageParser():
    def __init__(self):
        self.rows = []
        self.table_data_started = False
        self.partial_date = False

    def visitor_body(self, text, cm, tm, font_dict, font_size):
        log = logging.getLogger("visitor")

        log.info("text = '%s'", text)
        log.info(tm)
        if text == '' or text == '\n':
            return
        # Find the last word of the header
        if re.match("\(Box\s+16\)", text): # unicode space may be here
            self.table_data_started = True
            return
        if not self.table_data_started:
            return

        # looks like the name of a ticker.  10 or more non digits
        if re.match("^[^\d]{10,}", text):
            self.rows.append([])

        current_row = self.rows[-1]

        # looks like an incomplete year
        if re.match("\d+-$", text):
            #parts.append(text)
            current_row.append(text)
            self.partial_date = True
            return
        # looks like the rest of the incomplete date
        if self.partial_date:
            if re.match("[\d-]+", text):
                current_row[-1] +=text
                #parts[len(parts)-1] += text
                self.partial_date = False
            return

        current_row.append(text)
parser = DividendPageParser()
page.extract_text(visitor_text=parser.visitor_body)
for row in parser.rows:
    print(",".join(row))

for page_num, div_page in enumerate(dividend_page_list):
    log.info("Dividend page %d", page_num)
#    print(div_page)