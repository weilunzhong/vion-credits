from end_credit_detector import EndCreditDetector, VionCreditError
from frame_hist_calculator import FrameHistCalculator
from vionrabbit import VionWorker
import json
import sys

class CreditValidationWorker(VionWorker):

    def process_json_dict(self, json_dict):
        video_path = json_dict['path']
        FHC = FrameHistCalculator()
        ECD = EndCreditDetector()
        try:
            print '-'*10
            print video_path
            # wind back time should be in negative seconds
            frame_hist, time_stamps = FHC.frame_reader(video_path, 1, -300)
            dominant_array = ECD.frame_hist_dominance(frame_hist)
            sliding_window, time_stamps = ECD.array_sliding_window(dominant_array, time_stamps, 10)
            print sliding_window
            ECD.interpolation(sliding_window, time_stamps, 0.7)
        except VionCreditError:
            print "error when max of ratio is not greater than 0.75"
        except ValueError:
            print "error when start is greater than end of movie"
        except TypeError:
            print "file might be polluted"





def main():
    CreditValidationWorker("weilun_movies_with_no_credit").work_it()


if __name__ == '__main__':
    main()
