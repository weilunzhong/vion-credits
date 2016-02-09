import numpy as np
from scipy.spatial import distance
from vionaux.rnd import audioids

class StartCreditDetector(object):

    def _window_similarity(self, mfcc_1, mfcc_2, window_size):
        assert mfcc_1.shape == mfcc_2,shape
        similarity_score = [distance.euclidean(mfcc_1[i][1:], mfcc_2[i][1:] for i in range(0, window_size))]
        return sum(similarity_score)

    def position_loop(self, base_mfcc, income_mfcc):
        current_score = 1e6
        for idx1 in range(0,(len(base_mfcc)/sample_dist)):
            mfcc_1 = base_mfcc[idx1*sample_dist:idx1*sample_dist+window_size]
            sim_score_list = []
            for idx2 in range(0, len(base_mfcc)-2*window_size):
                mfcc_2 = income_mfcc[idx2*sample_dist:idx2*sample_dist+window_size]
                sim_score = self._window_similarity(mfcc_1, mfcc_2, window_size)
                sim_score_list.append(sim_score)

            if min(sim_score_list) < current_score and min(sim_score_list) > 10:
                current_score = min(sim_score_list)
                matched_base_idx = np.argmin(sim_score_list)
                

