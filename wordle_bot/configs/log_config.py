import logging
import os

def set_up_logging():
    LOG_FOLDER = 'logs'
    LOGFILE = 'wordle.log'
    os.makedirs(LOG_FOLDER, exist_ok=True)

    # set up logging to file
    logging.basicConfig(
        filename=f'{LOG_FOLDER}/{LOGFILE}',
        level=logging.INFO, 
        format= "[%(asctime)s] - {%(name)s - %(levelname)s} - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


