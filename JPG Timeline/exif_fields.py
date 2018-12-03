"""
File: exif_fields.py
Author: Melissa "Misha" Belisle (mxb4099)
Purpose: De-clutter the amount of data in the jpg_timeline file.
"""

#
# Exif Segments
#

# http://dev.exiv2.org/projects/exiv2/wiki/The_Metadata_in_JPEG_files
exif_segments = {
	
	'SOI'  :b'\xFF\xD8',	# Start of Image --> should be at offset 0
	'APP1' :b'\xFF\xE1',
	'DQT'  :b'\xFF\xDB',
	'DHT'  :b'\xFF\xC4',
	'SOF0' :b'\xFF\xC0',
	'SOF2' :b'\xFF\xC2',
	'SOS'  :b'\xFF\xDA',
	'DRI'  :b'\xFF\xDD',
	'RST0' :b'\xFF\xD0',
	'COM'  :b'\xFF\xFE',
	'EOI'  :b'\xFF\xD9'	# End of Image
}

#
# Select Exif Metadata Tags
#

# https://metacpan.org/pod/distribution/Image-MetaData-JPEG/lib/Image/MetaData/JPEG/Structures.pod#Structure-of-an-Exif-APP1-segment

# https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
# http://www.exiv2.org/tags.html
# See Page 30, 36 of the PDF

# hosted in APP1
exif_tags = {
	
	'DateTime'            :b'\x01\x32', # basically modify time
	'DateTimeOriginal'    :b'\x90\x03', # when original img data created
	'DateTimeDigitzed'    :b'\x90\x04', # when image was digitzed

	'SubSecTime'          :b'\x92\x90', # fractional seconds for DateTime
	'SubSecTimeOriginal'  :b'\x92\x91', # frac. sec. for DateTimeOriginal
	'SubSecTimeDigitzed'  :b'\x92\x92', 

	'OffsetTime'          :b'\x90\x10', # timezone for DateTime
	'OffsetTimeOriginal'  :b'\x90\x11',
	'OffsetTimeDigitzed'  :b'\x90\x12',

	'GPSInfo'  			  :b'\x88\x25',

	'Software'			  :b'\x01\x31'	# may or may not yield useful data...
}

#
# Select GPS Tags --> Only if GPSInfo exists
#

gps_tags = {
	
    'GPSVersionID'  	  :b'\x00\x00', 
	'GPSLatitudeRef'  	  :b'\x00\x01', # N or S
	'GPSLatitude'  		  :b'\x00\x02',
	'GPSLongitudeRef'  	  :b'\x00\x03', # E or W
	'GPSLongitude'  	  :b'\x00\x04',
	'GPSAltitudeRef'  	  :b'\x00\x05', # 0 (above sea), 1 (below sea)
	'GPSAltitude'  	      :b'\x00\x06'
}

relative_gps_tags = {

	0:	'GPSVersionID',  	  
	1:	'GPSLatitudeRef',  	  
	2:	'GPSLatitude',  		  
	3:	'GPSLongitudeRef',  	  
	4:	'GPSLongitude',  	 
	5:	'GPSAltitudeRef',  	  
	6:	'GPSAltitude'  	      
}
