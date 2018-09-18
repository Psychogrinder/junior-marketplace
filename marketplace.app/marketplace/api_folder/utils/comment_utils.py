from marketplace import db, COMMENTS_PER_PAGE
from marketplace.api_folder.schemas import comment_schema
from marketplace.api_folder.utils.abortions import abort_if_product_doesnt_exist_or_get, \
    abort_if_consumer_doesnt_exist_or_get, abort_if_comment_doesnt_exist_or_get
from marketplace.models import Comment, Order


def get_comment_by_id(comment_id: int) -> Comment:
    """Returns comment with given id"""
    return abort_if_comment_doesnt_exist_or_get(comment_id)


def get_comments_by_product_id(product_id: int, page: int = 1) -> list:
    """Returns page of comments for product"""
    abort_if_product_doesnt_exist_or_get(product_id)
    return Comment.query.filter_by(product_id=product_id).order_by(Comment.timestamp.desc()).paginate(page,
                                                                                                      COMMENTS_PER_PAGE,
                                                                                                      False)


def get_comments_by_consumer_id(consumer_id: int, page: int = 1) -> list:
    """Returns page of comments for consumer"""
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    return Comment.query.filter_by(consumer_id=consumer_id).order_by(Comment.timestamp.desc()).paginate(page,
                                                                                                        COMMENTS_PER_PAGE,
                                                                                                        False)


def post_comment(args: dict) -> Comment:
    """Create and returns comment by given args"""
    abort_if_product_doesnt_exist_or_get(args['product_id'])
    abort_if_consumer_doesnt_exist_or_get(args['consumer_id'])
    new_comment = comment_schema.load(args).data
    db.session.add(new_comment)
    order = Order.query.filter_by(id=args['order_id']).first()
    order.reviewed = True
    db.session.commit()
    return new_comment


def delete_comment_by_id(comment_id: int) -> dict:
    """Delete comment with given id"""
    comment = get_comment_by_id(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Comment with id {} has been deleted".format(comment_id)}
