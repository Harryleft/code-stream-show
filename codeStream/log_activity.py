import logging

# Configure logging
logging.basicConfig(filename='study_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def log_activity(activity):
    logging.info(activity)