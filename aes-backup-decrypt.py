import os, sys, time
import subprocess
from getpass import getpass
import progressbar
import multiprocessing
import argparse
import datetime

def decrypt_file_shell(input_all):
	in_file, out_file, key, verbose= input_all
	if verbose:
		print('Decryptyng to %s' % out_file)
	try:
		res = subprocess.run(['openssl', 'aes-256-cbc', '-d', '-k', key, '-in', in_file, '-out', out_file],
			text=True,
			stdout=subprocess.PIPE,
			check=True)
		result = res.stdout.split('\n')
	except Exception:
		result = None

def decrypt_file_shell_multiprocess(input_all):
	in_file, out_file, key, verbose= input_all
	#if verbose:
		#print('Decryptyng to %s' % out_file)
	try:
		res = subprocess.run(['openssl', 'aes-256-cbc', '-d', '-k', key, '-in', in_file, '-out', out_file],
			text=True,
			stdout=subprocess.PIPE,
			check=True)
		result = res.stdout.split('\n')
	except Exception:
		result = None

def decrypt_qnap_folders(path, npath, key, multiprocess_bool=False, verbose=False):
	# Variables for storing the roots and the files in input and output 
	fname = []
	roots = set()
	process_counter = 0

	# Absolute paths
	path = os.path.abspath(path)
	npath = os.path.abspath(npath)

	# Scan the input directory
	file_filtered = [".DS_Store"]
	for root,d_names,f_names in os.walk(path):
		for f in f_names:
			if f not in file_filtered:
				new_root = root.replace(path,npath)
				roots.add(new_root)
				fname.append((os.path.join(root, f),os.path.join(new_root, f),key,verbose))

	start_time = time.time()

	# Create the new foler and subdirectories 
	for new_folder in roots:
		if not os.path.exists(new_folder):
			if verbose:
				print("Creating folder %s" % new_folder)
			os.makedirs(new_folder)

	# Convert files
	l = len(fname)
	bar = progressbar.ProgressBar(max_value=l, redirect_stdout=verbose)

	if not multiprocess_bool:
		# File counter and number of files
		i = 0
		for fname_single in fname:
			i+=1
			decrypt_file_shell(fname_single)
			bar.update(i)
	else:
		
		print("Start multiprocessing")
		pool = multiprocessing.Pool(4)
		r = pool.map_async(decrypt_file_shell_multiprocess, fname, chunksize=1)

		last_process_left=-1
		while not r.ready():
			new_process_left = r._number_left	
			if not new_process_left == last_process_left:
				bar.update(l-r._number_left+1)
				if verbose:
					print('Decryptyng to %s' % fname[int(r._number_left)-1][1])
			last_process_left = new_process_left
		r.wait()
		pool.close()
		bar.update(l)
	#print("\n All done in", str(datetime.timedelta(seconds=int(time.time()-start_time))))


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("in_folder", help="path with encrypted files and folders")
	parser.add_argument("out_folder",  help="path to save decrypted files and folders")
	parser.add_argument("-m", "--multiprocess", help="increase output verbosity", action="store_true")
	parser.add_argument("-v", "--verbose", help="enable multiprocess execution", action="store_true")
	args = parser.parse_args()
	print("Enter password to start decrypting:")
	key = getpass()
	decrypt_qnap_folders(args.in_folder, args.out_folder, key, args.multiprocess, args.verbose)
	print()
