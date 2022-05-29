#!/usr/bin/env python
"""
Merges PDF documents input from directory given on command line.
"""
import datetime
import logging
import os
import typing
import uuid
from PyPDF4 import PdfFileReader, PdfFileMerger

LOG = logging.getLogger('scan_processor.pdf_merger')
LOG.setLevel(level=logging.INFO)

OUTPUT = "Merged_PDF"


def merge_pdfs(list_of_pdfs: typing.List[str], output_path) -> typing.Tuple[int, int]:
    """
    Directory to read from must be given as command line parameter
    """
    sum_pages = 0
    num_files_merged = 0
    merger = PdfFileMerger()

    for _input_file in list_of_pdfs:
        pages = PdfFileReader(_input_file).numPages

        with open(_input_file, "rb") as filehandle_write:
            merger.append(fileobj=filehandle_write, pages=(0, pages))

        sum_pages += pages
        num_files_merged += 1
        os.remove(_input_file)

    write_merged_pdf(merger, output_path)
    LOG.info("Output successfully written to %s, number of pages: %s", output_path, sum_pages)
    merger.close()

    return num_files_merged, sum_pages


def write_merged_pdf(merger, output_path):
    """
    Function writes the merged pdf to filesystem
    """
    with open(make_unique_filename(default_name=OUTPUT, output_dir=output_path), "wb") as filehandle_write:
        merger.write(filehandle_write)


def make_unique_filename(default_name: str, output_dir: str) -> str:
    """
    Function generates a unique file name and adds an uuid in case that the file name already exists
    """
    file_name_to_check = os.path.join(output_dir, f'{default_name}-{str(datetime.date.today())}')
    if os.path.exists(f'{file_name_to_check}.pdf'):
        return f'{file_name_to_check}-{str(uuid.uuid4())}.pdf'

    return f'{file_name_to_check}.pdf'
