#!/bin/bash

# Author: Xie Jialiang
# Date: 2013-02-20
# Function: run artery to get 
#  llevel4_filtering, llevel4_assigning llevel4_info
#  from info_level1 and activity_level2
# Generate: llevel4_filtering.tmp, llevel4_assigning.tmp, llevel4_info.tmp

echo "Starting running artery"

data_dir="../../data/$1/"
echo "data dirctory: $data_dir"

echo "export_linfo_level2 > linfo_level2.tmp"
cat "$data_dir"info_level1 | python export_linfo_level2.py > "$data_dir"linfo_level2.tmp

echo "export_linfo_level2 > lcmt_level2.tmp"
cat "$data_dir"info_level1 | python export_lcmt_level2.py > "$data_dir"lcmt_level2.tmp

echo "export_llevel3 > llevel3.tmp"
python export_llevel3.py "$data_dir"linfo_level2.tmp "$data_dir"activity_level2 "$data_dir"lcmt_level2.tmp > "$data_dir"llevel3.tmp

echo "export_llevel4_filtering > llevel4_filtering"
python export_llevel4_filtering.py "$data_dir"llevel3.tmp > "$data_dir"llevel4_filtering.tmp

echo "export_llevel4_info > llevel4_info_zero"
python export_llevel4_info.py "$data_dir"llevel3.tmp > "$data_dir"llevel4_info_zero.tmp
echo "link_info_valid > llevel4_info"
python link_info_valid.py "$data_dir"llevel4_info_zero.tmp "$data_dir"activity_level2 > "$data_dir"llevel4_info.tmp

echo "export_llevel4_assigning > llevel4_assigning_zero"
python export_llevel4_assigning.py "$data_dir"llevel3.tmp "$data_dir"product_convertion > "$data_dir"llevel4_assigning_zero.tmp

echo "link_assigning_valid > llevel4_assigning"
python link_assigning_valid.py "$data_dir"llevel4_assigning_zero.tmp "$data_dir"activity_level2 > "$data_dir"llevel4_assigning.tmp

