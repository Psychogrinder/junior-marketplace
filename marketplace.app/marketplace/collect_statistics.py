from marketplace.models import User, Order
from marketplace import celery, influx_client
from datetime import datetime
from marketplace.error_reports import influx_error_send_report


def set_metric_point(measurement, data, timestamp):
    return {
        "measurement": measurement,
        "tags": {k: v for k, v in data['tags'].items()},
        "time": timestamp,
        "fields": {k: v for k, v in data['fields'].items()}
    }


def get_users_by_entity(entity):
    return User.query.filter_by(entity=entity)


def count_users(users):
    return users.count()


def get_users_email_confirmed_count(users):
    return users.filter_by(email_auth_status=True).count()


def collect_users_count_stat():
    producers = get_users_by_entity('producer')
    consumer = get_users_by_entity('consumer')
    return [
        {'fields': {'producers_count': count_users(producers)}, 'tags': {'entity': 'producer'}},
        {
            'fields': {'producers_email_confirmed_count': get_users_email_confirmed_count(producers)},
            'tags': {'entity': 'producer'}
        },
        {
            'fields': {'consumers_count': count_users(consumer)},
            'tags': {'entity': 'consumer'}
        },
        {
            'fields': {'consumer_email_confirmed_count': get_users_email_confirmed_count(consumer)},
            'tags': {'entity': 'consumer'}
        }
    ]


def collect_orders_stat():
    order_status = ['Не обработан', 'Обрабатывается', 'Отправлен', 'Готов к самовывозу', 'Завершён']
    orders = Order.query
    orders_count = orders.count()
    points = [{'fields': {'orders_count': orders_count}, 'tags': {'orders': 'all_orders', 'status': 'all'}}]
    for status in order_status:
        count = orders.filter_by(status=status).count()
        points.append(
            {'fields': {'orders_count': count}, 'tags': {'status': status, 'orders': 'by_status'}}
        )
    return points


@celery.task(name='collect_statistics.send_orders_stat')
def send_orders_stat():
    points = []
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for stat in collect_orders_stat():
        points.append(set_metric_point('order', stat, timestamp))
    with influx_error_send_report():
        influx_client.write_points(points)


@celery.task(name='collect_statistics.send_users_count_stat')
def send_users_count_stat():
    points = []
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for stat in collect_users_count_stat():
        points.append(set_metric_point('users', stat, timestamp))
    with influx_error_send_report():
        influx_client.write_points(points)
