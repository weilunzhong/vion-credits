from end_credit_detector import EndCreditDetector, VionCreditError
from frame_hist_calculator import FrameHistCalculator
import json
import sys

def main():
    validation_file_path = "../vionlabs_weilun/rabbitMQ/credit_no.json"
    FHC = FrameHistCalculator()
    ECD = EndCreditDetector()
    sys.stdout = open("output.txt", "w")

    with open(validation_file_path, "r") as f:
        for line in f:
            video_path = json.loads(line)['path']
            try:
                print '-'*10
                print video_path
                video_path = json.loads(line)['path']
                # wind back time should be in negative seconds
                frame_hist, time_stamps = FHC.frame_reader(video_path, 1, -300)
                dominant_array = ECD.frame_hist_dominance(frame_hist)
                sliding_window, time_stamps = ECD.array_sliding_window(dominant_array, time_stamps, 10)
                print sliding_window
                ECD.interpolation(sliding_window, time_stamps, 0.7)
            except VionCreditError:
                print "error when max of ratio is not greater than 0.75"
                continue

if __name__ == '__main__':
    main()
