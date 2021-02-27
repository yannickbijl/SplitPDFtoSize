import argparse
import os
import sys

import fitz    #pymupdf

def convert_mb_to_byte(max_size):
    return max_size * 1024 * 1024

def get_filesize(filename):
    try:
        return os.path.getsize(filename)
    except FileNotFoundError:
        get_error(f"Could not find or open {filename}")

def get_pdf(filename):
    return fitz.open(filename)

def split_pdf(filename, max_size):
    document1 = get_pdf(filename)
    max_pages = document1.pageCount - 1
    mid = round(max_pages / 2)
    splits = [mid]
    filesize_condition = True
    while filesize_condition:
        new_filenames = [create_new_filename(filename, x+1) for x in range(len(splits) + 1)]
        splitting = [-1] + splits + [max_pages]

        if len(new_filenames) >= max_pages:
            get_error("Cannot generate files smaller than required size")

        new_filesizes = generate_files(document1, new_filenames, splitting)
        status_filesizes, splits = get_status_and_splits(new_filesizes, splits, max_size, max_pages)
        filesize_condition = check_status(status_filesizes, new_filenames)

def get_status_and_splits(filesizes, splits, max_size, max_pages):
    status_filesizes = []
    for pos in range(len(filesizes)):
        if filesizes[pos] <= max_size:
            status_filesizes.append(True)
        else:
            if pos == 0:
                splits.insert(0, round(splits[pos]/2))
            elif pos == len(filesizes)-1:
                new_page_split = max_pages - round((max_pages - splits[pos])/2)
                splits.append(new_page_split)
            else:
                new_page_split = splits[pos] - round((splits[pos] - splits[pos-1])/2)
                splits.insert(pos, new_page_split)
            status_filesizes.append(False)
    return status_filesizes, splits

def check_status(status_filesizes, filenames):
    if all(status == True for status in status_filesizes):
        print("Successfully created files under specified size")
        return False
    else:
        print("Generated files are too large in size")
        print("Removing currently generated files")
        for new_file in filenames:
            os.remove(new_file)
        print("Attempting to generate smaller files")
        return True

def create_new_filename(filename, filecount):
    file_info = os.path.splitext(filename)
    return f"{file_info[0]}_{filecount}{file_info[1]}"

def generate_files(source_doc, filenames, pages):
    new_filesizes = []
    for pos in range(len(pages) -1):
        print(f"Generating file {filenames[pos]}")
        create_new_document(source_doc, pages[pos]+1, pages[pos+1], filenames[pos])
        new_filesizes.append(get_filesize(filenames[pos]))
    return new_filesizes

def create_new_document(doc, start_page, end_page, new_file):
        document2 = fitz.open()
        document2.insertPDF(doc, from_page=start_page, to_page=end_page, start_at=0)
        document2.save(new_file)
        document2.close

def get_error(error):
    print(error)
    print("Shutting down!")
    sys.exit()


def main():
    parser = argparse.ArgumentParser()
    # Text arguments
    parser.add_argument('-f', '--file', dest='textfile', type=str, required=True, help="")
    parser.add_argument('-s', '--size', dest='sizefile', type=int, required=False, default=20, choices=range(1,26), metavar="[1-25]", help="")
    args = parser.parse_args()

    filename = args.textfile
    max_size = convert_mb_to_byte(args.sizefile)
    if get_filesize(filename) >= max_size:
        split_pdf(filename, max_size)
    else:
        print("The file is already less or equal to the required size.")
    print("Processing done!")


main()