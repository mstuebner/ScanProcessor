"""
Module implements a watchdog that monitors a directory for new files to process
"""
import logging
import sys
import time
import threading
import zc.lockfile

# Third party modules
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# Project owned modules
from config_model import settings

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

LOG = logging.getLogger('scan_processor.directory_monitor')
LOG.setLevel(level=logging.INFO)

TIMEOUT = 10
TIMER_THREAD = None


def process_files(filepath: str):
    """
    When this function is called:
    - Colled all *.pdf files in the defined directory
    - merge them into one pdf in the target directory
    - delete original pdfs
    """
    LOG.info(f"{filepath}")
    LOG.info('MERGE finished')


def start_timer_thread(timer):
    """
    This function is called each time a new file is detected and starts or restarts the timer after that
    pdfs are merged
    """
    if timer is not None:
        timer.cancel()
        LOG.debug('RESET timer')

    timer = threading.Timer(TIMEOUT, process_files, [settings])
    timer.start()
    LOG.debug('START timer')

    return timer


def create_event_handler():
    patterns = ["*.txt"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True

    return PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


def on_created(event):
    """Event handler for CREATE event, fires when a new file is created"""
    global TIMER_THREAD

    LOG.info("The file \"%s\" has been created! Starting scan processor time", event.src_path)
    TIMER_THREAD = start_timer_thread(timer=TIMER_THREAD)


def monitoring(monitoring_settings):
    """Main function to monitor the directory defined in monitoring_settings.directory"""
    my_event_handler = create_event_handler()
    LOG.debug('PatternMatchingEventHandler created')

    my_event_handler.on_created = on_created
    LOG.debug('"on_created" eventhandler added')

    observer = Observer()
    observer.schedule(my_event_handler, monitoring_settings.directory, recursive=True)
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
