#!/usr/bin/env python3

#*******************************************************************************
# Name: nci_admin.py.
#*******************************************************************************
# Check users' quota/iUsage on NCI HPC mdss, /short and /g/data
# Create notices to users who overuse resources
#*******************************************************************************
# 2019 AUG 23 WenmingLu Initial version
# 2020 APR 05 WenmingLu Python3
# 2020 MAY 01 WenmingLu Adding functions for guest users, extra -r options
# 2020 JUN 16 WenmingLu Adding /scratch 
# 2020 JUN 19 WenmingLu SU management
# 2021 NOV 08 DavidLee adding list of excluded projects that will not trigger an
#             email notification
#*******************************************************************************


import argparse
import datetime
import sys
from nci_proj import *
from nci_user import *
from nci_admin_function import *
from nci_admin_config import *
from contextlib import suppress

#__main__
parser = argparse.ArgumentParser(description='NCI Resource Management')
parser.add_argument('-p', '--proj', dest='proj', required=True, help='project')
parser.add_argument('-d', '--ymd', dest='ymd', default="", help='yyyymmdd')
parser.add_argument('-u', '--user', dest='user', default="all", help='all/user')
parser.add_argument('-c', '--core', dest='core', default="core", help='core/guest')
parser.add_argument('-r', '--report', dest='report', default="1", \
                    help='1->proj info, 2[a/b/c]->top users[mdss/gdata/igdata], 3->setting, 4->user table')
parser.add_argument('-v', '--verbose', default=1)
parser.add_argument('--debug', default=0)

args=parser.parse_args(sys.argv[1:])
if args.ymd != "":
    yyyymmdd = args.ymd
else:
    yyyymmdd = str(datetime.date.today()).replace("-", "")
proj = args.proj
user = args.user
report = int(args.report[0])
args.core = "Core" if args.core == "core" else "Guest"
file_user = file_core if args.core == "Core" else file_guest

report_proj = proj+"_"+yyyymmdd+".rpt"
report_mdss = get_mdss_report(yyyymmdd, path_report, proj)
report_proj_gdata = proj+"_gdata_"+yyyymmdd+".rpt"
report_proj_scratch = proj+"_scratch_"+yyyymmdd+".rpt"

new_proj = project(proj, quota_gdata, quota_igdata, quota_mdss, quota_imdss, 0, 0, 0, 0, quota_scratch, 0)
users = read_users(path_config+file_user, new_proj)
mdss_usage = read_mdss(report_mdss, users)
excluded_projs = ['ig2','lb4','wr45','ja4','access']
(gdata_usage, gdata_inode) = read_gdata(path_report+report_proj_gdata, users, excluded_projs)
scratch_usage = read_scratch(path_report+report_proj_scratch, users)
(su_usage, su_quota) = read_su(path_report+report_proj, users)
new_proj.set_gdata_disk_usage(gdata_usage*1.0/pow(1024, 4))
new_proj.set_gdata_inode_usage(gdata_inode*1.0/pow(10, 6))
new_proj.set_mdss_tape_usage(mdss_usage*1.0/pow(1024, 4))
new_proj.set_scratch_disk_usage(scratch_usage*1.0/pow(1024, 4))
new_proj.set_su_quota(su_quota)
new_proj.set_su_usage(su_usage)

total_mdss_usage  = 0.0
total_gdata_usage = 0.0
total_gdata_inode = 0
total_scratch_usage = 0.0
for login in users:
    total_mdss_usage += users[login].get_umdss()
    total_gdata_usage += users[login].get_ugdata()
    total_gdata_inode += users[login].get_igdata()
    total_scratch_usage += users[login].get_uscratch()

# Finding top users for each category
dict_mdss = {}
dict_gdata = {}
dict_igdata = {}
dict_scratch = {}
dict_su = {}

for u in users:
    dict_mdss[users[u].get_login()] = users[u].get_umdss() 
    dict_gdata[users[u].get_login()] = users[u].get_ugdata()
    dict_igdata[users[u].get_login()] = users[u].get_igdata()
    dict_scratch[users[u].get_login()] = users[u].get_uscratch()
    dict_su[users[u].get_login()] = users[u].get_su()
    
dict_mdss = sorted(dict_mdss.items(), key=lambda x: x[1])
dict_mdss.reverse()
dict_gdata = sorted(dict_gdata.items(), key=lambda x: x[1])
dict_gdata.reverse()
dict_igdata = sorted(dict_igdata.items(), key=lambda x: x[1])
dict_igdata.reverse()
dict_scratch = sorted(dict_scratch.items(), key=lambda x: x[1])
dict_scratch.reverse()
dict_su = sorted(dict_su.items(), key=lambda x: x[1])
dict_su.reverse()

# Print reports
if user != "all" :
    try:
        print(users[user])
    except:
        print("User %s does not exist in %s User List!" % (user, args.core))    	
else:
    if report == 0:
        for u in users:
            if 	int(args.debug) == 1: 
                if users[u].get_notify():
                    print(users[u])

            if users[u].get_notify():
                with open(path_notice+users[u].get_email(), "w") as output:
                    if args.core == "Core":
                        output.write(users[u].get_user_message())
                    elif args.core == "Guest":
                        output.write(users[u].get_guest_message())		
                    output.close()			     

    elif report == 1:
        print(new_proj)

    elif report == 2:
        topusers = "b"
        TOPUSERS = {"a":"MDSS", "b":"/g/data", "c":"/g/data inode", "d":"/scratch", "e":"SU" }	    
	    
        with suppress(IndexError): topusers = args.report[1]
	
        print("%4s \t %5s" % ("USER", "USAGE"))      
        print("="*18)
        if topusers == "a":
            for item in dict_mdss[:top_user_index]:
                print("%6s \t %4dT" % (item[0], item[1]/pow(1024,4)))
        elif topusers == "b":
            for item in dict_gdata[:top_user_index]:
                print("%6s \t %.2fT" % (item[0], item[1]/pow(1024,4))) 
        elif topusers == "c":
            for item in dict_igdata[:top_user_index]:
                print("%6s \t %.2fM" % (item[0], item[1]/pow(10,6)))   
        elif topusers == "d":
            for item in dict_scratch[:top_user_index]:
                print("%6s \t %.2fT" % (item[0], item[1]/pow(1024,4))) 
        elif topusers == "e":
            for item in dict_su[:top_user_index]:
                print("%6s \t %.2fKSU" % (item[0], item[1]/pow(10,3))) 
        print("="*18)
        print("These are Top Users in "+TOPUSERS[topusers]+" of "+proj+" for "+args.core+" Members.")

    elif report == 3:
        print("=== General Setting for " + new_proj.get_proj() + " ===")
        print("Max Individual Share of mdss Tape = %d%% (%dT)" % (limit_mdss*100, quota_mdss*limit_mdss))
        print("Max Individual Share of /g/data Disk = %d%% (%dT)" % (limit_gdata*100, quota_gdata*limit_gdata))
        print("Max Individual Share of /g/data inode = %d%% (%.2fM)" % (limit_igdata*100, quota_igdata*limit_igdata))
        print("Max Individual Share of /scratch Disk = %d%% (%dT)" % (limit_scratch*100, quota_scratch*limit_scratch))        
        print("Emergency Level of mdss Tape Usage = %d%%" % (warning_mdss*100))
        print("Emergency Level of /g/data Disk Usage = %d%%" % (warning_gdata*100))
        print("Emergency Level of /g/data inode Usage = %d%%" % (warning_igdata*100))
        print("Emergency Level of /scratch Disk Usage = %d%%" % (warning_scratch*100))
        print("Emergency mdss Big User Threshold = %dT" % (warning_mdss_disk))	
        print("Emergency /g/data Disk Big User Threshold = %dT" % (warning_gdata_disk))        	
        print("Emergency /g/data inode Big User Threshold = %dM" % (warning_gdata_inode))
        print("Emergency /scratch Disk Big User Threshold = %dT" % (warning_scratch_disk))        
        print("Guest /g/data/dp9 Usage <= %dG" % (warning_gdata_disk_guest))
        print("Guest /g/data/dp9 inode <= %dM" % (warning_gdata_inode_guest))
        print("Guest /mdss dp9 Usage = %dT" % (warning_mdss_disk_guest))	
        print("Guest /scratch/dp9 Usage <= %dG" % (warning_scratch_disk_guest))         	
	
    elif report == 4:
        print("<<<<<< %s User Info for %s >>>>>>" % (args.core, new_proj.get_proj()))
        print ("%s /g/data/dp9 Usage\t= %dT" % (args.core, total_gdata_usage/pow(1024, 4)))
        print ("%s /g/data/dp9 inode\t= %dM" % (args.core, total_gdata_inode/pow(10, 6)))
        print ("%s /mdss dp9 Usage \t= %dT" % (args.core, total_mdss_usage/pow(1024, 4)))
        print ("%s /scratch/dp9 Usage = %dT" % (args.core, total_scratch_usage/pow(1024, 4)))	
        print("="*82)
        print ("%4s \t %10s \t %11s \t %9s \t %7s \t %7s" % ("USER", "GDATA_DISK", "GDATA_INODE", "MDSS_TAPE", "SCRATCH", "SU"))
        print("="*82)
        for item in dict_gdata:
            login = item[0]
            udata = item[1]/pow(1024,3)
            igdata = users[login].get_igdata()/pow(10,3)
            umdss = users[login].get_umdss()/pow(1024,3)
            uscratch = users[login].get_uscratch()/pow(1024,3)
            su = users[login].get_su()/pow(10,3)
            print ("%6s \t %6dG \t %6dK \t %6dG \t %6dG \t %6dKSU" % (login, udata, igdata, umdss, uscratch, su)) 

    elif report == 5:
        option = None
        with suppress(IndexError): option = args.report[1]
        get_su_reports(yyyymmdd, proj, option)        
    

