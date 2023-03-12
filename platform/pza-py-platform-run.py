import sys
import argparse
from loguru import logger
from panduza_platform import MetaPlatform


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tree',  nargs='?', default=None)
parser.add_argument('-r', '--run-dir',nargs='?', default="/etc")
args = parser.parse_args()

logger.remove()
logger.add(sys.stdout, format="{level: <10}|{extra[driver_name]: <10}> {message}", level="DEBUG")
logger.add(f"{args.run_dir}/panduza/log/py.log", format="{level: <10}|{extra[driver_name]: <10}> {message}", level="DEBUG", rotation="50 MB")

srv = MetaPlatform(args.run_dir)
srv.force_log = True
srv.register_driver_plugin_discovery()
if args.tree != None:
    srv.load_tree_overide(args.tree)
srv.run()
logger.warning("Platform stopped !")
