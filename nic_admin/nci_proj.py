#*******************************************************************************
# Name: nci_proj.py.
#*******************************************************************************
# class for NCI project
#*******************************************************************************
# 2019 AUG 23 WenmingLu Initial version
# 2020 MAR 30 WenmingLu Gadi & Python3 version
# 2020 JUN 16 WenmingLu Adding /scratch and SU management 
#*******************************************************************************


# __class__project__ 
class project:
    # disk size unit = Gbyte
    def __init__(self, proj, gdataDiskQ, gdataInodeQ, mdssTapeQ, mdssInodeQ,\
                 gdataDiskU, gdataInodeU, mdssTapeU, mdssInodeU, \
		 scratchDiskQ, scratchDiskU, suQ=0.001, suU=0):
        self.proj        = proj
        self.gdataDiskQ  = gdataDiskQ
        self.gdataInodeQ = gdataInodeQ	
        self.mdssTapeQ   = mdssTapeQ
        self.mdssInodeQ  = mdssInodeQ
        self.gdataDiskU  = gdataDiskU
        self.gdataInodeU = gdataInodeU	
        self.mdssTapeU   = mdssTapeU
        self.mdssInodeU  = mdssInodeU
        self.scratchDiskQ  = scratchDiskQ
        self.scratchDiskU  = scratchDiskU
        self.suQ  = suQ
        self.suU  = suU
    
    # get 
    def get_proj(self):
        return self.proj
    
    def get_gdata_disk_quota(self):
        return self.gdataDiskQ

    def get_gdata_inode_quota(self):
        return self.gdataInodeQ

    def get_mdss_tape_quota(self):
        return self.mdssTapeQ

    def get_mdss_inode_quota(self):
        return self.mdssInodeQ
    
    def get_gdata_disk_usage(self):
        return self.gdataDiskU

    def get_gdata_inode_usage(self):
        return self.gdataInodeU

    def get_mdss_tape_usage(self):
        return self.mdssTapeU

    def get_mdss_inode_usage(self):
        return self.mdssInodeU

    def get_scratch_disk_quota(self):
        return self.scratchDiskQ

    def get_scratch_disk_usage(self):
        return self.scratchDiskU

    def get_su_quota(self):
        return self.suQ

    def get_su_usage(self):
        return self.suU

    # set
    def set_gdata_disk_usage(self, u):
        self.gdataDiskU = u

    def set_gdata_inode_usage(self, u):
        self.gdataInodeU = u

    def set_mdss_tape_usage(self, u):
        self.mdssTapeU = u

    def set_mdss_inode_usage(self, u):
        self.mdssInodeU = u

    def set_scratch_disk_usage(self, u):
        self.scratchDiskU = u

    def set_su_quota(self, u):
        self.suQ = u

    def set_su_usage(self, u):
        self.suU = u
 
    # get avail
    def get_gdata_disk_avail(self):
        return self.gdataDiskQ - self.gdataDiskU

    def get_gdata_inode_avail(self):
        return self.gdataInodeQ - self.gdataInodeU

    def get_mdss_tape_avail(self):
        return self.mdssTapeQ - self.mdssTapeU

    def get_mdss_inode_avail(self):
        return self.mdssInodeQ - self.mdssInodeU
    
    def get_gdata_disk_usage_in_percent(self):
        return self.gdataDiskU/self.gdataDiskQ

    def get_gdata_inode_usage_in_percent(self):
        return self.gdataInodeU/self.gdataInodeQ 

    def get_mdss_tape_usage_in_percent(self):
        return self.mdssTapeU/self.mdssTapeQ

    def get_mdss_inode_usage_in_percent(self):
        return self.mdssInodeU/self.mdssInodeQ
    
    def get_scratch_disk_avail(self):
        return self.scratchDiskQ - self.scratchDiskU
    
    def get_scratch_disk_usage_in_percent(self):
        return self.scratchDiskU/self.scratchDiskQ
    
    def get_su_avail(self):
        return self.suQ - self.suU
    
    def get_su_usage_in_percent(self):
        return self.suU/self.suQ
    
    # __str__
    def __str__(self):
        # disk in Tbyte; inode in M(illion)
        per_mdss = int(self.get_mdss_tape_usage_in_percent()*100)
        per_imdss = int(self.get_mdss_inode_usage_in_percent()*100)
        per_gdata = int(self.get_gdata_disk_usage_in_percent()*100)
        per_igdata = int(self.get_gdata_inode_usage_in_percent()*100)
        per_scratch = int(self.get_scratch_disk_usage_in_percent()*100)
        per_su = int(self.get_su_usage_in_percent()*100)
        
        content = "=== Project: %s ===" % (self.proj)
        content += "\nmassdata \tGrant=%4dT Usage=%4dT(%2d%%) Avail=%4dT iGrant=%4dM iUsage=%4dM(%2d%%) iAvail=%4dM" % \
	           (self.mdssTapeQ, self.mdssTapeU, per_mdss, self.mdssTapeQ-self.mdssTapeU, \
		   self.mdssInodeQ, self.mdssInodeU, per_imdss, self.mdssInodeQ-self.mdssInodeU)

        content += "\ngdata1a  \tGrant=%4dT Usage=%4dT(%2d%%) Avail=%4dT iGrant=%4dM iUsage=%4dM(%2d%%) iAvail=%4dM" % \
	           (self.gdataDiskQ, self.gdataDiskU, per_gdata, (self.gdataDiskQ-self.gdataDiskU), \
		    self.gdataInodeQ, self.gdataInodeU, per_igdata, (self.gdataInodeQ-self.gdataInodeU))
        
        content += "\nscratch  \tGrant=%4dT Usage=%4dT(%2d%%) Avail=%4dT" % \
                   (self.scratchDiskQ, self.scratchDiskU, per_scratch, (self.scratchDiskQ-self.scratchDiskU))
        
        content += "\nSU \t\tGrant=%2dMSU Usage=%2.1fMSU(%2d%%) Avail=%2.1fMSU" % \
                   (self.suQ, self.suU, per_su, (self.suQ-self.suU))

        return content
	
    
def main():
    new_proj = project("dp9", 220, 45, 1700, 82.1, 200, 35, 1100, 10, 800, 330) 
    print(new_proj)
    print()
    print(new_proj.get_proj()) 
    print(new_proj.get_gdata_disk_quota())
    print(new_proj.get_gdata_inode_quota())
    print(new_proj.get_gdata_disk_usage())
    print(new_proj.get_gdata_inode_usage())
    print(new_proj.get_gdata_disk_avail())
    print(new_proj.get_gdata_inode_avail())
    print(new_proj.get_gdata_disk_usage_in_percent())
    print(new_proj.get_gdata_inode_usage_in_percent())
    print(new_proj.get_mdss_tape_quota())
    print(new_proj.get_mdss_inode_quota())
    print(new_proj.get_mdss_tape_usage())
    print(new_proj.get_mdss_inode_usage())
    print(new_proj.get_mdss_tape_avail())
    print(new_proj.get_mdss_inode_avail())
    print(new_proj.get_mdss_tape_usage_in_percent())
    print(new_proj.get_mdss_inode_usage_in_percent())
    print()
    new_proj.set_gdata_disk_usage(210)
    new_proj.set_gdata_inode_usage(38)
    new_proj.set_mdss_tape_usage(1200)
    new_proj.set_mdss_inode_usage(15)
    new_proj.set_su_quota(12)
    new_proj.set_su_usage(5)
    print(new_proj)
    
    
if __name__ == "__main__":
    main()

