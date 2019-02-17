#!/usr/bin/env python3

import click
import m3u8


@click.command()
@click.option('--url', help='URL to HLS m3u8 playlist.')
@click.option('--freq', default=10, help="Frequency for downloading m3u8 stream")
def fetch_hls_stream(url, freq):
    dynamicplaylist = m3u8.loads(url)


if __name__ == '__main__':
    fetch_hls_stream()
