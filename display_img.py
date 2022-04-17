'''
Display Image so that we can determine points we want to select for transform
'''
from homography_estimation import Transform, Point
import argparse

# argument parser
parser = argparse.ArgumentParser(description='Homography Transform')
parser.add_argument("-i","--img", help="<Required> path to image to be transformed", type=str, default='/test_data/tv.jpg', required=True)

args = parser.parse_args()

t = Transform()

t.load_image(args.img)

t.display_image()
