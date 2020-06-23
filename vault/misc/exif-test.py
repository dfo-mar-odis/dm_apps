#!/usr/bin/env python
#
# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
from PIL import Image

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

exif = get_exif('image.jpg')
#print(exif)


from PIL.ExifTags import TAGS

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

exif = get_exif('image.jpg')
labeled = get_labeled_exif(exif)
#print(labeled)



from PIL.ExifTags import GPSTAGS

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

exif = get_exif('image.jpg')
geotags = get_geotagging(exif)
print(geotags)
