#!/usr/bin/env python3

import os
import sys
import requests
from multiprocessing.dummy import Pool

def _download_image(args):
	img_url = args[0]
	seq = args[1]
	seq_count = args[2]
	filename = img_url.split("/")[-2]

	r = requests.get(img_url)
	with open('downloads/%s/%04.f.jpeg' % (seq, seq_count), 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)


def download_sequence(sequence_id):
	os.makedirs("downloads/%s" % sequence_id, exist_ok=True)

	image_list = []
	sequence_count = 0

	print("Downloading sequence information from mapillary...")
	r = requests.get('http://api.mapillary.com/v1/im/sequence?skey=%s' % sequence_id)
	for shot in r.json():
		for img_version in shot["map_image_versions"]:
			if img_version["name"] == "thumb-2048":
				image_list.append((img_version["url"], sequence_id, sequence_count))

		sequence_count += 1

	print("Starting download of %s images" % sequence_count)
	download_pool = Pool(4)
	download_pool.map(_download_image, image_list)
	download_pool.close()
	download_pool.join()
	print("Downloaded images into downloads/%s" % sequence_id)


if __name__ == "__main__":
	if len(sys.argv) < 2 or sys.argv[1] == "--help":
		print("Usage: python3 downloader.py <SEQUENCE-ID>")
	download_sequence(sys.argv[1])