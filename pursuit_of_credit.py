import numpy as np
from scipy.spatial import distance
from vionaux.rnd import audioids

class StartCreditHunter(object):
    """
    If the start credit is specified them this class finds the same content
    If the start is not known, try StartCreditDetector
    """

    @staticmethod
    def _window_similarity(mfcc_1, mfcc_2, window_size):
        similarity_score = [distance.euclidean(mfcc_1[i][1:], mfcc_2[i][1:]) for i in range(0, window_size)]
        return similarity_score

    def locate_credit_position(self, base_mfcc, income_mfcc, base_timestamp, income_timestamp):
        credit_length = len(base_timestamp)
        sim_score_list = []
        for idx in range(0, len(income_mfcc)-credit_length):
            sim_score = self._window_similarity(base_mfcc, income_mfcc[idx:idx+credit_length], credit_length)
            sim_score_list.append(sum(sim_score))
        sims = np.asarray(sim_score_list)
        start_index = np.argmin(sims)
        print sims, income_timestamp[start_index]
        print start_index

def main():
    path_1 = "/media/weilun/tv_series/audio_file/humans_1.wav"
    path_2 = "/media/weilun/tv_series/audio_file/humans_2.wav"
    VAH = audioids.VionAudioHandler()
    SCH = StartCreditHunter()
    base_mfcc, time_stamp1 = VAH.get_mfccs(path_1, 71, 115, 14000, 2048, 1400)
    income_mfcc, time_stamp2 = VAH.get_mfccs(path_2, 0, 300, 14000, 2048, 1400)
    print "here is the mfcc length: {0}".format(len(base_mfcc))
    SCH.locate_credit_position(base_mfcc, income_mfcc, time_stamp1, time_stamp2) 


if __name__ == "__main__":
    main()
