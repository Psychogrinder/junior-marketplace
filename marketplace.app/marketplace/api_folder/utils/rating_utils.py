from marketplace import db
from marketplace.api_folder.utils.abortions import abort_if_invalid_rating_value


def post_rating(rating, rated):
    abort_if_invalid_rating_value(rating)
    rating = rated.update_rating(rating)
    db.session.commit()
    return {'rating': rating}
