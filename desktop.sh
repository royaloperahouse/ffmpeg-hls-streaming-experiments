# clear up old output files and start generating an HLS capture from the top left corner of the screen

rm -rf *.ts
rm -rf *.m3u8
ffmpeg -f avfoundation -r 30 -i "3:3" -vf  "crop=640:360:0:0" -pix_fmt yuv420p -f hls -hls_time 4 -hls_playlist_type event stream.m3u8
