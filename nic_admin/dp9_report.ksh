#!/bin/ksh

#PROJECT_INPUT=$1
PROJECT_INPUT=dp9
PROJECT=${PROJECT_INPUT:-$PROJECT}
HPC=gadi

REPORT_DIR=/g/data/${PROJECT}/admin/report

YYYYMMDD=`date "+%Y%m%d"`
echo $YYYYMMDD

echo "nci_account -P $PROJECT -vv > ${REPORT_DIR}/${PROJECT}_${YYYYMMDD}.rpt"
ssh $HPC nci_account -P $PROJECT -vv > ${REPORT_DIR}/${PROJECT}_${YYYYMMDD}.rpt
