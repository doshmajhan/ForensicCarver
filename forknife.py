import argparse
import time
from datetime import datetime

import jpg_carver
import jpg_searcher
import jpg_timeline

DIRECTORY = "carved_jpgs"

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
    print("------------------------------------------")

    # create timelines for images

    print(jpg_timeline.banner)
    print("Processing files in: " + DIRECTORY)
    date = "{:%B %d, %Y at %H:%M:%S}".format(datetime.now())
    print("Processing started on: " + date)
    print(jpg_timeline.banner)
    
    processed_files = jpg_timeline.process_files(DIRECTORY)

    #mass_print()
    jpg_sorted, no_time = jpg_timeline.date_sort_original()	# Ordered dict of Original Times: filename, List of JPG(s) w none

    timeline_name = jpg_timeline.generate_timeline(DIRECTORY, jpg_sorted)
    print("Generated JPG Timeline...." + timeline_name)

    report_name = jpg_timeline.generate_report(DIRECTORY, jpg_sorted)
    print("Generated JPG Report...." + report_name + "\n")

    print(jpg_timeline.banner)
    print("Total files processed: " + str(processed_files))
    print("Processing finished on: " + date)
    print("Hashes generated with: Python's 'hashlib' library.")
    print(jpg_timeline.banner)


    # search images for hidden files



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Takes a dd image and carves out JPGs and creates timeline for each and seaching for hidden files',
        add_help=True
    )
    parser.add_argument('-i', dest='image', help='dd image', required=True)
    args = parser.parse_args()
    image = args.image
    analyze_image(image)