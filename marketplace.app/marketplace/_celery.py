from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from celery.signals import task_failure, worker_shutting_down
from celery.task import periodic_task

from marketplace.error_reports import send_report


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_BACKEND_URL'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def setup_periodic_tasks():
    return {
        'collect-stat-every-two-hours': {
            'task': 'marketplace.collect_statistics.send_users_count_stat',
            'schedule': crontab(hour='*/2')
        },
        'collect-stat-every-three-hours': {
            'task': 'marketplace.collect_statistics.send_orders_stat',
            'schedule': crontab(hour='*/3')
        },
        'generate-sitemap-every-day': {
            'task': 'marketplace.sitemap_tools.generate_sitemap',
            'schedule': crontab(hour='*/24')
        }
    }


@task_failure.connect
def task_failure_report_send(sender=None, exception=None, **kwargs):
    msg = f'Celery. Task {sender} fail with exception {exception}'
    send_report(msg, 'celery', reporter='celery', celery='task')


@worker_shutting_down.connect
def worker_shutdown_report_send(sig=None, exitcode=None, how=None, **kwargs):
    msg = f'Celery. Worker shutting down with exitcode {exitcode}, signal - {sig}'
    send_report(msg, 'celery', reporter='celery', celery='worker')
