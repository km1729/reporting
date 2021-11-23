#*******************************************************************************
# Name: nci_admin_function.py.
#*******************************************************************************
# common functions for NCI project
#*******************************************************************************
# 2019 AUG 23 WenmingLu Initial version
# 2020 MAR 31 WenmingLu Gadi & Python3 ready
# 2021 NOV 08 DavidLee adding list of excluded projects that will not trigger an
#             email notification
#*******************************************************************************

import os
import datetime
from nci_proj import *
from nci_user import *

# Return the closest mdss report
def get_mdss_report(yyyymmdd, pathReport, proj):
    year = int(yyyymmdd[0:4])
    month = int(yyyymmdd[4:6])
    mdssReport = proj+"_mdss_"+yyyymmdd[0:8]+".rpt"
    while os.path.exists(pathReport+mdssReport) == False:
        if year>=2020:
            mdssDate = datetime.datetime(year, month, 1)
            mdssReport = proj+"_mdss_"+mdssDate.strftime("%Y%m%d")+".rpt"   
        else:
            mdssDate = datetime.datetime(year, month, 1)
            mdssReport = proj+"_mdss_"+"20200101"+".rpt"
        if month==1:
            year = year -1
            month = 12
        else:
            month = month-1	     
    return  pathReport+mdssReport  

# Read $proj.config 
def read_users(proj_config, proj):
    users = dict()
    with open(proj_config, "r") as config:
        for line in config.readlines():
            login, fname, lname, email = line.split()
            new_user = user(proj, name=fname+"_"+lname, login=login, email=email)		
            users[login]=new_user
    return users

# Read $proj_mdss_$yyyymmdd.rpt
def read_mdss(mdss_file, users):
    total_disk = 0.0
    #total_inode = 0.0
    with open(mdss_file, "r") as mdss:
        for line in mdss.readlines():
            try:
                login_uid, umdss = line.split()
                login, uid = login_uid.split("(")
                umdss = int(umdss)
                total_disk += umdss
                users[login].set_umdss(umdss)
            except:
                None
    return total_disk
    
# Read $proj_gdata_$yyyymmdd.rpt
def read_gdata(gdata_file, users, excluded_projs):
    total_disk = 0.0
    total_inode = 0.0
    if os.path.exists(gdata_file) == False:
        print("!NOTE: Log for /g/data not available for the date of "+gdata_file[35:43])
        return (total_disk, total_inode)
    with open(gdata_file, "r") as gdata:
        for line in gdata.readlines():
            try:
                proj, login, size, files, inode = line.split()
                inode = float(inode)
                unit = size[-2:]
                usage = size[:-2]
	    
                if unit == "kB":
                    usage = float(usage)*1024.0
                if unit == "MB":
                    usage = float(usage)*pow(1024.0, 2)
                if unit == "GB":
                    usage = float(usage)*pow(1024.0, 3)
                if unit == "TB":
                    usage = float(usage)*pow(1024.0, 4)
                
                total_disk += usage
                total_inode += inode
                if proj not in excluded_projs:
                    users[login].add_ugdata(usage)
                    users[login].add_igdata(inode)
                    users[login].add_ugdata_projs(proj)
            except:
                None
    return (total_disk, total_inode)

# Read $proj_scratch_$yyyymmdd.rpt
def read_scratch(scratch_file, users):
    total_disk = 0.0
    if os.path.exists(scratch_file) == False:
        print("!NOTE: Log for /scratch not available for the date of "+scratch_file[37:45])
        return total_disk    
    with open(scratch_file, "r") as scratch:
        for line in scratch.readlines():
            try:
                proj, login, size, files, inode = line.split()
                unit = size[-2:]
                usage = size[:-2]
	    
                if unit == "kB":
                    usage = float(usage)*1024.0
                if unit == "MB":
                    usage = float(usage)*pow(1024.0, 2)
                if unit == "GB":
                    usage = float(usage)*pow(1024.0, 3)
                if unit == "TB":
                    usage = float(usage)*pow(1024.0, 4)
                
                total_disk += usage
                users[login].add_uscratch(usage)
            except:
                None
    return total_disk

def read_age(age_file, user, proj):
    if os.path.exists(age_file) == False:
        return (0, 0)
     
    disk = 0
    iusage = 0
    with open(age_file, "r") as age:
        for line in age.readlines():
            try:
                uid, project, size, tag, path = line.split(",")
                if uid == user and project == proj:
                    disk = disk + int(size)
                    iusage = iusage + 1
            except:
                None
    return (disk/pow(1024.0, 3), iusage)

# Read $proj_$yyyymmdd.rpt
def read_su(project_file, users=None):
    suQ = 0.001
    suU = 0.0
    if os.path.exists(project_file) == False:
        print("!NOTE: Log for SU not available for the date of "+project_file[29:37])
        return (suU, suQ) 
    with open(project_file, "r") as project:
        index = 1
        for line in project.readlines():
            try:
                if index==4:
                    term, suQ, unit = line.split()
                    if unit=="MSU":
                        suQ = float(suQ)
                    elif unit=="KSU":
                        suQ = float(suQ)/1000
                    elif unit=="SU":
                        suQ = float(suQ)/1000000
                elif index==5:
                    term, suU, unit = line.split()
                    if unit=="MSU":
                        suU = float(suU)
                    elif unit=="KSU":
                        suU = float(suU)/1000
                    elif unit=="SU":
                        suU = float(suU)/1000000
                elif index>15:
                    login, su, unit, trash1, trash2 = line.split()
                    if unit=="MSU":
                        su = float(su)*1000000
                    elif unit=="KSU":
                        su = float(su)*1000
                    elif unit=="SU":
                        su = float(su)
                    users[login].set_su(su)	
            except:
                None
            index = index+1
    return (suU, suQ)  

def get_su_reports(yyyymmdd, proj, option):
    year = int(yyyymmdd[0:4])
    month = int(yyyymmdd[4:6])
    day = int(yyyymmdd[6:])
    thisDate = datetime.datetime(year, month, day)

    if month in [1,2,3]:
        start = datetime.datetime(year, 1, 1)
        finish = datetime.datetime(year, 3, 30)	    
    elif month in [4,5,6]:
        start = datetime.datetime(year, 4, 1)
        finish = datetime.datetime(year, 6, 30)	    
    elif month in [7,8,9]:
        start = datetime.datetime(year, 7, 1)
        finish = datetime.datetime(year, 9, 30)	    
    elif month in [10,11,12]:	
        start = datetime.datetime(year, 10, 1)
        finish = datetime.datetime(year, 12, 31)
    START=start
    print("YYYYYMMDD \tUSAGE \t\tDAILY_AVG \tQUOTA \tPROJECTION")
    print("-"*66)
    while (thisDate-start).days>=0:
        ymd = start.strftime("%Y%m%d")
        report_proj = proj+"_"+ymd+".rpt"
        (su_usage, su_quota) = read_su(path_report+report_proj)
        
        daysInQuater = 	(finish-START).days+1	
        daysGone = (start-START).days+1
        avgSU = su_usage/daysGone 
        projectionSU = avgSU*daysInQuater
	
        print("%6s \t%.2fMSU \t%.2fKSU \t%.1fMSU \t%.1fMSU" % \
            (ymd, su_usage, avgSU*1000, su_quota, projectionSU))
        start = start+datetime.timedelta(days=1)    
    if (su_usage>su_quota*0.9 or projectionSU>su_quota) and option == "z":
        with open(path_notice+su_warning, "w") as output:
            output.write("YYYYYMMDD \tUSAGE \t\tDAILY_AVG \tQUOTA \tPROJECTION\n")
            output.write("%6s \t%.2fMSU \t%.2fKSU \t%.1fMSU \t%.1fMSU" % \
                (ymd, su_usage, avgSU*1000, su_quota, projectionSU))  

def process_age_left(age_file, age_file_left, user, proj):
    age = open(age_file, "r")
    age_left = open(age_file_left, "w")   
    
    for line in age.readlines():
        try:
            uid, project, size, tag, path = line.split(",")
            if uid == user and project == proj:
                if os.path.exists(path.strip()):
                    age_left.write(line)
        except:
            None
    
    age.close()
    age_left.close()

