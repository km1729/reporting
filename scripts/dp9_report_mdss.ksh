#!/bin/ksh

#PROJECT_INPUT=$1
PROJECT_INPUT=dp9
PROJECT=${PROJECT_INPUT:-$PROJECT}
HPC=gadi

REPORT_DIR=/g/data/${PROJECT}/admin/report

YYYYMMDD=`date "+%Y%m%d"`
echo $YYYYMMDD

echo "mdss get dp9_MASSDATA_USAGE> ${REPORT_DIR}/${PROJECT}_mdss_$YYYYMMDD.rpt"
ssh $HPC mdss get dp9_MASSDATA_USAGE ${REPORT_DIR}/${PROJECT}_mdss_$YYYYMMDD.rpt

