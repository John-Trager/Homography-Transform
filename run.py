'''
file used to run homography transform
@Author: John Trager, Daniel Stefanescu
'''
from homography_estimation import Transform, Point
import argparse
import json

# argument parser
parser = argparse.ArgumentParser(description='Homography Transform')
parser.add_argument("-i","--img", help="<Required> path to image to be transformed", type=str, default='/test_data/tv.jpg', required=True)
parser.add_argument('--points_in', help='<Required> 4 points 1st img plane, points should be clockwise ordered "[[x1,y1],[x2,y2],...]"', required=True, type=str)
parser.add_argument('--points_out', help='<Required> 4 points for 2nd img plane, points should be clockwise ordered "[[x1,y1],[x2,y2],...]"', required=True,type=str)
parser.add_argument("-c","--compression", help="<Optional> scale/compression number", type=int, default=4)

args = parser.parse_args()

t = Transform()

t.load_image(args.img)

SCALE = args.compression

# create transform point
# point order: top left, top right, bottom right, bottom left
points_in = json.loads(args.points_in)
points_out = json.loads(args.points_out)

t.add_points([Point(points_in[0][0],points_in[0][1]), Point(points_in[1][0],points_in[1][1]),
              Point(points_in[2][0],points_in[2][1]), Point(points_in[3][0],points_in[3][1])],

            [Point(points_out[0][0]*SCALE,points_out[0][1]*SCALE),
             Point(points_out[1][0]*SCALE,points_out[1][1]*SCALE),
             Point(points_out[2][0]*SCALE,points_out[2][1]*SCALE),
             Point(points_out[3][0]*SCALE,points_out[3][1]*SCALE)])

## example coordinates for images
#tv
# "[[280,120],[504,295],[450,534],[184,560]]"
# "[[0,0],[0,200],[200,200],[200,0]]"
#t.add_points([Point(280,120), Point(504,295), Point(450,534), Point(184,560)], [Point(0,0), Point(0,SCALE*200), Point(SCALE*200,SCALE*200), Point(SCALE*200,0)])

# life
#t.add_points([Point(95,352), Point(330,270), Point(435,554), Point(225,660)], [Point(0,0), Point(0,SCALE*200), Point(SCALE*200,SCALE*200), Point(SCALE*200,0)])

# qr_code3
#t.add_points([Point(4*62,4*65), Point(4*107,4*93), Point(4*80,4*120), Point(4*37,4*98)], [Point(0,0), Point(4*200,0), Point(4*200,4*200), Point(0,4*200)])

t.transform_image(2)
t.display_transform()

