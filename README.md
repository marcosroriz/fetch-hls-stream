# fetch-hls-stream

A simple Python CLI tool that can continuosly fetch and save video segments from a HLS stream (M3U8 URL).

It also includes another CLI tool to join the resulting videos into a single one.

## Basic setup

Clone the repository and install the requirements:
```
$ pip install -r requirements.txt
```

__Note__: *the additional join tool requires the installation of [FFmpeg](https://www.ffmpeg.org/).*

Ubuntu users can install FFmpeg as follow:
```
$ sudo apt-get install ffmpeg
```

## Fetch HLS stream from M3U8 URL

The CLI tool is run as following:
```
$ python -m fetch_hls_stream --url M3U8URL
```

You can pass the following parameters:
- ```--url TEXT      URL to HLS m3u8 playlist.```
- ```--freq INTEGER  Frequency for downloading the HLS m3u8 stream```
- ```--output PATH   Output directory for video files```
- ```--verbose       Verbose```
- ``` --help          Show this message and exit.```

For instance, the line below configure the tool to:
1. Every 10 seconds retrieve the `https://example.org/playlist.m3u8` URI
2. Retrieve the playlist inside this URI (_e.g._, `https://example.org/chunk127.m3u8`)
3. Check if there are new TS video files in this playlist.
4. If positive, download them to `outdir`

```
$ python -m fetch_hls_stream --url https://example.org/playlist.m3u8 --output outdir --freq 10
```

## Join downloaded videos
To join the downloaded video run the `join_stream` tool as following:
```
$ python -m join_stream --input dirwithvideos --output finalvideo.mp4
```

You can pass the following parameters:
- ```--input PATH      Input directory containing downloaded videos.```
- ```--output TEXT   Output Video File```
- ```--verbose       Verbose```
- ``` --help          Show this message and exit.```

For instance, the line below configure the tool to:
1. Read all video files from outdir (in string order)
2. Save them into a single vidoe file called out.mp4

```
$ python -m join_stream --input outdir --output out.mp4
```

## Tests

To run the tests execute the following command:
```
$ pytest
```
