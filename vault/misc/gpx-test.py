## https://pypi.org/project/gpx-parser/
import gpx_parser as parser
import sys


with open(sys.argv[1], 'r') as gpx_file:
    gpx = parser.parse(gpx_file)
print("{} tracks loaded".format(len(gpx)))

for track in gpx:
    print('Track with {} segments and {} points')
    format(str(len(track)), str(track.get_points_no()))
    for segment in track:
        print('Segment with %s points % len(segment)')
        for point in segment:
            print(point)
