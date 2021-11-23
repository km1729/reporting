#!/bin/ksh

#PROJECT_INPUT=$1
PROJECT_INPUT=dp9
PROJECT=${PROJECT_INPUT:-$PROJECT}
HPC=gadi

REPORT_DIR=/g/data/${PROJECT}/admin/report

YYYYMMDD=`date "+%Y%m%d"`
echo $YYYYMMDD

echo "nci-files-report -g $PROJECT -f scratch> ${REPORT_DIR}/${PROJECT}_scratch_$YYYYMMDD.rpt"
ssh $HPC nci-files-report -g $PROJECT -f scratch> ${REPORT_DIR}/${PROJECT}_scratch_$YYYYMMDD.rpt

CONVERT=/projects/access/apps/nci_admin/3.0.0/convert_report.py
ssh $HPC "module load intel-mkl/2019.3.199 python3; python3 $CONVERT ${REPORT_DIR}/${PROJECT}_scratch_$YYYYMMDD.rpt ${REPORT_DIR}/${PROJECT}_scratch_$YYYYMMDD.rpt.new"
ssh $HPC "mv ${REPORT_DIR}/${PROJECT}_scratch_$YYYYMMDD.rpt.new ${REPORT_DIR}/${PROJECT}_scratch_$YYYYMMDD.rpt"
