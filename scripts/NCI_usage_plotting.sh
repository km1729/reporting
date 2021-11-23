#!/usr/bin/env bash
module use ~access/modules
module load bom_envs/python_3.7.5


python /g/data/dp9/admin/script/nci_usage_plotting.py --config /g/data/dp9/admin/script/nci_usage_config.ini
