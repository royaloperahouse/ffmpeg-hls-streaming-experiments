rm -rf *.ts;
rm -rf *.m3u8
ffmpeg -f avfoundation -framerate 30 -video_size 640x360 -i "0:3" -c:v libx264 -crf 21 -preset veryfast \
    -c:a aac -b:a 128k -ac 2 \
    -f hls -hls_time 4 -hls_playlist_type event stream.m3u8

