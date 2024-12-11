import os
from videoDownloader import download_video

test_url = "<TEST URL HERE>" 
test_dir = os.path.join(os.path.dirname(os.getcwd()), "..\\..\\Files\\test.mp4")

download_video(test_url, test_dir)