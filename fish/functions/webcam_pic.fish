function webcam_pic
	ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 $argv[1]
end
