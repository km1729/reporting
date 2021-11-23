#!/usr/bin/env python3

#*******************************************************************************
# Name: nci_admin_age.py.
#*******************************************************************************
# Check users' aged disk/iUsage on NCI HPC /short and /g/data
# Create notices to users who overuse resources
#*******************************************************************************
# 2019 AUG 27 WenmingLu Initial version
# 2020 OCT 15 WenmingLu Gadi & Python3 version
#*******************************************************************************

import argparse
import sys
from nci_proj import *
from nci_user import *
from nci_admin_function import *
from nci_admin_config import *

#__main__
parser = argparse.ArgumentParser(description='NCI Resource Management for Aged Files')
parser.add_argument('-p', '--proj', dest='proj', required=True, help='project')
parser.add_argument('-u', '--user', dest='user', default="all", help='all/user')
parser.add_argument('-t', '--target', dest='target', default=1024, help='target')
parser.add_argument('-c', '--core', dest='core', default="core", help='core/guest')
parser.add_argument('-v', '--verbose', default=1)
parser.add_argument('--debug', default=0)

args=parser.parse_args(sys.argv[1:])
proj = args.proj
user= args.user
args.core = "Core" if args.core == "core" else "Guest"
file_user = file_core if args.core == "Core" else file_guest

age_file_gdata = path_age+user+".gdata"
new_proj = project(proj, quota_gdata, quota_igdata, quota_mdss, quota_imdss, 0, 0, 0, 0, quota_scratch, 0)
users = read_users(path_config+file_user, new_proj)


if user == "all":
    age_total = 0
    age_left = 0        
    for u in users:
        age_file = path_age+u+".gdata"
        age_file_left = age_file+".left"
        process_age_left(age_file, age_file_left, u, proj)
        (age_disk, age_iusage) = read_age(age_file, u, proj)
        (age_disk_left, age_iusage_left) = read_age(age_file_left, u, proj)
        age_total += age_disk
        age_left += age_disk_left
    print("Total Aged Files = %dTB" % (age_total/1024))
    print("Total Aged Files Left = %dTB" % (age_left/1024))       
else:
    age_file = path_age+user+".gdata"
    age_file_left = age_file+".left"        
    (age_disk, age_iusage) = read_age(age_file, user, proj)
    (age_disk_left, age_iusage_left) = read_age(age_file_left, user, proj)
    print("User = %s" % (user))
    print("You have total aged file = %dGB" % (age_disk))    
    print("You have total aged file left = %dGB" % (age_disk_left))   	
    
    if int(age_disk_left) > int(args.target):
        print("You need to deleted aged files = %dGB" % (int(age_disk_left)-int(args.target)))			
    else:
        print("You level of aged files is satisfactory. You don't need to do anything.")    		

