from typing import Dict

from click import STRING, command, option

from illallangi.orpheusapi import API as ORP_API, ENDPOINTDEF as ORP_ENDPOINTDEF

from telegraf_pyplug.main import print_influxdb_format

METRICNAMEDEF = 'orpheus'


@command()
@option('--metric-name',
        type=STRING,
        required=False,
        default=METRICNAMEDEF)
@option('--api-key',
        '--orpheus-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=ORP_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
def cli(metric_name, api_key, endpoint, cache):
    index = ORP_API(api_key, endpoint, cache, success_expiry=600).get_index()

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
        measurement=metric_name,
        tags=tags,
        fields=fields,
        add_timestamp=True
    )


if __name__ == "__main__":
    cli()
