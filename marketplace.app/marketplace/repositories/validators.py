from flask_restful import abort


def failed_email_check(email):
    abort(406, message='Given email = \'{}\'  is invalid'.format(email))


def failed_password_len_check():
    abort(406, message='Given password is too short')


def failed_email_uniqueness_check(email):
    abort(406, message='User with given email = {} already exists'.format(email))


def failed_producer_name_uniqueness_check(name):
    abort(406, message='Producer with given name = {} already exists'.format(name))


def no_file_part_in_request():
    abort(406, message='No file part in request')


def no_image_presented():
    abort(406, message='No image presented')
