import numpy as np
from scipy.spatial import distance
from vionaux.rnd import audioids

class StartCreditDetector(object):

    def _window_similarity(self, mfcc_1, mfcc_2, window_size):
        similarity_score = [distance.euclidean(mfcc_1[i][1:], mfcc_2[i][1:]) for i in range(0, window_size)]
        return similarity_score

    def position_loop(self, base_mfcc, income_mfcc):
        assert (base_mfcc.shape == income_mfcc.shape), "both mfccs must have the same dimension"
        current_score = 1e6
        sample_dist = 20
        window_size = 20
        for idx1 in range(0,(len(base_mfcc)/sample_dist)):
            mfcc_1 = base_mfcc[idx1*sample_dist:idx1*sample_dist+window_size]
            sim_score_list = []
            for idx2 in range(0, len(base_mfcc)-2*window_size):
                mfcc_2 = income_mfcc[idx2:idx2+window_size]
                sim_score = sum(self._window_similarity(mfcc_1, mfcc_2, window_size))
                sim_score_list.append(sim_score)

            if min(sim_score_list) < current_score and min(sim_score_list) > 10:
                current_score = min(sim_score_list)
                matched_base_idx = idx1*sample_dist
                matched_income_idx = np.argmin(sim_score_list)
        print current_score, matched_base_idx, matched_income_idx
        self.shift_diff = matched_base_idx - matched_income_idx
        print self.shift_diff

    def lenth_extraction(self,base_mfcc, income_mfcc, base_timestamp, income_timestamp):
        if self.shift_diff > 0:
            truncated_base_mfcc = base_mfcc[self.shift_diff:]
            truncated_base_timestamp = base_timestamp[self.shift_diff:]
            truncated_income_mfcc = income_mfcc[0:len(truncated_base_mfcc)]
            truncated_income_timestamp = income_timestamp[0:len(truncated_base_mfcc)]
        else:
            truncated_income_mfcc = income_mfcc[abs(self.shift_diff):]
            truncated_income_timestamp = income_timestamp[abs(self.shift_diff):]
            truncated_base_mfcc = base_mfcc[0:len(truncated_income_mfcc)]
            truncated_base_timestamp = base_timestamp[0:len(truncated_income_mfcc)]

        sim_score_list = self._window_similarity(truncated_base_mfcc, truncated_income_mfcc, len(truncated_base_mfcc))
        print [int(i) for i in sim_score_list]
        start_credit_index = [i for i , value in enumerate(sim_score_list) if value < 30]
#        print "s3e1: ", truncated_base_timestamp[start_credit_index]
#        print "s3e2: ", truncated_income_timestamp[start_credit_index]
        print "diff in the two: ", self.shift_diff
        base_mfcc_credit_start = truncated_base_timestamp[start_credit_index[0]]
        income_mfcc_credit_start = truncated_income_timestamp[start_credit_index[0]]
        print "credit start for base {0}, and for income {1}.".format(base_mfcc_credit_start, income_mfcc_credit_start)


if __name__ == "__main__":
    path_1 = "/media/weilun/tv_series/audio_file/house_of_cards_1.wav"
    path_2 = "/media/weilun/tv_series/audio_file/house_of_cards_4.wav"
    VAH = audioids.VionAudioHandler()
    SCD = StartCreditDetector()
    base_mfcc, time_stamp1 = VAH.get_mfccs(path_1, 0, 300, 14000, 2048, 1400)
    income_mfcc, time_stamp2 = VAH.get_mfccs(path_2, 0, 300, 14000, 2048, 1400)
    print "here is the mfcc length: {0}".format(len(base_mfcc))
    SCD.position_loop(base_mfcc, income_mfcc)
    SCD.lenth_extraction(base_mfcc, income_mfcc, time_stamp1, time_stamp2)
