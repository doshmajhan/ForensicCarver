import argparse
import binwalk

def scan_image(image):
    """
    Uses the binwalk module to search for other files within the given image

    :param image: the image file to search

    :returns: an array containing files found in the image if any
    """
    carved_files = list()
    signatures = binwalk.scan(image, signature=True, extract=True, quiet=True)[0]

    for result in signatures.results:
        if signatures.extractor.output.has_key(result.file.path):
            # These are files that binwalk carved out of the original firmware image, a la dd
            if signatures.extractor.output[result.file.path].carved.has_key(result.offset):
                carved_file_name = signatures.extractor.output[result.file.path].carved[result.offset]
                carved_files.append(carved_file_name)
                print("Carved data from offset 0x{:x} to {}".format(result.offset, carved_file_name))
        
            # These are files/directories created by extraction utilities (gunzip, tar, unsquashfs, etc)
            if signatures.extractor.output[result.file.path].extracted.has_key(result.offset):
                print("Extracted {} files from offset 0x{:x} to '{}' using '{}'".format(
                    len(signatures.extractor.output[result.file.path].extracted[result.offset].files),
                    result.offset,
                    signatures.extractor.output[result.file.path].extracted[result.offset].files[0],
                    signatures.extractor.output[result.file.path].extracted[result.offset].command))

    return carved_files
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Looks for other files hidden within the given JPG image', add_help=True)
    parser.add_argument('-f', dest='file', help='The JPG image to search in', required=True)
    args = parser.parse_args()
    image = args.file
    files = scan_image(image)
    if len(files) == 0:
        print("JPG image is clean")
    else:
        print("Files discovered within the JPG:")
        for file in files:
            print("\t{}".format(file))