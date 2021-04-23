#!/usr/bin/python3

from PIL import Image
import os, glob
import ntpath

if not os.path.exists('neg'):
    os.makedirs('neg')

PHOTO_DIR = "BioID"
NEG_DIR   = "neg"
POS_DIR   = "pos"

def pgm2jpg(in_dir, out_dir):
    filepaths = glob.glob(os.path.join(in_dir, '*.pgm'))
    size = 150, 150

    for fp in filepaths:
        im = Image.open(fp)
        im = im.resize(size, Image.ANTIALIAS)
        fn = ntpath.basename(fp)[0:10] + '.jpg'
        out_file = os.path.join(out_dir, fn)
        im.save(out_file)
        print(out_file)


if __name__ == "__main__":
    pgm2jpg(PHOTO_DIR, NEG_DIR)

