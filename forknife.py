import argparse
import os
import time
from datetime import datetime

import jpg_carver
import jpg_searcher
import jpg_timeline

DIRECTORY = "carved_jpgs"
BANNER = "============================================"
HALF_BANNER = "--------------------------------------------"

def analyze_image(image):
    """
    Takes a dd image and goes through the steps of carving out jpgs and 
    creating timelines for each in addition to searching for hidden files
    within in it. Displaying the output for each step.

    :param image: the dd image file
    """
	# parse disk image for jpgs
    start = time.clock()
    images_found = jpg_carver.carve_jpgs(image)
    end = time.clock() - start
    print("\nFound {} JPEG images in {:.4f} seconds".format(images_found, end))
    print("Parsing complete.")
    print(BANNER)
    
    # create timelines for images
    print(BANNER)
    print("Processing files in: " + DIRECTORY)
    date = "{:%B %d, %Y at %H:%M:%S}".format(datetime.now())
    print("Processing started on: " + date)
    print(BANNER)
    
    processed_files = jpg_timeline.process_files(DIRECTORY)

    #mass_print()
    jpg_sorted, no_time = jpg_timeline.date_sort_original()	# Ordered dict of Original Times: filename, List of JPG(s) w none

    timeline_name = jpg_timeline.generate_timeline(DIRECTORY, jpg_sorted)
    print("Generated JPG Timeline...." + timeline_name)

    report_name = jpg_timeline.generate_report(DIRECTORY, jpg_sorted)
    print("Generated JPG Report...." + report_name + "\n")

    print(BANNER)
    print("Total files processed: " + str(processed_files))
    print("Processing finished on: " + date)
    print("Hashes generated with: Python's 'hashlib' library.")
    print(BANNER)


    print(BANNER)
    print("Searching each image for hidden files\n")
    # search images for hidden files
    for fi in os.listdir(DIRECTORY):
        print("\nSearching {}".format(fi))
        hidden_files = jpg_searcher.scan_image("{}/{}".format(DIRECTORY, fi))
        if len(hidden_files) == 0:
            print("JPG image is clean")
        else:
            print("Files discovered within the JPG:")
            for f in hidden_files:
                print("\t{}".format(f))
        
        print("\n{}".format(HALF_BANNER))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Takes a dd image and carves out JPGs and creates timeline for each and seaching for hidden files',
        add_help=True
    )
    parser.add_argument('-i', dest='image', help='dd image', required=True)
    args = parser.parse_args()
    image = args.image
    analyze_image(image)