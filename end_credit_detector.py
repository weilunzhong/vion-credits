from vionrnd.models import FrameHistogram




class EndCreditDetector(object):

    def single_frame_hist_dominance(self, frame_hist):
        dominating_pixel = sum(np.sort(frame_hist)[-5:])
        return float(dominating_pixel) / sum(frame_hist)
        
    def frame_hist_dominance(self, frame_hists):
        dominating_ratio = [self.single_frame_hist_dominance(i) for i in frame_hists]
        return np.asarray(dominating_ratio)

    def array_sliding_window(self, result_array, window_size, filter_ratio):
        array_length = np.size(result_array)
        buffer_array = np.zeros((array_length-window_size), dtype = np.int)
        flag_array = np.zeros((array_length-window_size), dtype = np.int)
        for idx in range(0, array_length - window_size):
            window_score = np.sum(result_array[idx:idx+window_size])
            buffer_array[idx] = (1 if window_score>(window_size*filter_ratio) else 0)
            if buffer_array[idx] < buffer_array[idx]
        buffer_array = np.delete(buffer_array, 0)
        flag_array = np.zeros(np.size(buffer_array), dtype=np.int)
        return flag_array  
            
def getWords(text):
    return re.compile("\w+").findall(text)
