#!/usr/bin/env python3

import click
import logging
import m3u8
import os
import time
from concurrent.futures import ThreadPoolExecutor
from requests import get


# Set representing chunks that we have already downloaded
dlset = set()

# Download Pool
dlpool = ThreadPoolExecutor(max_workers=4)

# Logger
logger = logging.getLogger("fetch_hls_stream")


def setuplog(verbose):
    """Config the log output of fetch_hls_stream"""
    log_msg_format = '%(asctime)s :: %(levelname)5s ::  %(name)10s :: %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=log_msg_format, datefmt=log_date_format)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def download_file(uri, outputdir, filename):
    """Download a ts file and save on the outputdir as outputdir/filename"""
    try:
        fpath = os.path.join(outputdir, filename)
        with open(fpath, "wb") as file:
            logger.info("DOWNLOADING FILE: " + uri)
            response = get(uri)
            file.write(response.content)
            logger.debug("FINISHED DOWNLOADING FILE: " + uri)
    except Exception as ex:
        logger.error(ex)


@click.command()
@click.option('--url', help='URL to HLS m3u8 playlist.')
@click.option('--freq', default=5, help="Frequency for downloading the HLS m3u8 stream")
@click.option('--output', default="./", type=click.Path(exists=True), help="Output directory for video files")
@click.option('--verbose', is_flag=True, help="Verbose")
def fetch_hls_stream(url, freq, output, verbose):
    """Fetch a HLS stream by periodically retrieving the m3u8 url for new
    playlist video files every freq seconds. For each segment that exists,
    it downloads them to the output directory as a TS video file."""

    setuplog(verbose)

    while True:
        # Retrieve the main m3u8 dynamic playlist file
        dynamicplaylist = m3u8.load(url)

        # Retrieve the real m3u8 playlist file from the dynamic one
        for playlist in dynamicplaylist.playlists:
            # Check if we have each segment in the playlist file
            playlistdata = m3u8.load(playlist.absolute_uri)

            for videosegment in playlistdata.segments:
                # Since the playlist changes names dynamically we use the
                # last part of the uri (vfname) to identify segments
                videouri = videosegment.absolute_uri
                videofname = videouri.split("_")[-1]

                if videofname not in dlset:
                    dlset.add(videofname)
                    dlpool.submit(download_file, videouri, output, videofname)

        # Sleep until next check
        time.sleep(freq)


if __name__ == '__main__':
    fetch_hls_stream()
