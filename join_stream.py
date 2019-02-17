#!/usr/bin/env python3

import logging
import os
import tempfile

import click
from ffmpy import FFmpeg

# Logger
logger = logging.getLogger("join_stream")


def setuplog(verbose):
    """Config the log output of join_stream"""
    log_msg_format = '%(asctime)s :: %(levelname)5s ::  %(name)10s :: %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=log_msg_format, datefmt=log_date_format)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


@click.command()
@click.option('--input', default="./", type=click.Path(exists=True),
              help="Input directory containing downloaded videos")
@click.option('--output', default='outmerge.mp4', help='Output Video File')
@click.option('--verbose', is_flag=True, help="Verbose")
def join_stream(input, output, verbose):
    """Join a list of downloaded TS video files from a given directory (output)
    into an Output Video File (output)."""

    setuplog(verbose)

    # Create temp file to store all videos
    tfd, tpath = tempfile.mkstemp(suffix=".ts")
    logger.debug("Created temp file at: " + tpath)

    with open(tpath, "wb") as tfile:
        # Reading video files in input directory
        dirfilenames = sorted(os.listdir(input))
        logger.info("Reading input files...")

        for videofname in dirfilenames:
            if videofname.endswith(".ts"):
                logger.debug("Reading file: " + videofname)
                with open(os.path.join(input, videofname), "rb") as videofile:
                    for line in videofile:
                        tfile.write(line)

                logger.debug("Finished reading file: " + videofname)

        logger.info("Finished reading all video TS files")
        tfile.flush()
        os.fsync(tfile.fileno())

        ff = FFmpeg(
            global_options=[
                '-y',
                '-loglevel error'
            ],
            inputs={tpath: None},
            outputs={output: '-acodec copy -vcodec copy'}
        )

        logger.info("Running FFMPEG tool to convert the file")
        logger.debug("FFMPEG CLI: " + ff.cmd)

        ff.run()

        logger.debug("Finished FFMPEG conversion")
        logger.info("Output video file: " + output)


if __name__ == '__main__':
    join_stream()
