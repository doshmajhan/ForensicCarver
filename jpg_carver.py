#!/usr/bin/env python

import re
import sys
import os
import time
import hashlib

# define jpg file format segments
#JPEG_SOF=b'\xFF\xD8\xFF\xE0'
JPEG_SOF=b'\xFF\xD8'
JPEG_EOF=b'\xFF\xD9'

# output directory for jpgs
DIR = "carved_jpgs/"

def carve_jpgs(image):
	# print program start
	image_size = os.path.getsize(image)
	print("\n------------------------------------------")
	print("Parsing {} ({} bytes) for JPGs\n".format(image, image_size))

	# load disk image data
	images_found = 0
	image_file = open(image, 'rb')
	data = image_file.read()
	image_file.close()

	# use regex to find the SOF and EOF of jpgs
	sof_list = [match.start() for match in re.finditer(re.escape(JPEG_SOF), data)]
	eof_list = [match.start() for match in re.finditer(re.escape(JPEG_EOF), data)]

	# get subdata for each jpg and create a file
	i = 0
	for sof, eof in zip(sof_list, eof_list):
		subdata=data[sof:eof + 2]
		carve_filepath= "{}{}_{}.jpg".format(DIR, str(sof), str(eof))
		print("\t-> JPG found, carving to " + carve_filepath)
		carve_jpg = open(carve_filepath, 'wb')
		carve_jpg.write(subdata)
		carve_jpg.close()

		images_found += 1
		i += 1

	return images_found

def ensure_dir():
	# check if directory exists, if not, create it
	if not os.path.exists(DIR):
		os.makedirs(DIR)

def usage():
	# print program usage
	print("\nusage: ./jpg_carver.py <dd file>\n")
	sys.exit(0)

if __name__ == '__main__':
	# check arguments for disk image file
	if(len(sys.argv) != 2):
		usage()
	image = sys.argv[1]

	ensure_dir()
	# parse disk image for jpgs
	s = time.clock()
	images_found = carve_jpgs(image)
	print("\nFound {} JPEG images in {:.4f} seconds".format(images_found, time.clock() - s))
	print("Parsing complete.\n------------------------------------------\n")
