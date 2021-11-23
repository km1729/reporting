# 2020 OCT 08 WenmingLu Convert report of scratch&gdata to old format
#*******************************************************************************

import sys

fileInputPath=sys.argv[1]
fileOutputPath=sys.argv[2]

fileOutput=open(fileOutputPath, "w")
fileOutput.write("------------------------------------------------------------------------------\n")
fileOutput.write("         project             user     space used      file size          count\n")
fileOutput.write("------------------------------------------------------------------------------\n")

with open(fileInputPath, "r") as fileInput:
    for line in fileInput.readlines():
        try:
            fileSystem, scanDate, project, group, user, spaceUsed, totalSize, count = line.split()
            spaceUsed = spaceUsed.replace("K", "k").replace("B","k")
            totalSize = totalSize.replace("K", "k").replace("B","k")
            fileOutput.write("%16s %16s %13sB %13sB %14s\n" % (project, user, spaceUsed, totalSize, count))
        except:
            None

fileOutput.write("------------------------------------------------------------------------------\n")
fileOutput.close()
