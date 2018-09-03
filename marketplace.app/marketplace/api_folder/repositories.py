from marketplace import db
from marketplace.repositories.consumer_repository import ConsumerRepository
from marketplace.repositories.producer_repository import ProducerRepository

consumer_repository = ConsumerRepository(db.session)
producer_repository = ProducerRepository(db.session)