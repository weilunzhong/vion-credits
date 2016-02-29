import numpy as np
import pysrt
from vionaux.rnd import vidioids
import re
from end_credit_detector import EndCreditDetector
#from vionrnd.models import FrameHistogram

class FrameHistCalculator(object):

    def __init__(self):
        self.VVH = vidioids.VionVideoHandler()

    def calculate_histogram(self, frame):
        r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]
        # translate to grey scale without opencv
        frame = 0.2989*r + 0.5870*g + 0.1140*b
        hist, bins = np.histogram(frame.ravel(),256, [0,256])
        return hist

    def frame_reader(self, path, sampling_rate=1, wind_back_time=-300):
        frame_generator = self.VVH.get_frames(path, sampling_rate, wind_back_time)
        frame_hist = []
        time_stamps = []
        for frame, time_stamp in frame_generator:
            frame_hist.append(self.calculate_histogram(frame))
            time_stamps.append(time_stamp)
        frame_hist = np.asarray(frame_hist)
        time_stamps = np.asarray(time_stamps)
        return frame_hist, time_stamps
#        return FrameHistogram(data=frame_hists , time_stamps=time_stamps)


if __name__ == "__main__":
    FHC = FrameHistCalculator()
    ECD = EndCreditDetector()
    video_path = "/mnt/movies03/boxer_movies/tt1906329/As Cool as I Am (2013)/As.Cool.as.I.Am.2013.720p.BluRay.x264.YIFY.mp4"
    # wind back time should be in negative seconds
    frame_hist, time_stamps = FHC.frame_reader(video_path, 1, -400)
    print "length of frame histogram is {0}.".format(len(frame_hist))
    dominant_array = ECD.frame_hist_dominance(frame_hist)
    sliding_window, time_stamps = ECD.array_sliding_window(dominant_array, time_stamps, 10)
    print sliding_window
    ECD.interpolation(sliding_window, time_stamps, 0.7)
