"""
File: jpg_obj.py
Author: Melissa "Misha" Belisle (mxb4099)
Purpose: Small Class to keep track of data for processed "jpgs"
"""

class JPG:

	def __init__(self, md5, sha1, filename, contents, size):
		self.md5 = md5
		self.sha1 = sha1
		self.processed_md5 = ""	# to prove nothing has been modified
		self.processed_sha1 = ""
		self.filename = filename
		self.contents = contents
		self.size = size
		self.exif_tags = {}
		self.gps_tags = {}


	def print_exif(self):

		print("------------------------------")
		print ("Exif Time And Date Tag Data:")

		for key, value in self.exif_tags.items():

			if key == "GPSInfo" and len(self.gps_tags) > 0:
				self.print_gps()

			else:
				print("%18s: %s" % (key, value))
	
	def print_gps(self):

		print ("\nExif GPS Tag Data:")
		
		for key, value in self.gps_tags.items():
			print("%18s: %s" % (key, value))

	