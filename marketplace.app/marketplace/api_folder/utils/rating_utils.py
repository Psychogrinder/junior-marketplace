from marketplace import db
from marketplace.api_folder.utils.abortions import abort_if_invalid_rating_value
from marketplace.models import RatedMixin


def post_rating(rating: int, rated: RatedMixin) -> dict:
    """Posts rating for given RatedMixin instance"""
    abort_if_invalid_rating_value(rating)
    rating = rated.update_rating(rating)
    db.session.commit()
    return {'rating': rating}
