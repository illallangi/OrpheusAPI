# OrpheusAPI
[![Docker Pulls](https://img.shields.io/docker/pulls/illallangi/orpheusapi.svg)](https://hub.docker.com/r/illallangi/orpheusapi)
[![Image Size](https://images.microbadger.com/badges/image/illallangi/orpheusapi.svg)](https://microbadger.com/images/illallangi/orpheusapi)
![Build](https://github.com/illallangi/OrpheusAPI/workflows/Build/badge.svg)

Tool and Python bindings for the [Orpheus](https://orpheus.network) [API](https://github.com/OPSnet/Gazelle/wiki/JSON-API-Documentation).

## Installation

```shell
pip install git+git://github.com/illallangi/OrpheusAPI.git
```

## Usage

```shell
$ orpheus-tool
Usage: orpheus-tool [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG|SUCCESS|TRACE]
  --slack-webhook TEXT
  --slack-username TEXT
  --slack-format TEXT
  --help                          Show this message and exit.

Commands:
  get-directory
  get-group
  get-index
  get-torrent
  rename-torrent-file
```
