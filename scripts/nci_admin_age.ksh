#!/bin/ksh
#*******************************************************************************
# nci_admin_age.ksh
# Produce aged files profile for ech user  
#*******************************************************************************
#2019 Jan 30 WenmingLu First version
#2019 Aug 28 WenmingLu For all projects
#2020 Oct 09 WenmingLu Gadi
#*******************************************************************************

module load  bom_envs/python_3.7.5 nci_admin

PROJECT_INPUT=dp9
PROJECT=${PROJECT_INPUT:-$PROJECT}

CONFIG=/g/data/${PROJECT}/admin/config/${PROJECT}.core
GDATA=/g/data/${PROJECT}/admin/report/AGE/latest_${PROJECT}_gdata_age
DEST=/g/data/${PROJECT}/admin/report/AGE
mkdir -p $DEST

while read -r line 
do  
    user=`echo $line | cut -d' ' -f1`
    echo $user
    #cat $GDATA | grep $user > $DEST/$user.gdata
    cp $DEST/$user.gdata.left  $DEST/$user.gdata.left.old
    #/projects/access/apps/nci_admin/dev/nci_admin_age.py -p dp9 -u $user
done < $CONFIG
nci_admin_age.py -p dp9
