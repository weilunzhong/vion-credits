import numpy as np
import pysrt
#from vionrnd.models import FrameHistogram
from vionaux.rnd import vidioids
import re

class FrameHistCalculator(object):

    def __init__(self):
        self.VVH = vidioids.VionVideoHandler()

    def calculate_histogram(self, frame):
        r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]
        frame = 0.2989*r + 0.5870*g + 0.1140*b
        hist, bins = np.histogram(frame.ravel(),256, [0,256])
        return hist

    def frame_reader(self, path, sampling_rate=1, wind_back_time=-300):
        frame_generator = self.VVH.get_frames(path, sampling_rate, wind_back_time)
        frame_hist = None
        time_stamps = []
        for (frame, time_stamp) in frame_generator:
            hist = self.calculate_histogram(frame)
            hist = np.expand_dims(hist,axis=0)
            if frame_hist == None:
                frame_hist = hist
            else:
                frame_hist = np.append(frame_hist, hist, axis=0)
            time_stamps.append(time_stamp)
        time_stamps = np.asarray(time_stamps)
#        print frame_hist.shape, len(time_stamps)
        return FrameHistogram(data=frame_hists , time_stamps=time_stamps)


if __name__ == "__main__":
    FHC = FrameHistCalculator()
    video_path = "/mnt/movies03/boxer_movies/tt3247714/Survivor (2015)/Survivor.2015.720p.BluRay.x264.YIFY.mp4"
    hist_generator = FHC.frame_reader(video_path, 0.1)
#    log_path = "/home/vionlabs/Documents/vionlabs_weilun/video_projects/credit_detection/credit_log/with_ratio_tt1401152.txt"
#    log_file = open(log_path, 'r')
#    hist_result_array = np.zeros(0)
#    for index, line in enumerate(log_file):
#        if index == 0:
#            start_frame_index = int(getWords(line)[0])
#
#        if(index%2)==1:
#            hist_ratio = float(line[0:9])
#            hist_result_array = np.append(hist_result_array,hist_ratio)
#    hist_result_array = np.delete(hist_result_array,0)
#    result = ECD.array_sliding_window(hist_result_array, 20, 0.55)
#
#    print "start is {0}, end is {1}".format(np.argwhere(result==1), np.argwhere(result==-1))
