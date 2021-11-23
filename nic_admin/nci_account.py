#!/opt/nci/nciaccount/venv/bin/python3 -I

import argparse
import json
import math
import os
import pymunge
import requests
import sys
import urllib

parser = argparse.ArgumentParser()
parser.add_argument("-P", "--project", help="project to view")
parser.add_argument("-p", "--period", help="accounting period to view")
parser.add_argument("-v", "--verbose", help="verbose report", action='store_true')
parser.add_argument("--no-pretty-print", help=argparse.SUPPRESS, action='store_true')
args = parser.parse_args()

# Get project
if args.project:
    project = args.project
else:
    if 'PROJECT' in os.environ:
        project = os.environ['PROJECT']
    else:
        print("Please specify --project PROJECT with the project you'd like to view")
        sys.exit(1)

if args.period:
    period = args.period
else:
    period = None

if args.verbose:
    verbose = True
else:
    verbose = False

if args.no_pretty_print:
    pretty_print = not args.no_pretty_print
else:
    pretty_print = True


SERVER='http://gadi-pbs-01.gadi.nci.org.au:8811/'

url = SERVER + 'project/%s' % project
token = pymunge.encode().decode('utf-8')

payload = dict()

if period is not None:
    payload['period'] = period

headers = { 'Authorization': "MUNGE %s" % (token) }

try:
    response = requests.get(url, params=payload, headers=headers, timeout=180.0)
    res = response.json()
except:
    print("Could not retrieve response from server. Server may be offline or overloaded, please try again later.")
    sys.exit(1)

if res['status'] != 200:
    print(res['message'])
    sys.exit(1)

#print(res)

def format_su(su_val):
    if not pretty_print:
        return '%.2f SU' % su_val
    
    units = ['SU ', 'KSU', 'MSU', 'GSU', 'TSU', 'PSU']
    
    if su_val <= 1000.0:
        i = 0
    else:
        i = int(math.floor(math.log(su_val, 1000)))
    p = math.pow(1000, i)
    s = round(su_val/p, 2)
    return '%.2f %s' % (s, units[i])

def format_size(size_val, suffix='B'):
    if not pretty_print:
        return '%s  B' % size_val
    for unit in [' ','K','M','G','T','P','E','Z']:
        if abs(size_val) < 1024.0:
            return "%3.2f %s%s" % (size_val, unit, suffix)
        size_val /= 1024.0
    return "%.1f %s%s" % (size_val, 'Y', suffix)

def format_si_num(size_val, suffix='B'):
    if not pretty_print:
        return '%s' % size_val
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(size_val) < 1000.0:
            return "%3.2f %s%s" % (size_val, unit, suffix)
        size_val /= 1000.0
    return "%.2f %s%s" % (size_val, 'Y', suffix)

if res['usage'] is not False:
    total_su = format_su(res['usage']['total_grant'])
    running_jobs_su = format_su(res['usage']['running_job_reserved'])
    used_su = format_su(res['usage']['used'])
    free_su = format_su(res['usage']['total_grant'] - res['usage']['running_job_reserved'] - res['usage']['used'])
    period = res['usage']['period']
    
    
    #### Summary Report for Project
    summary_report = f"""
Usage Report: Project={project} Period={period}
=============================================================
    Grant: {total_su:>12}
     Used: {used_su:>12}
 Reserved: {running_jobs_su:>12}
    Avail: {free_su:>12}
    """
    print(summary_report)
    
    #### Verbose Requested
    #### Provides per-stakeholder usage information
    if verbose:
        stakeholder_header = f"""\
Stakeholder                   Grant         Used        Avail
-------------------------------------------------------------\
    """
        print(stakeholder_header)
    
        for stakeholder in res['usage']['stakeholders'].keys():
            stakeholder_info = res['usage']['stakeholders'][stakeholder]
                    
            stakeholder_total_su = format_su(stakeholder_info['grant'])
            stakeholder_used_su = format_su(stakeholder_info['grant'] - stakeholder_info['balance'])
            stakeholder_free_su = format_su(stakeholder_info['balance'])
            stakeholder_report = f"""\
{stakeholder:<22} {stakeholder_total_su:>12} {stakeholder_used_su:>12} {stakeholder_free_su:>12}\
    """
            print(stakeholder_report)
    
        stakeholder_footer = f"""\
------------------------------------------------------------- 
    """
        print(stakeholder_footer)
        
        
    #### And the per-user usage information
        if len(res['usage']['users']) > 0:
            users_header = f"""\
User                                        Used     Reserved
-------------------------------------------------------------\
        """
            print(users_header)
    
            for user in res['usage']['users'].keys():
                user_info = res['usage']['users'][user]
                    
                user_used_su = format_su(user_info['usage'])
                user_reserved_su = format_su(user_info['acquired'])
                user_report = f"""\
{user:<36} {user_used_su:>12} {user_reserved_su:>12}\
        """
                print(user_report)
    
            users_footer = f"""\
-------------------------------------------------------------\
        """
            print(users_footer)
            
#### Storage Summary
if len(res['storage'].keys()) > 0:
    storage_summary_report = f"""
Storage Usage Report: Project={project}
=============================================================
Filesystem        Used     iUsed    Allocation    iAllocation\
    """
    print(storage_summary_report)
    
    for filesystem in res['storage'].keys():
        filesystem_usage = res['storage'][filesystem]
        
        if filesystem.startswith('global-'):
            filesystem_name = filesystem[7:]
        else:
            filesystem_name = filesystem
        filesystem_used = format_size(filesystem_usage['block_usage'])
        filesystem_inodes_used = format_si_num(filesystem_usage['inode_usage'], suffix='')
        
        # Add up the allocations for summary
        filesystem_allocation = 0
        filesystem_inode_allocation = 0
        
        for allocation in filesystem_usage['allocations']:
            filesystem_allocation = filesystem_allocation + allocation['block_allocation']
            filesystem_inode_allocation = filesystem_inode_allocation + allocation['inode_allocation']
        
        filesystem_allocation = format_size(filesystem_allocation)
        filesystem_inode_allocation = format_si_num(filesystem_inode_allocation, suffix='')
        
        filesystem_report = f"""\
{filesystem_name:<11} {filesystem_used:>10} {filesystem_inodes_used:>9} {filesystem_allocation:>13} {filesystem_inode_allocation:>14}\
        """
        
        print(filesystem_report)
        
        if verbose:
            filesystem_stakeholder_header = f"""
Stakeholder                         Allocation    iAllocation
-------------------------------------------------------------\
            """
            print(filesystem_stakeholder_header)
            
            for allocation in filesystem_usage['allocations']:
                stakeholder_name = allocation['funding_source']
                stakeholder_allocation = format_size(allocation['block_allocation'])
                stakeholder_inode_allocation = format_si_num(allocation['inode_allocation'], suffix='')
                
                filesystem_stakeholder_allocation_report = f"""\
{stakeholder_name:<32} {stakeholder_allocation:>13} {stakeholder_inode_allocation:>14}\
                """
                print(filesystem_stakeholder_allocation_report)
                
            filesystem_stakeholder_footer = f"""\
-------------------------------------------------------------
            """
            print(filesystem_stakeholder_footer)
    if not verbose:
        filesystem_summary_footer = f"""\
=============================================================
        """
        print(filesystem_summary_footer)
        
