import shutil
import os
import filecmp

fle = "pageant"

for i in range(10):
	print "Test Case "+str(i+1)+" Output:",
	shutil.copyfile("./test_data/I."+str(i+1),"./"+fle+".in")
	os.system(".\\"+fle+".exe")
	fin = open("./"+fle+".out", 'r')
	fin2 = open("./test_data/O."+str(i+1), 'r')
	a = fin.read()
	b = fin2.read()
	print a+" - "+b,
