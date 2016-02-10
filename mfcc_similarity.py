import numpy as np
from scipy.spatial import distance
from vionaux.rnd import audioids

class StartCreditDetector(object):

    def _window_similarity(self, mfcc_1, mfcc_2, window_size):
        assert (mfcc_1.shape == mfcc_2,shape), "both mfccs must have the same dimension"
        similarity_score = [distance.euclidean(mfcc_1[i][1:], mfcc_2[i][1:]) for i in range(0, window_size)]
        return similarity_score

    def position_loop(self, base_mfcc, income_mfcc):
        assert (base_mfcc.shape == income_mfcc.shape), "both mfccs must have the same dimension"
        current_score = 1e6
        for idx1 in range(0,(len(base_mfcc)/sample_dist)):
            mfcc_1 = base_mfcc[idx1*sample_dist:idx1*sample_dist+window_size]
            sim_score_list = []
            for idx2 in range(0, len(base_mfcc)-2*window_size):
                mfcc_2 = income_mfcc[idx2*sample_dist:idx2*sample_dist+window_size]
                sim_score = sum(self._window_similarity(mfcc_1, mfcc_2, window_size))
                sim_score_list.append(sim_score)

            if min(sim_score_list) < current_score and min(sim_score_list) > 10:
                current_score = min(sim_score_list)
                matched_base_idx = np.argmin(sim_score_list)
                

    def lenth_extraction(self):
        if shift_diff < 0:
            truncated_base_mfcc = base_mfcc[shift_diff:]
            truncated_income_mfcc = income_mfcc[0:len(truncated_base_mfcc)]
        else:
            truncated_income_mfcc = income_mfcc[abs(shift_diff):]
            truncated_base_mfcc = base_mfcc[0:len(truncated_income_mfcc)]

        sim_score_list = _window_similarity(truncated_base_mfcc, truncated_income_mfcc, len(truncated_base_mfcc))
        

if __name__ == "__main__":
    path_1 = "/media/weilun/tv_series/audio_file/house_of_cards_1.wav"
    path_2 = "/media/weilun/tv_series/audio_file/house_of_cards_2.wav"
    VAH = audioids.VionAudioHandler()
    base_mfcc, time_stamp1 = VAH.get_mfccs(path_1, 0, 60, 14000, 2048, 1400)
    income_mfcc, time_stamp2 = VAH.get_mfccs(path_2, 0, 60, 14000, 2048, 1400)
    print base_mfcc.shape
