from marketplace import sentry


def send_report(msg, service, **tags):
    tags.update({'service':service})
    sentry.captureMessage(msg, tags=tags)