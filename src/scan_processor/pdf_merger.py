#!/usr/bin/env python
"""
Merges PDF documents input from directory given on command line.
"""
import datetime
import logging
import os
import os.path
import typing
import uuid
from PyPDF4 import PdfFileReader, PdfFileMerger


LOG = logging.getLogger('scan_processor.pdf_merger')
LOG.setLevel(level=logging.INFO)


output = "Merged_PDF"


def merge_pdfs(list_of_pdfs: typing.List[str], output_path):
    """
    Directory to read from must be given as command line parameter
    """
    sum_pages = 0
    merger = PdfFileMerger()

    for _input_file in list_of_pdfs:
        pages = PdfFileReader(_input_file).numPages
        sum_pages += pages
        merger.append(fileobj=open(_input_file, "rb"), pages=(0, pages))

        os.remove(_input_file)

    merger.write(open(make_filename(default_name=output, output_dir=output_path), "wb"))
    LOG.info("Output successfully written to %s, number of pages: %s", output_path, sum_pages)

    merger.close()


def make_filename(default_name, output_dir):
    """
    Function generates a valid file name and adds an uuid in case that the file name already exists
    """
    file_name_to_check = os.path.join(output_dir, f'{default_name}-{str(datetime.date.today())}')
    if os.path.exists(f'{file_name_to_check}.pdf'):
        return f'{file_name_to_check}-{str(uuid.uuid4())}.pdf'
    else:
        return f'{file_name_to_check}.pdf'
