#!/usr/bin/env python

import re
import sys
import os
import time

JPEG_SOF=b'\xFF\xD8\xFF\xE0'
JPEG_EOF=b'\xFF\xD9'
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
	ensure_dir()
	for sof in sof_list:
		subdata=data[sof:eof_list[i] + 2]
		carve_filepath= DIR + str(sof) + "_" + str(eof_list[i]) + ".jpg"
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

	# parse disk image for jpgs
	s = time.clock()
	images_found = carve_jpgs(image)
	print("\nFound {} JPEG images in {:.4f} seconds".format(images_found, time.clock() - s))
	print("Parsing complete.\n------------------------------------------\n")
