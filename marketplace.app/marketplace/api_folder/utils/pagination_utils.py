from flask import request


def get_meta_from_page(page_number, page):
    return {'page': page_number, 'has_next': page.has_next, 'has_prev': page.has_prev}


def get_page_number():
    page = request.args.get('page', type=int, default=1)
    return page if page > 0 else 1
