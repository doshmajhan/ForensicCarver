"""
File: jpg_timeline.py
Author: Melissa "Misha" Belisle (mxb4099)

[Input] Directory of JPEG files
[Output] Option(s): Timeline, Report 

Purpose:
Process all files in the provided directory;
meant to be run on JPGs or files suspected to be JPGs

For all file(s), generates:

- a single Timeline, based on the "DateTimeOriginal" Exif Tag, if it exists
- a general report, with more detail(s) on the files processed
- suggests the files that are not JPGs and would be good candidates to run
with other tools in the project

- ** Does NOT check to see if any of JPG files are duplicates, based on hashes

python3 jpg_timeline.py [jpg_dir_filepath]
"""

import os, hashlib, collections, sys

#from matplotlib import pyplot
from datetime import datetime
from exif_fields import exif_segments, exif_tags, gps_tags, relative_gps_tags
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS
from jpg_obj import JPG

banner 		= "============================================"
half_banner = "--------------------------------------------"
divider 	= "############################################"

jpg_files = []
not_jpgs = []

"""
Simple checker that looks for the SOI and EOI that indicate
a file is a JGP.

Checks first two bytes for SOI, checks last two bytes for EOI.
Locations based on JPG Exif Documentation.
"""
# is likely more useful if running separately from the jpg scraper
def is_jpg(jpg, size):

	soi = False
	eoi = False

	if exif_segments['SOI'] in jpg[0:2]:
		soi = True

	if exif_segments['EOI'] in jpg[size-2:size]:
		eoi = True

	return soi, eoi

"""
Basic function to open and read a file in binary.

Returns the completely read-in file as binary,
its size, and whether or not it has the expected
SOI and EOI.
"""
def read_file(jpg):

	with open(jpg, 'rb') as bin:
		contents = bin.read()
		size = len(contents)

		soi, eoi = is_jpg(contents, size)

	return contents, size, soi, eoi

"""
Experimental function for parsing the APP1 segment
found in JPG's Exif header.

Takes a jpg and its suspected APP1 offset.

https://www.codeproject.com/Articles/47486/Understanding-and-Reading-Exif-Data
"""
def parse_app1(jpg, offset):
	
	app1 = binary[offset:offset+2] 			# APP1
	marker_len = binary[offset+2:offset+4]	# supposedly Len of marker section data...
	identifier = binary[offset+4:offset+10]	# identifier: Exif\000\000
	end = binary[offset+10:offset+12]		# Endian-ness (II, little end, or MM, big end)
	sig = binary[offset+12:offset+14]		# Supposedly a fixed value (42)
	zeroth = binary[offset+14:offset+18]	# offset of 0th id; typically 8

    # Tags begin at 1st IFD; interoperability arrays
    # https://metacpan.org/pod/distribution/Image-MetaData-JPEG/lib/Image/MetaData/JPEG/TagLists.pod#Valid-tags-for-Exif-APP1-data
    # e.g. DateTime, GPSInfo

"""
Really basic processor that tries to extract the offsets of 
Exif segments from the binary.
"""
def process_exif(jpg):

	offsets = {}
	
	for seg in exif_segments:

		# find locates first instance of the sequence
		offset = binary.find(headers[seg])

		if offset > -1:
			offsets[seg] = str(offset)

			#if seg == "APP1":
			#	parse_app1(jpg, offset)

		else:
			offsets[seg] = ""

	return offsets

"""
Function using the PIL library to extract Exif tag metadata.
"""
def process_PIL(jpg):

	img = Image.open(jpg)
	data = img._getexif()
	metadata = {}

	if not data:
		print ("Could not obtain Exif data for file")

	else:
		for tag, value in data.items():
			tag_name = TAGS.get(tag, tag)
			metadata[tag_name] = value
			#print(tag_name)
			#print (val)
			#print("\n")

	return metadata
			
"""
Locate information on existing, desired Exif tag types.

Specifically looking for Location and DateTime fields,
which may be more valuable to a Forensics Investigator.
"""
def process_tags(tag_dict, jpg):
	
	exif = {}
	gps = {}

	tags = tag_dict.keys()

	for tag in exif_tags:
		if tag in tags:

			exif[tag] = tag_dict[tag]
			
			if tag == 'GPSInfo':

				gps_data = tag_dict[tag]
				for gps_tag, value in gps_data.items():

					if gps_tag in relative_gps_tags:
				
						gps[relative_gps_tags[gps_tag]] = value
		
		else:
			exif[tag] = ""

		jpg.exif_tags = exif
		jpg.gps_tags = gps

"""
Sort files according to DateTimeOriginal

https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

WARNING: On the off-chance two images have the exact same DateTime down to the Seconds field,
there is a chance one will overwrite the other in the "value" slot (due to updating the same key)

This is unlikely, but in the low % chance this does occur, implement a key check and
make the value(s) a list or something --> see timeline_stats() for an example of this
"""
def date_sort_original():

	datetimes = {}
	no_dt_org = []

	for jpg in jpg_files:

		dt_raw = jpg.exif_tags['DateTimeOriginal']

		if not dt_raw == "":
			dt_obj = datetime.strptime(dt_raw, '%Y:%m:%d %H:%M:%S')
			datetimes[dt_obj] = jpg.filename

		else:
			no_dt_org.append(jpg.filename)

	dt_sorted = collections.OrderedDict(sorted(datetimes.items()))

	#for dt, fi in dt_sorted.items():
	#	print(dt, fi)

	return dt_sorted, no_dt_org


"""
[TBD]

Create a basic graph using timeline data

X Axis: Date
Y Axis: Count

https://matplotlib.org/index.html
"""
def graphical_timeline(dt_sorted):
	
	# each unique date
	x = []

	# count of files on each unique date
	y = []

	# some logic to calculate an even distr based on date range
	x_axis = []

	# min 0 to VAL % more than the max_file_count on a given date
	# or something
	y_axis = [x for x in range(0,len(dt_sorted))]

	### logic for x, y vals
	# parse the DT for the Date (Year, Month) only 
	# for each dt key (x), y = count of associated files


"""
Convert DateTime: Filename pairs into a dict
with files sorted by Year 
"""
def timeline_stats(dt_sorted):

	years = {}

	for key, value in dt_sorted.items():

		year = key.year

		if year not in years.keys():
			years[year] = [value]

		else:
			years[year].append(value)

	#for unique in years:
	#	print(unique)

	#	for fi in years[unique]:
	#		print(fi)

	return years

"""
Function that generates a Timeline with:

Report Header
	Including statistics (breakdown by year)

A text-based timeline
A simple timeline graphic
[TBD] A GPS graphic 
"""
def generate_timeline(image_path, dt_sorted):
	
	generation_path = "Generating timeline for files in: " + image_path + "\n"
	dt_now = datetime.now()
	date = "{:%B %d, %Y at %H:%M:%S}".format(dt_now)
	generation_dt = "Timeline report generated on: " + date + "\n"

	report_name = "JPG_Timeline_" + str(dt_now) + ".txt"

	try:
		with open(report_name, 'a+') as report:
			
			report.write(divider +"\n")
			report.write(generation_path)
			report.write(generation_dt)
			report.write(half_banner +"\n\n")
			
			report.write("Basic DateTimeOriginal Statistics: \n")

			stats = timeline_stats(dt_sorted)
			total_years = len(stats) # 1 unique key/year
			total_files = len(dt_sorted)

			report.write("%d unique files over %d unique years:\n\n" % (total_files, total_years))

			for year in stats.keys():
				report.write("Files created in year %d:\n" % year)

				for fi in stats[year]:
					report.write(fi + "\n")

				report.write("\n")

			report.write(half_banner +"\n\n")

			report.write("DateTimeOriginal Timeline: \n\n")

			report.write("%18s %s\n\n" % ("DateTimeOriginal Stamp", " JGP File"))

			for date, fi in dt_sorted.items():
				report.write("%20s %s\n" % (str(date), "   " + fi))

			report.write("\n" + divider +"\n")

		# actual timeline
		# --> can I create a basic graph to output???
		# if gps data exists, can i get a map?

	except IOError as error:
		print("Failed to create timeline report with name: " + report_name)

	return report_name

"""
Function that generates a Report with:

Report Header
	Date Report has been generated on
	Time of generation
	Directory Name
	List of processed Files
	Time Range(s) of date(s) found (low -> high)
	Suggestion of any "Suspect Files"

Summary of each File Processed
"""
def generate_report(image_path, dt_sorted):

	generation_path = "Generating report for files in: " + image_path + "\n"
	dt_now = datetime.now()
	date = "{:%B %d, %Y at %H:%M:%S}".format(dt_now)
	generation_dt = "Report generated on: " + date + "\n"

	report_name = "JPG_Report_" + str(dt_now) + ".txt"

	summary_line = "Summary of Files Processed: \n"
	# loop through the list of files
	not_jpgs_msg = "The following files did not contain the expected JPG header marker and may be suspect: \n"
	# loop through any not jpegs
	no_suspects = "No files were suspect of not being JPGs. \n"

	date_summary = "According to the DateTimeOriginal tag, the range of JPG creation is: \n"

	keys = list(dt_sorted.keys())
	low_time = keys[0]
	low_fn = dt_sorted[low_time]
	lower_bound = "Earliest created: " + str(low_time) + " (" + low_fn + ") \n"

	upper_time = keys[len(dt_sorted)-1]
	up_fn = dt_sorted[upper_time]
	upper_bound = "Latest created: " + str(upper_time) + " (" + up_fn + ") \n"

	try:
		with open(report_name, 'a+') as report:
			
			report.write(divider +"\n")
			report.write(generation_path)
			report.write(generation_dt)
			report.write(half_banner +"\n")
			report.write(summary_line)

			total_processed = len(jpg_files)
			report.write("Total files processed: " + str(total_processed) + "\n")

			for jpg in jpg_files:
				report.write(jpg.filename + "\n")

			report.write("\n")	

			if len(not_jpgs) > 0:
				report.write(not_jpgs_msg)

				for not_jpg in not_jpgs:
					report.write(not_jpg + "\n")	

			else:
				report.write(no_suspects)

			report.write("\n")	
			report.write(half_banner +"\n")
			report.write(date_summary)
			report.write(lower_bound)
			report.write(upper_bound)
			report.write("\n")
			report.write(divider +"\n")

			report.write("Individual File Reports: \n\n")

			# loop through files and call file report

			for jpg in jpg_files:
				file_report(jpg, report, image_path)

	except IOError as error:
		print("Failed to create report with name: " + report_name)

	return report_name

"""
Creates a "File Report" from a given jpg_obj,
to be used with generate_report()

Filename (File Size, Bytes)
md5, sha1 hashes (from before/after)

Headers Found and at what Offsets
	Including SOI and EOI

DateTime Data
GPS Data

[TBD] File Dump
"""
def file_report(jpg, report, image_path):
	
	report.write("Generating File Report for: " + jpg.filename + "(" + str(jpg.size) + " bytes)\n")
	report.write(half_banner +"\n")

	report.write("Hashes before file processing: \n")
	report.write("md5:  " + jpg.md5 + "\n")
	report.write("sha1: " + jpg.sha1 + "\n\n")

	report.write("Hashes after file processing: \n")

	new_md5 = hashlib.md5(jpg.filename.encode()).hexdigest()
	new_sha1 = hashlib.sha1(jpg.filename.encode()).hexdigest()

	report.write("md5:  " + new_md5 + "\n")
	report.write("sha1: " + new_sha1 + "\n\n")

	report.write("Summary of DateTime and GPS Exif Metadata Recovered: \n\n")

	# Headers Found & at what Offset
	# 	if JPG Header/Footer exists: flag

	report.write("Exif DateTime Tags: \n")

	has_gps = False

	for dt_tag, dt_val in jpg.exif_tags.items():

		if dt_tag == "GPSInfo" and len(jpg.gps_tags) > 0:
			has_gps = True

		else:
			report.write("%18s: %s\n" % (dt_tag, dt_val))

	report.write("\n")

	if has_gps:

		report.write("Select Exif GPSInfo Tags: \n")

		for gps_tag, gps_val in jpg.gps_tags.items():
			report.write("%18s: %s\n" % (gps_tag, gps_val))
	else:
		report.write("No GPS Metadata Found. \n")

	# Header Dump? in hex or bytes 

	report.write("\n" + divider + "\n")

"""
Simple function for printing jpg obj's attributes
"""
def mass_print():

	for jpg in jpg_files:
		for field in vars(jpg).items():
			if not field[0] == "contents": 
				print(str(field[0]) + ": " + str(field[1]))

		print("\n")

def main():
	
	# get directory path from user input

	if not len(sys.argv) == 2:
		print("Usage: python3 jpg_timeline.py [path_to_jpg_directory]")

	else:
		#image_path = "/Users/Crystal/Desktop/Forensics/Project/Test Images"

		image_path = sys.argv[1]
		processed_files = 0

		if not (os.path.exists(image_path)):
			print("\nError, problem with given file path.")
			print("[%s] does not seem to exist.\n" % image_path)

		else:
			print(banner)
			print("Processing files in: " + image_path)
			date = "{:%B %d, %Y at %H:%M:%S}".format(datetime.now())
			print("Processing started on: " + date)
			print(banner)
			
			for fi in os.listdir(image_path):

				#fi = fi.strip()
				full_path = image_path + "/" + fi

				# ignore hidden files and sub-dirs
				if not fi.startswith('.') and not os.path.isdir(full_path):
					processed_files += 1
					
					print("Generating md5 and sha1 hashes for " + fi)

					md5 = hashlib.md5(fi.encode()).hexdigest()
					sha1 = hashlib.sha1(fi.encode()).hexdigest()

					print("md5 hash:  " + md5)
					print("sha1 hash: " + sha1)
					
					print("\nOpening " + fi + "...")

					contents, size, soi, eoi = read_file(full_path)

					if (not soi) or (not eoi):
						print("\n" + fi + " may not be a JPG file...")
						not_jpgs.append(fi)

						if not soi:
							print ("File is missing SOI header " + str(exif_segments['SOI']))
						if not eoi:
							print ("File is missing EOI header " + str(exif_segments['EOI']))

					else:

						print("Extracting file metadata....\n")

						new_jpg = JPG(md5, sha1, fi, contents, size)
						jpg_files.append(new_jpg)

						tag_dict  = process_PIL(full_path)
						process_tags(tag_dict, new_jpg)

						#new_jpg.print_exif()

					print(half_banner + "\n")

			#mass_print()
			jpg_sorted, no_time = date_sort_original()	# Ordered dict of Original Times: filename, List of JPG(s) w none

			timeline_name = generate_timeline(image_path, jpg_sorted)
			print("Generated JPG Timeline...." + timeline_name)

			report_name = generate_report(image_path, jpg_sorted)
			print("Generated JPG Report...." + report_name + "\n")

			print(banner)
			print("Total files processed: " + str(processed_files))
			print("Processing finished on: " + date)
			print("Hashes generated with: Python's 'hashlib' library.")
			print(banner)

main()

