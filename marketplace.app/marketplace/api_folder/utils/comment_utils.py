from marketplace import db, COMMENTS_PER_PAGE
from marketplace.api_folder.schemas import comment_schema
from marketplace.api_folder.utils.abortions import abort_if_product_doesnt_exist_or_get, \
    abort_if_consumer_doesnt_exist_or_get, abort_if_comment_doesnt_exist_or_get, abort_if_invalid_rating_value
from marketplace.api_folder.utils.producer_utils import get_producer_by_id
from marketplace.models import Comment, Order


def get_comment_by_id(comment_id):
    return abort_if_comment_doesnt_exist_or_get(comment_id)


def get_comments_by_product_id(product_id, page=1):
    abort_if_product_doesnt_exist_or_get(product_id)
    return Comment.query.filter_by(product_id=product_id).order_by(Comment.timestamp.desc()).paginate(page,
                                                                                                      COMMENTS_PER_PAGE,
                                                                                                      False)


def get_comments_by_consumer_id(consumer_id, page):
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    return Comment.query.filter_by(consumer_id=consumer_id).order_by(Comment.timestamp.desc()).paginate(page,
                                                                                                        COMMENTS_PER_PAGE,
                                                                                                        False)


def post_comment(args):
    abort_if_invalid_rating_value(int(args['rating']))
    product = abort_if_product_doesnt_exist_or_get(args['product_id'])
    producer = get_producer_by_id(product.producer_id)
    abort_if_consumer_doesnt_exist_or_get(args['consumer_id'])
    new_comment = comment_schema.load(args).data
    db.session.add(new_comment)
    order = Order.query.filter_by(id=args['order_id']).first()
    order.reviewed = True
    product.update_rating(int(args['rating']))
    producer.update_rating(int(args['rating']))
    db.session.commit()
    return new_comment


def delete_comment_by_id(comment_id):
    comment = get_comment_by_id(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Comment with id {} has been deleted".format(comment_id)}
