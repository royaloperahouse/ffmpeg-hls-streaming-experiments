# Streaming HLS to S3 with FFmpeg

Experiments with FFmpeg and S3 for faking our Ateme Titan +
[AWS MediaPackage](https://aws.amazon.com/mediapackage/)

## Dependencies

[FFmpeg](https://ffmpeg.org) and [AWS CLI](https://aws.amazon.com/cli/)

## Notes

Show available video and audio devices:

`ffmpeg -f avfoundation -list_devices true -i ""` (note `avfoundation` is for
Mac OS - see
[alternatives for Linux and Windows](https://trac.ffmpeg.org/wiki/Capture/Webcam))

Example output:

```sh
[AVFoundation indev @ 0x154605d80] AVFoundation video devices:
[AVFoundation indev @ 0x154605d80] [0] HD Pro Webcam C920
[AVFoundation indev @ 0x154605d80] [1] FaceTime HD Camera
[AVFoundation indev @ 0x154605d80] [2] OBS Virtual Camera
[AVFoundation indev @ 0x154605d80] [3] Capture screen 0
[AVFoundation indev @ 0x154605d80] AVFoundation audio devices:
[AVFoundation indev @ 0x154605d80] [0] CalDigit Thunderbolt 3 Audio
[AVFoundation indev @ 0x154605d80] [1] HD Pro Webcam C920
[AVFoundation indev @ 0x154605d80] [2] MacBook Pro Microphone
[AVFoundation indev @ 0x154605d80] [3] RODE NT-USB
[AVFoundation indev @ 0x154605d80] [4] Microsoft Teams Audio
```

Capture the first video input (HD Pro Webcam C920) and the Rode mic, with set
video size, to a file:

`ffmpeg -f avfoundation -framerate 30 -video_size 640x480 -i "0:3" out.avi`

Output as HLS:

```sh
ffmpeg -f avfoundation -framerate 30 -video_size 640x360 -i "0:3" -c:v libx264 -crf 21 -preset veryfast \
    -c:a aac -b:a 128k -ac 2 \
    -f hls -hls_time 4 -hls_playlist_type event stream.m3u8
```

or output top left bit of screen as HLS:

```sh
ffmpeg -f avfoundation -r 30 -i "3:3" -vf "crop=640:360:0:0" -pix_fmt yuv420p \
    -f hls -hls_time 4 -hls_playlist_type event stream.m3u8
```

or use FFmpeg's test source (with `-re` to generate in real time):

```
ffmpeg -f lavfi -re -i testsrc -pix_fmt yuv420p \
    -f hls -hls_time 4 -hls_playlist_type event stream.m3u8
```

Make a target bucket:

`aws s3 mb s3://ffmpeg-stream-demo`

Sync with S3 every 5 seconds (segments are 8 seconds long):

`while true; do aws s3 sync ./ s3://ffmpeg-stream-demo --acl public-read; sleep 5; done`

Generate a JPG every 6 seconds:

`ffmpeg -i https://ffmpeg-stream-demo.s3-eu-west-1.amazonaws.com/stream.m3u8 -vf fps=1/6 img%03d.jpg`

## To do

1. ~~Stream a window with a clock in it instead of my webcam~~
2. Work out how to generate sprites
3. Use `watch` or similar to only sync files when they change
4. Create bitrate ladder
5. Look into subtitles

## Reference

1. https://www.martin-riedl.de/2018/08/24/using-ffmpeg-as-a-hls-streaming-server-part-1/
2. https://gist.github.com/docPhil99/d8667de1e8c5e96e2203f2bc0f28f89d
3. https://ottverse.com/hls-packaging-using-ffmpeg-live-vod/
4. https://ffmpeg.org/ffmpeg-all.html#hls-2
5. https://stackoverflow.com/questions/31223926/ffmpeg-command-to-create-thumbnail-sprites
