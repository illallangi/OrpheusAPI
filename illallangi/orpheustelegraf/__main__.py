from datetime import datetime
from typing import Dict

from click import STRING, command, option

from illallangi.orpheusapi import API as ORP_API, ENDPOINTDEF as ORP_ENDPOINTDEF

from telegraf_pyplug.main import datetime_tzinfo_to_nano_unix_timestamp, print_influxdb_format

METRIC_NAME: str = 'orpheus'
METRIC_DATE: str = '01.01.2020 03:00:00+0300'


@command()
@option('--api-key',
        '--orpheus-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=ORP_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
def cli(api_key, endpoint, cache):
    index = ORP_API(api_key, endpoint, cache).get_index()
    date = datetime.strptime(METRIC_DATE, '%d.%m.%Y %H:%M:%S%z')

    tags: Dict[str, str] = {
        'id': index.id,
        'username': index.username,
        'class': index.userstats.userclass
    }

    fields: Dict[str, int] = {
        'uploaded': int(index.userstats.uploaded),
        'downloaded': int(index.userstats.downloaded),
        'ratio': index.userstats.ratio,
        'requiredratio': index.userstats.requiredratio,
        'bonuspoints': index.userstats.bonuspoints,
        'bonuspointsperhour': index.userstats.bonuspointsperhour
    }

    print_influxdb_format(
        measurement=METRIC_NAME,
        tags=tags,
        fields=fields,
        nano_timestamp=datetime_tzinfo_to_nano_unix_timestamp(date)
    )


if __name__ == "__main__":
    cli()
