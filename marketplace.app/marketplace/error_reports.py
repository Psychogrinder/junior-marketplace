from marketplace import sentry, app


def send_report(msg, service, **tags):
    if app.config['SENTRY_DSN']:
        tags.update({'service': service})
        sentry.captureMessage(msg, tags=tags)
