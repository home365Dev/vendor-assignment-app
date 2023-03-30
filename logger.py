# import watchtower
import logging
from logging import *
from cloud_watch_logs import CloudWatchLogger
import configuration as config

logger = CloudWatchLogger(log_group='Vendor_Assignment_App', log_stream='conversation')

# name_str = '[{}]'.format(str(config.ENV_PREFIX))
# basicConfig(
#     format='{} %(asctime)s %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s'.format(name_str),
#     datefmt='%H:%M:%S',
#     level=INFO)
#
# logger = getLogger(__name__)
# # logger.addHandler(StreamHandler(stream=sys.stdout))
# # if not config.IS_TEST:
# #     logger.addHandler(watchtower.CloudWatchLogHandler())
#
# if config.IS_TEST:
#     logger.setLevel(logging.DEBUG)
# else:
#     logger.setLevel(logging.INFO)
logger.info("Log has started")
