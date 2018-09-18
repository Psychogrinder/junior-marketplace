import re

from marketplace.api_folder.utils.abortions import failed_email_check, failed_password_len_check


def validate_registration_data(email: str, password: str) -> bool:
    """
    Checks if email required to email regex
    Checks password length
    """
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_pattern, email):
        failed_email_check(email)
    if len(password) < 6:
        failed_password_len_check()
    return True
