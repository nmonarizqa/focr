
import os
import zipfile
import sys


def extract(path_to_zip_file):
    print "Extract File.."
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(os.path.join("..","data","delivery","000"))
    zip_ref.close()

if __name__ == "__main__":
    fname = sys.argv[1]
    extract(fname)


