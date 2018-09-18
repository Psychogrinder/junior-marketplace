try:
    from marketplace import sentry
except ImportError:
    sentry = None


def send_report(msg, service, **tags):
    if sentry:
        tags.update({'service': service})
        sentry.captureMessage(msg, tags=tags)
