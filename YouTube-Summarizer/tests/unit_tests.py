import unittest
from pydub import AudioSegment
from pyannote.core import Segment
import os
from backend.app.diarization import calculate_iou
import sys
sys.path.append("..")


class TestIOU(unittest.TestCase):
    
    def test_calculate_iou(self):
        segment1 = Segment(0,5)
        segment2 = Segment(2,7)
        
        expected_intersection = 3
        expected_total = 7
        expected_iou = float(expected_intersection/expected_total)
        
        output = calculate_iou(segment1, segment2)
        
        self.assertAlmostEqual(output, expected_iou)


class TestSpeakerSentences(unittest.TestCase):
    ...


if __name__ == '__main__':
    unittest.main()
        
        
        