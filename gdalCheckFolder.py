#Run as scidb user
import os
import sys
import time
import subprocess as subp
import argparse
import datetime
import logging
#********************************************************
#WORKER
#********************************************************
def main(argv):
	parser = argparse.ArgumentParser(description = "Monitors a folder for SDBBIN (gdal-generated) files for uploading to SCIDB")
	parser.add_argument("path_to_watch", help = "Folder path")
	parser.add_argument("scriptFolder", help = "Folder containing python scripts")
	parser.add_argument("destArray", help = "3D Array to upload the data to")
	parser.add_argument("-t", "--checktime", help = "Waiting time between folder inspections", type = int, default = 60)
	parser.add_argument("--log", help = "Log level", default = 'WARNING')
	#Get paramters
	args = parser.parse_args()
	path_to_watch = args.path_to_watch
	scriptFolder = args.scriptFolder
	destArray = args.destArray
	checktime = args.checktime
	log = args.log
	####################################################
	# CONFIG
	####################################################
	numeric_loglevel = getattr(logging, log.upper(), None)
	if not isinstance(numeric_loglevel, int):
		raise ValueError('Invalid log level: %s' % log)
	logging.basicConfig(filename = 'log_checkFolder.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
	logging.info("addHdfs2bin: " + str(args))
	#
	#checktime = 60 # seconds
	## GIS-OBAMA
	#path_to_watch = "/mnt/lun0/test/toLoad/"
	#scriptFolder = '/mnt/lun0/test/test013/scripts/'
	# CHRONOS
	#path_to_watch = "/dados/scidb/toLoad/"
	#scriptFolder = '/dados/scidb/scripts/'
	####################################################
	# SCRIPT
	####################################################
	cmdprefix = "python " + scriptFolder + "gdalLoad2scidb.py --log INFO "
	before = dict ([(f, None) for f in os.listdir (path_to_watch)])
	while 1:
		time.sleep (checktime)
		#print "Checkin " + path_to_watch + " for new hdfs..."
		after = dict ([(f, None) for f in os.listdir (path_to_watch)])
		added = [f for f in after if not f in before]
		if added:
			logging.debug("Added: ", ", ".join(added))
			for ad in added:
				fileFullPath = path_to_watch + str(ad)
				fileName, fileExtension = os.path.splitext(fileFullPath)
				if(fileExtension == '.sdbbin'):
					#Call to gdalLoad2scidb.py
					if path_to_watch[-1:] == '/':
						binaryFilepath = path_to_watch + str(ad)
					else:
						binaryFilepath = path_to_watch + '/' + str(ad)
					cmd = cmdprefix + binaryFilepath + " " + destArray
					print cmd
					logging.info(cmd)
					try:
						subp.check_call(str("date"), shell=True)
						subp.check_call(str(cmd), shell=True)
						subp.check_call(str("date"), shell=True)
						os.remove(fileFullPath)
						subp.check_call(str("date"), shell=True)
					except subp.CalledProcessError as e:
						logging.exception("CalledProcessError: " + cmd + "\n" + str(e.message))
					except ValueError as e:
						logging.exception("ValueError: " + cmd + "\n" + str(e.message))
					except OSError as e:
						logging.exception("OSError: " + cmd + "\n" + str(e.message))
					except:
						e = sys.exc_info()[0]
						logging.exception("Unknown exception: " + cmd + "\n" + str(e.message))
		before = after

	
if __name__ == "__main__":
   main(sys.argv[1:])
