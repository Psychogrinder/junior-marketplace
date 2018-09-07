from marketplace.api_folder.utils import user_utils, producer_utils
from marketplace.api_folder.utils.abortions import failed_email_uniqueness_check, failed_producer_name_uniqueness_check


def check_email_uniqueness(email):
    if user_utils.get_user_by_email(email) is not None:
        failed_email_uniqueness_check()


def check_producer_name_uniqueness(name):
    if producer_utils.get_producer_by_name(name) is not None:
        failed_producer_name_uniqueness_check()
