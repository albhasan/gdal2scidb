import os
import sys
import argparse
import datetime
import subprocess as subp
import logging
from subprocess import check_output as qx
##################################################
# CREATE DESTINATION ARRAY
##################################################
#iquery -o dcsv -a
#set lang aql;
#DROP ARRAY BLISS_TEST009GDAL_20140520;
#CREATE ARRAY BLISS_TEST009GDAL_20140520 <band01:double, band02:double, band03:double> [col_id=0:14840, 502, 5,row_id=0:10915, 502, 5, time_id=0:20000, 1, 0];
##################################################
# GET TIME SERIES
##################################################
#iquery -o dcsv -a
#set lang aql;
#SELECT * FROM BLISS_TEST009GDAL_20140520 WHERE col_id = 0 AND row_id = 0;
#time iquery -q "SELECT * FROM BLISS_TEST009GDAL_20140520 WHERE col_id = 0 AND row_id = 0"

#********************************************************
# UTIL
#********************************************************
def getArrayname(aname):
	'''Return a valid SciDB array name from the input'''
	res = aname
	res = res.replace(".","_")
	res = res.replace("-","_")
	return res


def getArrayDescription(arrayName):
	#TODO: Improve!!!!!!!!!!!!!!!!!
	res = []
	resCmd = subp.check_output(["iquery", "-aq", "show(" +  arrayName + ")"])
	strAtt = resCmd[resCmd.index('<') + 1:resCmd.index('>')]
	strDim = resCmd[resCmd.index('[') + 1:resCmd.index(']')]
	strAttArray = strAtt.split(',')
	dims = processArrayDimensions(strDim)
	atts = []
	for strSinAtt in strAttArray:
		atts.append(processArrayAttribute(strSinAtt))
	res.append(atts)
	res.append(dims)
	return res
	
	
def processArrayDimensions(strDim):
	strDimArray = strDim.split(',')
	res = []
	for dim in range(len(strDimArray) / 3):
		dname, dinterval = strDimArray[dim * 3].split('=')
		dfrom, dto = dinterval.split(':')
		dchunk = strDimArray[dim * 3 + 1]
		doverlap = strDimArray[dim * 3 + 2]
		dim = {'name': dname, 'start': dfrom, 'end': dto, 'chunksize': dchunk, 'overlap': doverlap}
		res.append(dim)
	return res
	
	
def processArrayAttribute(strSinAtt):
	sp = strSinAtt.split(' ')
	atname = ""
	atdatatype = ""
	atnull = ""
	atdefault = ""
	if len(sp) >= 1:
		atname,atdatatype = sp[0].split(':')
	if len(sp) >= 2:
		atnull = sp[1]
	if len(sp) == 3:
		atdefault = sp[2]
	res = {'name': atname, 'datatype': atdatatype, 'null': atnull, 'default': atdefault}
	return res
	
	
	
def load2scidbGdal(bfile, DESTARRAY, chunkSize1D, cmdaql, cmdafl, loadInstance, maxErrors):
	'''Load the binary file to SciDB'''
	#---------------
	# Script starts here
	#---------------
	cmd = ""
	try:
		ad = getArrayDescription(DESTARRAY)
		DESTARRAYatts = ad[0]
		DESTARRAYdims = ad[1]
		tmparraylist = []
		fieldDataTypes = []
		bpath, bfilename = os.path.split(bfile)
		TMP_VALUE1D = getArrayname(bfilename)
		#---------------
		#Create the temporal 1D array for holding the data
		#---------------
		attNames = []
		for dim in DESTARRAYdims:
			aName = dim['name'] + ":int64"
			attNames.append(aName)
			fieldDataTypes.append("int64")
		for att in DESTARRAYatts:
			aName = att['name'] + ":" + att['datatype']
			attNames.append(aName)
			fieldDataTypes.append(att['datatype'])
		#aql = "CREATE ARRAY " + TMP_VALUE1D + " <col_id:int64, row_id:int64, time_id:int64, band01:double, band02:double, band03:double> [k=0:*," + str(chunkSize1D) + ",0];"
		aql = "CREATE ARRAY " + TMP_VALUE1D + " <" + ", ".join(attNames) + "> [k=0:*," + str(chunkSize1D) + ",0];"
		cmd = cmdaql + aql + "\""
		retcode = subp.call(cmd, shell = True)#os.system(cmd)
		tmparraylist.append(TMP_VALUE1D)
		logging.debug("GDAL - Created the 1D array for the values: " + TMP_VALUE1D)
		#---------------
		#Load to 1D temporal array
		#---------------
		afl = "load(" + TMP_VALUE1D + ", '" + bfile + "', " + str(loadInstance) + ", '(" + ", ".join(fieldDataTypes) + ")', " + str(maxErrors) + ", shadowArray);"#afl = "load(" + TMP_VALUE1D + ", '" + bfile + "', " + str(loadInstance) + ", '(int64, int64, int64, float, float, float)', 0, shadowArray);"
		cmd = cmdafl + afl + "\""
		retcode = subp.call(cmd, shell = True)#os.system(cmd)
		logging.debug("GDAL - Loaded the binary file to 1D-Array using instance " + str(loadInstance))
		#---------------
		#Re-build dimension indexes and insert into the destination array
		#---------------
		afl = "insert(redimension(" + TMP_VALUE1D + ", " + DESTARRAY + ")," + DESTARRAY + ");"
		cmd = cmdafl + afl + "\""
		retcode = subp.call(cmd, shell = True)#os.system(cmd)
		logging.debug("GDAL - Dimension indexes are built and inserted into array " + DESTARRAY)
		#---------------
		#Removes temporal arrays
		#---------------
		for an in tmparraylist:
			aql = "DROP ARRAY " + an + ";"
			cmd = cmdaql + aql + "\""
			retcode = subp.call(cmd, shell = True)
		logging.debug("GDAL - Temporal arrays dropped")
	except subp.CalledProcessError as e:
		logging.exception("CalledProcessError: " + cmd + "\n" + str(e.message))
	except ValueError as e:
		logging.exception("ValueError: " + cmd + "\n" + str(e.message))
	except OSError as e:
		logging.exception("OSError: " + cmd + "\n" + str(e.message))
	except:
		e = sys.exc_info()[0]
		logging.exception("Unknown exception: " + cmd + "\n" + str(e.message))

#********************************************************
#WORKER
#********************************************************
def main(argv):
	t0 = datetime.datetime.now()
	parser = argparse.ArgumentParser(description = "Loads a SCIDB's binary (exported from GDAL) file to SCIDB")
	parser.add_argument("binaryFilepath", help = "Path to a binary file (*.sdbbin exported from GDAL)")
	parser.add_argument("destArray", help = "3D Array to upload the data to")
	parser.add_argument("-c", "--chunkSize1D", help = "Chunksize for the temporal 1D-array holding the loaded data", type = int, default = 262144)
	parser.add_argument("-l", "--loadInstance", help = "SciDB's instance used for uploading the data", type = int, default = -2)
	parser.add_argument("-e", "--maxErrors", help = "Maximum allowed errors while loading data", type = int, default = 0)
	parser.add_argument("--log", help = "Log level", default = 'WARNING')
	#Get paramters
	args = parser.parse_args()
	binaryFilepath = args.binaryFilepath	
	destArray = args.destArray
	chunkSize1D = args.chunkSize1D
	loadInstance = args.loadInstance
	maxErrors = args.maxErrors
	log = args.log
	####################################################
	# CONFIG
	####################################################
	numeric_loglevel = getattr(logging, log.upper(), None)
	if not isinstance(numeric_loglevel, int):
		raise ValueError('Invalid log level: %s' % log)
	logging.basicConfig(filename = 'log_gdalLoad2scidb.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
	logging.info("gdalLoad2scidb: " + str(args))
	#
	iqpath = "/opt/scidb/14.3/bin/" # Path to iquery
	cmdaql = iqpath + "iquery -nq \"" # Prefix on how to call iquery with AQL expression
	cmdafl = iqpath + "iquery -naq \"" # Prefix on how to call iquery with AFL expression
	#loadInstance = -2 #HACK: -2 (Load all data using the coordinator instance of the query.) is way faster than -1(Initiate the load from all instances)
	#TODO: Try named instances for loading when a multi-node SciDB is in place
	####################################################
	# SCRIPT
	####################################################
	load2scidbGdal(binaryFilepath, destArray, chunkSize1D, cmdaql, cmdafl, loadInstance, maxErrors)
	t1 = datetime.datetime.now()
	tt = t1 - t0
	logging.info("Done in " + str(tt))
	
	
if __name__ == "__main__":
   main(sys.argv[1:])
