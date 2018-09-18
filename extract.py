
import os
import zipfile
import sys

def extract(path_to_zip_file, output_path):
    print "Extract File.."
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(output_path)
    zip_ref.close()

if __name__ == "__main__":
    fname = sys.argv[1]
    extract(fname)


