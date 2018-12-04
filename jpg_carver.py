#!/usr/bin/env python

import re
import sys
import os

JPEG_SOF=b'\xFF\xD8\xFF\xE0'
JPEG_EOF=b'\xFF\xD9'
DIR = "carved_jpgs/"

def carve_jpgs(image):
    images_found = 0
    image_file = open(image, 'rb')
    data = image_file.read()
    image_file.close()

    sof_list = [match.start() for match in re.finditer(re.escape(JPEG_SOF), data)]
    eof_list = [match.start() for match in re.finditer(re.escape(JPEG_EOF), data)]

    i = 0
    for sof in sof_list:
        subdata=data[sof:eof_list[i] + 2]
        carve_filepath= DIR + str(sof) + "_" + str(eof_list[i]) + ".jpg"
        ensure_dir()

        carve_jpg = open(carve_filepath, 'wb')
        carve_jpg.write(subdata)
        carve_jpg.close()
        i += 1
        print("Found image and carving it to " + carve_filepath)
        images_found += 1
    
    return images_found

def ensure_dir():
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def usage():
	print("\nusage: ./jpg_carver.py <dd file>\n")
	sys.exit(0)

if __name__ == '__main__':
	if(len(sys.argv) != 2):
		usage()
	image = sys.argv[1]
	images_found = carve_jpgs(image)
	print("Found {} JPEG images".format(images_found))
