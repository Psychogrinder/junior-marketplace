import flask_sqlalchemy
from flask import request


def get_meta_from_page(page_number: int, page: flask_sqlalchemy.Pagination) -> dict:
    return {'page': page_number, 'has_next': page.has_next, 'has_prev': page.has_prev}


def get_page_number() -> int:
    """Returns page number from request"""
    page = request.args.get('page', type=int, default=1)
    return page if page > 0 else 1
