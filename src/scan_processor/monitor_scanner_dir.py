"""
Module implements a watchdog that monitors a directory for new files to process
"""
import logging
import os
import sys
import time
import threading
import typing

import zc.lockfile

# Third party modules
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# Project owned modules
from config_model import settings
import pdf_merger

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

LOG = logging.getLogger('scan_processor.directory_monitor')
LOG.setLevel(level=logging.INFO)  # Comment this line for debugging

TIMER_THREAD = None


def collect_pdfs_to_merge(scan_directory: str) -> typing.List[str]:
    """
    Function scans the scan_directory and returns a list of absolut filepathes
    """
    pdf_list = []

    if os.path.exists(scan_directory):
        file_list = os.listdir(path=scan_directory)
        pdf_list = [os.path.join(scan_directory, item) for item in file_list]

    return pdf_list


def process_files():
    """
    This function is called when the timer runs out after TIMEOUT. When this function is called:
    - Collect all *.pdf files in the defined scan directory: Done
    - merge them into one pdf in the target directory: Done
    - delete original pdfs: Done
    """
    pdf_list = collect_pdfs_to_merge(scan_directory=settings.scan_directory)
    pdf_list = [f.strip() for f in pdf_list if f.endswith('.pdf')]

    sum_pages, num_files = pdf_merger.merge_pdfs(list_of_pdfs=pdf_list, output_path=settings.output_path)
    LOG.info('Finished merging %s pdf file with %s pages.', num_files, sum_pages)


def start_timer_thread(timer):
    """
    This function is called each time a new file is detected and starts or restarts the timer after that
    pdfs are merged
    """
    if timer is not None:
        timer.cancel()
        LOG.debug('RESET timer')

    timer = threading.Timer(settings.timeout, process_files)
    timer.start()
    LOG.debug('START timer: %s', str(timer))

    return timer


def create_event_handler() -> PatternMatchingEventHandler:
    """
    Function creates and returns an event handle for the observer to monitor the file system
    """
    patterns = settings.filepattern
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True

    return PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


def on_created(event):
    """
    Event handler for CREATE event, fires when a new file is created
    """
    # pylint: disable=W0603
    global TIMER_THREAD

    if file_in_scandir(filepath=os.path.split(event.src_path)[0], scan_dir=settings.scan_directory):
        LOG.info("The file \"%s\" has been created! Starting scan processor TIMER", event.src_path)
        TIMER_THREAD = start_timer_thread(timer=TIMER_THREAD)
    else:
        LOG.debug("The file \"%s\" is not in the scan dir itself. Not processing it.", event.src_path)


def file_in_scandir(filepath: str, scan_dir: str) -> bool:
    """
    Function compares filepath (the path of the event) and scan_dir (the directory to scan for files) and returns
    True is they are identical. This test is required, because the watchdog module is monitoring directories
    recursively, not only the given directory. The recursive scan would lead to an endless loop, in case merged
    files are created ina subdirectory of scan_dir.
    """
    return filepath == scan_dir


def monitoring(monitoring_settings):
    """Main function to monitor the directory defined in monitoring_settings.directory"""
    my_event_handler = create_event_handler()
    my_event_handler.on_created = on_created
    LOG.debug('PatternMatchingEventHandler created and "on_created" eventhandler added')

    observer = Observer()
    observer.schedule(my_event_handler, monitoring_settings.scan_directory, recursive=True)
    observer.start()
    LOG.debug('Observer scheduled and started.')

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
        LOG.debug('Observer stopped')


if __name__ == "__main__":
    APPLICATION = 'ScanProcessor'
    LOCK = None

    try:
        LOCK = zc.lockfile.LockFile(f'{APPLICATION}.lock')
        LOG.info('%s started.', APPLICATION)
        monitoring(monitoring_settings=settings)
        LOCK.close()

    except zc.lockfile.LockError:
        LOG.warning('Application %s is already running and cannot run twice!', APPLICATION)
        sys.exit(-1)

    except KeyboardInterrupt:
        LOG.info('%s stpped.', APPLICATION)
