import logging

# set up logging to file
logging.basicConfig(
     filename='logs/wordle.log',
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

logger = logging.getLogger(__name__)
