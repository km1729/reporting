#!/usr/bin/env bash

set -xv

# Location to dump the lquota call
outDir="/g/data/dp9/admin/report/"

# Create output filename
dateStr=$(date +%Y%m%d)
fout="${outDir}lquota_${dateStr}.rpt"

lquota > $fout
