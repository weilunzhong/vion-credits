#from vionrnd.models import FrameHistogram
import numpy as np

class VionCreditError(Exception):
    pass


class EndCreditDetector(object):

    def single_frame_hist_dominance(self, frame_hist):
        dominating_pixel = sum(np.sort(frame_hist)[-5:])
        return float(dominating_pixel) / sum(frame_hist)

    def frame_hist_dominance(self, frame_hists):
        dominating_ratio = [self.single_frame_hist_dominance(i) for i in frame_hists]
        return np.asarray(dominating_ratio)

    def array_sliding_window(self, frame_hists, time_stamps, window_size=5):
        array_length = np.size(frame_hists)
        smoothed_array = np.zeros((array_length-window_size), dtype = np.float)
        for idx in range(0, array_length - window_size):
            smoothed_array[idx] = float(np.sum(frame_hists[idx:idx+window_size]))/window_size
        return smoothed_array, time_stamps[0:array_length-window_size]

    """ dynamic thresholding that doesnt work well for now
    def interpolation(self, smoothed_array, time_stamps, threshold):
        max_ratio, min_ratio  =  np.max(smoothed_array), np.min(smoothed_array)
        print max_ratio, min_ratio
        interpolation_value = min_ratio + threshold * (max_ratio - min_ratio)
        print interpolation_value
        estimation_func = np.poly1d(np.polyfit(range(0, len(smoothed_array)), smoothed_array, 7))
        self.estimation_func =estimation_func
        print estimation_func(range(0,len(smoothed_array)))
        idx_array = np.where(estimation_func(range(0,len(smoothed_array))) > interpolation_value)
        print "index {0} and the timestamp {1}.".format(idx_array[0][0], time_stamps[idx_array[0][0]])
        return time_stamps[idx_array[0]]
        """

    def interpolation(self, smoothed_array, time_stamps, threshold):
        max_ratio, min_ratio  =  np.max(smoothed_array), np.min(smoothed_array)
        if max_ratio - min_ratio < 0.5:
            raise VionCreditError("The hist ratio max {0} and min {1} is too close, check for wind back time.".format(max_ratio, min_ratio) )
        if max_ratio < 0.75:
            raise VionCreditError("The hist ratio max {0} is not large enough to be a credit, check again.".format(max_ratio))
        interpolation_value = min_ratio + threshold * (max_ratio - min_ratio)
        filtered_array = [(1 if ele > interpolation_value else 0) for ele in smoothed_array]
        print filtered_array
        pre_value = 0
        start_index, end_index = [], []
        for idx, ratio in enumerate(filtered_array):
            if ratio > pre_value:
                start_index.append(idx)
            if ratio < pre_value:
                end_index.append(idx)
            pre_value = ratio
        print time_stamps[start_index]
        print time_stamps[end_index]
