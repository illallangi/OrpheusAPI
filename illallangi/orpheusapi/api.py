from click import get_app_dir

from diskcache import Cache

from loguru import logger

from requests import get as http_get, HTTPError

from yarl import URL

from .tokenbucket import TokenBucket
from .index import Index

ENDPOINTDEF = 'https://orpheus.network/'
EXPIRE = 7 * 24 * 60 * 60


class API(object):
    def __init__(self, api_key, endpoint=ENDPOINTDEF, cache=True, config_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.endpoint = URL(endpoint) if not isinstance(endpoint, URL) else endpoint
        self.cache = cache
        self.config_path = get_app_dir(__package__) if not config_path else config_path
        self.bucket = TokenBucket(10, 5 / 10)

    def get_index(self):
        with Cache(self.config_path) as cache:
            if not self.cache or __name__ not in cache:
                self.bucket.consume()
                logger.trace(__name__)
                try:
                    r = http_get(
                        self.endpoint / 'ajax.php' % {'action': 'index'},
                        headers={
                            'User-Agent': 'illallangi-orpheusapi/0.0.1',
                            'Authorization': f'token {self.api_key}'
                        })
                    r.raise_for_status()
                except HTTPError as http_err:
                    logger.error(f'HTTP error occurred: {http_err}')
                    return
                except Exception as err:
                    logger.error(f'Other error occurred: {err}')
                    return
                logger.debug('Received {0} bytes from API'.format(len(r.content)))

                logger.trace(r.request.url)
                logger.trace(r.request.headers)
                logger.trace(r.headers)
                logger.trace(r.text)
                cache.set(
                    __name__,
                    r.json()['response'],
                    expire=EXPIRE)
            return Index(cache[__name__])
