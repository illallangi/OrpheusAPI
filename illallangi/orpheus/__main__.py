from sys import stderr

from click import Choice as CHOICE, STRING, group, option

from loguru import logger

from notifiers.logging import NotificationHandler

from illallangi.orpheusapi import API as ORP_API, ENDPOINTDEF as ORP_ENDPOINTDEF


@group()
@option('--log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        envvar='HARVESTR_LOG_LEVEL',
        default='DEBUG')
@option('--slack-webhook',
        type=STRING,
        envvar='SLACK_WEBHOOK',
        default=None)
@option('--slack-username',
        type=STRING,
        envvar='SLACK_USERNAME',
        default='Harvestr')
@option('--slack-format',
        type=STRING,
        envvar='SLACK_FORMAT',
        default='{message}')
def cli(log_level, slack_webhook, slack_username, slack_format):
    logger.remove()
    logger.add(stderr, level=log_level)

    if slack_webhook:
        params = {
            "username": slack_username,
            "webhook_url": slack_webhook
        }
        slack = NotificationHandler("slack", defaults=params)
        logger.add(slack, format=slack_format, level="SUCCESS")


@cli.command(name='get-index')
@option('--api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=ORP_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
def get_index(api_key, endpoint, cache):
    logger.info(ORP_API(api_key, endpoint, cache).get_index())


if __name__ == "__main__":
    cli()
