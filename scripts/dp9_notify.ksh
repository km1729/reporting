#!/bin/ksh
#*******************************************************************************
# Send notice to users who overuse resources
#*******************************************************************************
#2019 Jan 30 WenmingLu First version
#2019 Aug 28 WenmingLu For all projects
#2020 Apr 01 WenmingLu Gadi
#*******************************************************************************

PROJECT_INPUT=$1
PROJECT_INPUT=dp9
PROJECT=${PROJECT_INPUT:-$PROJECT}

HPC=gadi
dp9_manager="david.lee@bom.gov.au"
dp9_su_warning="dp9_SU_WARNING"

DIR_NOTICE=/g/data/${PROJECT}/admin/notice
mkdir -p ${DIR_NOTICE}
cd ${DIR_NOTICE}
rm -rf $dp9_su_warning

YYYYMMDD=`date "+%Y%m%d"`
echo $YYYYMMDD

# create notices
echo $'\ncreating emails to users for action...'
ssh ${HPC} "module load intel-mkl/2019.3.199 python3; python3 ~access/apps/nci_admin/3.0.0/nci_admin.py -p ${PROJECT} --ymd $YYYYMMDD --report 0"
ssh ${HPC} "module load intel-mkl/2019.3.199 python3; python3 ~access/apps/nci_admin/3.0.0/nci_admin.py -p ${PROJECT} --ymd $YYYYMMDD --report 0 -c guest"
ssh ${HPC} "module load intel-mkl/2019.3.199 python3; python3 ~access/apps/nci_admin/3.0.0/nci_admin.py -p ${PROJECT} --ymd $YYYYMMDD --report 5z"
echo "creation done..."

# delete emails without the content of warnings
echo $'\ndeleting emails with no content...'
sleep 10
emails=`ls *.au *.nz`
for email in $emails; 
do 
    line=`cat $email | wc -l`
    if [[ $line -eq 3 ]]; then 
        echo $email
	rm -rf $email
    fi
done
echo "deletion done..."

# send emails
echo $'\nsending emails...'
emails=`ls *.au *.nz`
for email in $emails; 
do 
    line=`cat $email | wc -l`
    if [[ $line -gt 3 ]]; then
        echo $email
	echo "mail -s "$PROJECT disk/inode management request" $email < $email"
        mail -s "$PROJECT disk/inode management request" $email < $email
        #mail -s "$PROJECT disk/inode management request" wenming.lu@bom.gov.au < $email
    fi
done
echo "sent emails..."


echo $'\nsending SU warning...'
if [[ -f $dp9_su_warning ]]; then
    mail -s "$PROJECT SU WARNING" $dp9_manager < $dp9_su_warning
fi
echo $'\nsent SU warning...'

# archive emails
echo $'\narchiving emails...'
mkdir -p $YYYYMMDD
mv *.au $YYYYMMDD
echo "archiving done..."



