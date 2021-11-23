# This config is directly imported by python code nci_admin_dp9.py
# Please make sure every line is python valid statement
# configuration for dp9 mdss, /short, /g/data disk and inode usage
# /scratch on gadi, equivalent of /short on raijin, is managed since June 2020.

file_core  = "dp9.core"
file_guest = "dp9.guest"
path_notice = "/g/data/dp9/admin/notice/"
path_report = "/g/data/dp9/admin/report/"
path_config = "/g/data/dp9/admin/config/"
#report_mdss is decided dynamically from June 2020
#report_mdss = "/g/data/dp9/admin/report/latest_mdss.rpt"
path_age    = "/g/data/dp9/admin/report/AGE/"
su_warning = "dp9_SU_WARNING"

quota_mdss     = 2000   		#TB
quota_imdss    = 82.1   		#Million
quota_gdata    = 220    		#TB
quota_igdata   = 45     		#Million
quota_scratch  = 1200    		#TB

top_user_index = 10

limit_igdata   = 0.15
limit_gdata    = 0.15
limit_mdss     = 0.10
limit_scratch  = 0.20
warning_mdss   = 0.90
warning_imdss  = 0.85
warning_gdata  = 0.85
warning_igdata = 0.85
warning_scratch= 0.90
warning_mdss_disk = 50			#TB
warning_gdata_disk = 5			#Million
warning_gdata_inode = 2			#TB
warning_scratch_disk = 200		#TB

warning_mdss_disk_guest = 10.0	   	#TB
warning_gdata_disk_guest = 500     	#GB
warning_gdata_inode_guest = 1	   	#Million
warning_scratch_disk_guest = 5000  	#GB

