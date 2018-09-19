from contextlib import contextmanager
import requests
import influxdb
try:
    from marketplace import sentry
except ImportError:
    sentry = None


def send_report(msg, service, **tags):
    if sentry:
        tags.update({'service': service})
        sentry.captureMessage(msg, tags=tags)


@contextmanager
def influx_error_send_report():
    try:
        yield
    except requests.exceptions.ConnectionError:
        send_report('No connect to influxdb', 'celery', reporter='influxdb')
    except influxdb.exceptions.InfluxDBClientError as e:
        send_report(e.message, 'celery', reporter='influxdb')
