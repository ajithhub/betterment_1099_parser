2022 Bettermment 1099-DIV parser
-------------------------------

Apparently there is no CSV version of the dividend payment details available
directly from Betterment.  This script will parse the PDF to create CSV output

This only works with the 2022 1099 from Betterment.   Writes to CSV to stdout

 - Filename is hard-coded right now
 - Looks for "Box 16" line to know when data starts, this is different from previous years
 - only depends on `pypdf` which is pure python so easy to install without building and native libraries or other dependencies


Usage
------

    pip install pypdf
    python process.py
