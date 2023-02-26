from pypdf import PdfReader
import logging
import re


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
page = reader.pages[20]
text = page.extract_text()

class DividendPageParser():
    def __init__(self, page):
        self.rows = []
        self.table_data_started = False
        self.partial_date = False
        self.page = page
        self.page.extract_text(visitor_text=self.visitor_body)
        self.fixup_total_line()

    def fixup_total_line(self):
        if self.rows[-1][0] == "Totals":
            if len(self.rows[-1]) ==14:
                log = logging.getLogger("totals row")
                self.rows[-1].insert(11, "-")

    def visitor_body(self, text, cm, tm, font_dict, font_size):
        log = logging.getLogger("visitor")

        log.debug("text = '%s'", text)
        log.debug(tm)
        if text == '' or text == '\n':
            return
        
        text = text.strip()
        # omit commas 
        text = text.replace(",","")
        # Find the last word of the header
        if re.match("\(Box\s+16\)", text): # unicode space may be here
            self.table_data_started = True
            return
        if not self.table_data_started:
            return

        # looks like the long name of a ticker. I hope. 
        if len(text) > 10:
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

        # if this is the totals line, then we need to add a new row and fill 
        # in two cells to preserve the alignment
        if re.match("^Totals", text):
            self.rows.append([])
            current_row = self.rows[-1]
            current_row.append(text)
            current_row.extend(["",""])
            return
        current_row.append(text)

all_rows = []
for page in dividend_pages:
    rows = DividendPageParser(page).rows
    all_rows.extend(rows)

for row in all_rows:
    print(",".join(row))
