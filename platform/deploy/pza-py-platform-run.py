import sys
import argparse
from loguru import logger
from panduza_platform import MetaPlatform


# fmt='[%(name)s] %(asctime)s %(funcName)s %(lineno)-3d  %(message)s',

import coloredlogs, logging
coloredlogs.install(level='DEBUG', isatty=True,
    fmt='%(levelname)-10s|%(name)-10s> %(message)s',
    # level_styles=dict(
    #     debug=dict(color='white'),
    #     info=dict(color='blue'),
    #     warning=dict(color='yellow', bright=True),
    #     error=dict(color='red', bold=True, bright=True),
    #     critical=dict(color='black', bold=True, background='red'),
    # ),
    # field_styles=dict(
    #     name=dict(color='white'),
    #     asctime=dict(color='white'),
    #     funcName=dict(color='white'),
    #     lineno=dict(color='white'),
    # )
    )




parser = argparse.ArgumentParser()
parser.add_argument('tree', nargs='?', default=None)
args = parser.parse_args()

logger.remove()
logger.add(sys.stdout, format="{level: <10}|{extra[driver_name]: <10}> {message}", level="DEBUG")
logger.add("/etc/panduza/log/py.log", format="{time} | {level: <10}|{extra[driver_name]: <10}> {message}", level="DEBUG", rotation="50 MB")

srv = MetaPlatform()
srv.force_log = True
srv.register_driver_plugin_discovery()
if args.tree != None:
    srv.load_tree_overide(args.tree)
srv.run()
logger.warning("Platform stopped !")
