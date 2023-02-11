import sys
import argparse
from loguru import logger
from panduza_platform import MetaPlatform



import logging
logging.basicConfig(filename="/etc/panduza/log/ttt.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 


parser = argparse.ArgumentParser()
parser.add_argument('tree', nargs='?', default=None)
args = parser.parse_args()

logger.remove()
logger.add(sys.stdout, format="{level: <10}|> {message}", level="DEBUG")
logger.add("/etc/panduza/log/py.log", format="{time} | {level: <10}|> {message}", level="DEBUG", rotation="50 MB")

srv = MetaPlatform()
srv.force_log = True
srv.register_driver_plugin_discovery()
if args.tree != None:
    srv.load_tree_overide(args.tree)
srv.run()
logger.warning("Platform stopped !")
