import argparse
import time
import jpg_carver
import jpg_searcher

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