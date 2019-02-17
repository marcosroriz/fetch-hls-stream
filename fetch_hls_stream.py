#!/usr/bin/env python3

import logging

import click
import m3u8

# Set representing chunks that we have already downloaded
dlset = set()


def setuplog(verbose):
    log_msg_format = '%(asctime)s :: %(name)20s :: %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=log_msg_format, datefmt=log_date_format)
    logger = logging.getLogger("fetch_hls_stream")
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


@click.command()
@click.option('--url', help='URL to HLS m3u8 playlist.')
@click.option('--freq', default=10,
              help="Frequency for downloading the HLS m3u8 stream")
@click.option('--output', default="./", type=click.Path(exists=True),
              help="Output directory for video files")
@click.option('--verbose', is_flag=True, help="Verbose")
def fetch_hls_stream(url, freq, output, verbose):
    setuplog(verbose)

    dynamicplaylist = m3u8.load(url)
    for playlist in dynamicplaylist:
        playlistdata = m3u8.load(playlist.absolute_uri)


if __name__ == '__main__':
    fetch_hls_stream()
