#*******************************************************************************
# Name: nci_user.py.
#*******************************************************************************
# class for NCI project
#*******************************************************************************
# 2019 AUG 26 WenmingLu Initial version revised from nci_admin_dp9.py
# 2020 MAR 30 WenmingLu Gadi & Python3 version
# 2020 APR 30 WenmingLu Guest user
# 2020 JUN 16 WenmingLu /scratch and SU management
#*******************************************************************************

from nci_admin_config import *
from nci_proj import *

# __class__user__ 
class user:
    def __init__(self, proj, name=None, login=None, email=None):
        # User info
        self.proj = proj
        self.login = login
        self.email = email
        self.name = name
	
        # Usage by the user
        self.ugdata = 0
        self.igdata = 0
        self.umdss = 0
        self.imdss = 0
        self.ugdata_projs = []
        self.uscratch = 0
        self.su = 0
	
	# Email yes or no
        self.notify = False

    def get_proj(self):
        return self.proj 
    
    def get_name(self):
        return self.name 
    
    def get_email(self):
        return self.email 

    def get_notify(self):
        return self.notify
    
    def get_login(self):
        return self.login    
    
    def get_ugdata(self):
        return self.ugdata
    
    def get_igdata(self):
        return self.igdata
    
    def get_umdss(self):
        return self.umdss
    
    def get_imdss(self):
        return self.imdss

    def get_uscratch(self):
        return self.uscratch

    def get_su(self):
        return self.su
    
    def set_umdss(self, umdss):
        self.umdss = umdss
        if self.umdss > self.proj.get_mdss_tape_quota()*limit_mdss*pow(1024, 4):
            self.notify = True
    
    def set_imdss(self, imdss):
        self.imdss = imdss
        if self.imdss > self.proj.get_mdss_inode_quota()*limit_mdss*pow(10, 6):
            self.notify = True        
     
    def set_su(self, su):
        self.su = su
   
    def add_ugdata(self, ugdata):
        self.ugdata += ugdata  
        if self.ugdata > self.proj.get_gdata_disk_quota()*limit_gdata*pow(1024, 4):
            self.notify = True 

    def add_igdata(self, igdata):
        self.igdata += igdata    
        if self.igdata > self.proj.get_gdata_inode_quota()*limit_gdata*pow(10, 6):
            self.notify = True 

    def add_ugdata_projs(self, proj):
        if proj != self.proj:
            self.ugdata_projs.append(proj)
            self.notify = True

    def add_uscratch(self, uscratch):
        self.uscratch += uscratch  
	
    def __str__(self):
        # disk in Gbyte; inode in M(illion)
        ugdata = self.ugdata/pow(1024, 3)
        igdata = self.igdata/pow(10, 6)
        umdss  = self.umdss/pow(1024, 3)
        imdss  = self.imdss/pow(10, 6)
        uscratch = self.uscratch/pow(1024, 3)
	
        content = "\n"
        content += self.name+"\n"
        content += self.email+"\n"
        content += self.login+"\n\n"
        content += self.get_proj().get_proj()+"\n"
	
        content += "/g/data/ usage  = %7dG  share = %2.2f%%\n" % \
	            (ugdata, 100*(ugdata/1024.0)/self.proj.get_gdata_disk_quota())
        content += "/g/data/ iUsage = %7dM  share = %2.2f%%\n" % \
	            (igdata, 100*igdata/self.proj.get_gdata_inode_quota())
        content += "mdss     usage  = %7dG  share = %2.2f%%\n" % \
	            (umdss, 100*(umdss/1024)/self.proj.get_mdss_tape_quota())
        content += "/scratch usage  = %7dG  share = %2.2f%%\n" % \
	            (uscratch, 100*(uscratch/1024.0)/self.proj.get_scratch_disk_quota())
        content += "Service Unit usage  = %.2fKSU\n" % \
	            (self.su/1000)
        return content

    def get_user_message(self):
        content = ""
        content += self.email+"\n"
        content += self.login+"\n\n"
        
        proj = self.proj.get_proj()
        umdss = self.umdss*1.0/pow(1024, 4)
        ugdata = self.ugdata*1.0/pow(1024, 4)
        igdata = self.igdata*1.0/pow(10, 6)
        gdata_disk_percentile = self.proj.get_gdata_disk_usage_in_percent()
        gdata_inode_percentile = self.proj.get_gdata_inode_usage_in_percent()
        mdss_tape_percentile = self.proj.get_mdss_tape_usage_in_percent()
        mdss_tape_limit = limit_mdss*self.proj.get_mdss_tape_quota()
        gdata_inode_limit = limit_igdata*self.proj.get_gdata_inode_quota()
        gdata_disk_limit = limit_gdata*self.proj.get_gdata_disk_quota()
        uscratch = self.uscratch*1.0/pow(1024, 4)
        scratch_disk_percentile = self.proj.get_scratch_disk_usage_in_percent()
        scratch_disk_limit = limit_scratch*self.proj.get_scratch_disk_quota()
 
        if umdss > mdss_tape_limit:	
            content += "Your "+ proj +" mdss usage = %.2fT\n" % (umdss)
            content += "Please reduce your /mdss/"+proj+" below "+str(mdss_tape_limit)+"T\n\n"
        else:		        
            if mdss_tape_percentile > warning_mdss:
                if umdss > warning_mdss_disk:
                    content += "Your "+ proj +" mdss usage = %.2fT\n" % (umdss)                
                    content += "Total "+ proj +" mdss usage at %.1f%%\n" % (mdss_tape_percentile*100)
                    content += "Your personal mdss share is %.1f%%\n" % (100*umdss/self.proj.get_mdss_tape_quota())              
                    content += "Please reduce your /mdss/"+proj+" usage\n\n"       
        
        if ugdata > gdata_disk_limit:	
            content += "Your "+ proj +" /g/data usage = %.2fT\n" % (ugdata)
            content += "Please reduce your /g/data/"+proj+" below "+str(gdata_disk_limit)+"T\n\n"
        else:		        
            if gdata_disk_percentile > warning_gdata:
                if ugdata > warning_gdata_disk:
                    content += "Your /g/data/"+ proj +" usage = %.2fT\n" % (ugdata)                
                    content += "Total /g/data/"+ proj +" usage at %.1f%%\n" % (gdata_disk_percentile*100)
                    content += "Your personal /g/data disk share is %.1f%%\n" % (100*ugdata/self.proj.get_gdata_disk_quota())               
                    content += "Please reduce your /g/data/"+proj+" usage\n\n"        
                
                if len(self.ugdata_projs) > 0:
                    try:
                        self.ugdata_projs.remove(self.proj.get_proj()) 
                    except:
                        None
                if len(self.ugdata_projs)>0:
                    content += "Please clean up your files on other gdata disk(s)\n"		
                    for p in self.ugdata_projs:
                        content += "/g/data/%s\n" % (p)		        
                    content += "\n"
		    	
        if igdata > gdata_inode_limit:	
            content += "Your "+ proj +" /g/data iUsage = %.2fM\n" % (igdata)
            content += "Please reduce your inodes of /g/data/"+proj+" below "+str(gdata_inode_limit)+"M\n\n"
        else:		        
            if gdata_inode_percentile > warning_gdata:
                if igdata > warning_gdata_inode:
                    content += "Your /g/data/"+ proj +" iUsage = %.2fM\n" % (igdata)                
                    content += "Total /g/data/"+ proj +" iUsage at %.1f%%\n" % (gdata_inode_percentile*100)
                    content += "Your personal /g/data inode share is %.1f%%\n" % (100*igdata/self.proj.get_gdata_inode_quota())              
                    content += "Please reduce your /g/data/"+proj+" iUsage\n\n"            

        if uscratch > scratch_disk_limit:	
            content += "Your "+ proj +" /scratch usage = %.2fT\n" % (uscratch)
            content += "Please reduce your /scratch/"+proj+" below "+str(scratch_disk_limit)+"T\n\n"
        else:		        
            if scratch_disk_percentile > warning_scratch:
                if uscratch > warning_scratch_disk:
                    content += "Your /scratch/"+ proj +" usage = %.2fT\n" % (uscratch)                
                    content += "Total /scratch/"+ proj +" usage at %.1f%%\n" % (scratch_disk_percentile*100)
                    content += "Your personal /scratch disk share is %.1f%%\n" % (100*uscratch/self.proj.get_scratch_disk_quota())               
                    content += "Please reduce your /scratch/"+proj+" usage\n\n"        

        return content

    def get_guest_message(self):
        content = ""
        content += self.email+"\n"
        content += self.login+"\n\n"
        
        proj = self.proj.get_proj()
        umdss = self.umdss*1.0/pow(1024, 4)
        ugdata = self.ugdata*1.0/pow(1024, 3)
        igdata = self.igdata*1.0/pow(10, 6)
        uscratch = self.uscratch*1.0/pow(1024, 3)
        
        if umdss > warning_mdss_disk_guest:
            content += "Your "+ proj +" mdss usage = %.2fT\n" % (umdss)                
            content += "Please reduce your /mdss/"+proj+" usage below "+str(warning_mdss_disk_guest)+"T\n\n"       
        
        if ugdata > warning_gdata_disk_guest:
            content += "Your /g/data/"+ proj +" usage = %.2fG\n" % (ugdata)                
            content += "Please reduce your /g/data/"+proj+" usage below "+str(warning_gdata_disk_guest)+"G\n\n"        
                
        if len(self.ugdata_projs) > 0:
            try:
                self.ugdata_projs.remove(self.proj.get_proj()) 
            except:
                None
        if len(self.ugdata_projs)>0:
            content += "Please clean up your files on other gdata disk(s)\n"		
            for p in self.ugdata_projs:
                content += "/g/data/%s\n" % (p)		        

        if igdata > warning_gdata_inode_guest:
            content += "Your /g/data/"+ proj +" iUsage = %.2fM\n" % (igdata)                
            content += "Please reduce your /g/data/"+proj+" iUsage below "+str(warning_gdata_inode_guest)+"M\n\n"            

        if uscratch > warning_scratch_disk_guest:
            content += "Your /scratch/"+ proj +" usage = %.2fG\n" % (ugdata)                
            content += "Please reduce your /scratch/"+proj+" usage below "+str(warning_scratch_disk_guest)+"G\n\n"        

        return content
    

def main():
    new_proj = project("dp9", 220, 45, 1700, 82.1, 210, 40, 1600, 80, 800, 730) 
    new_user = user(new_proj, "Wenming Lu", "wml548", "wenming.lu@bom.gov.au") 
    
    print(new_user)  
    print()
    print(new_user.get_proj()) 
    print(new_user.get_name())
    print(new_user.get_login()) 
    print(new_user.get_email())
    print(new_user.get_notify())
    print()
    new_user.set_umdss(78962757582201)
    new_user.set_imdss(3000001)
    new_user.set_su(3000001)
    new_user.add_ugdata(2178962757581)
    new_user.add_igdata(12897231)
    new_user.add_uscratch(241789627575810)
    print(new_user.get_ugdata())
    print(new_user.get_igdata())
    print(new_user.get_umdss())
    print(new_user.get_imdss()) 
    print(new_user.get_notify())
    print(new_user.get_uscratch()) 
    print("="*20)
    print(new_user)  
    print("="*20)
    print(new_user.get_user_message())
    print("="*20)
    print(new_user.get_guest_message())
   
    
if __name__ == "__main__":
    main()    

