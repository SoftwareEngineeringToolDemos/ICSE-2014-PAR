#!/bin/bash

# Author: Xie Jialiang
# Date: 2013-2-20
# Function: run artery to get 
#  llevel5_filtering, llevel5_assigning llevel5_info
#  from artery_stage1
# Generate: llevel5_filtering, llevel5_assigning llevel5_info
# Demand: Capillary data should be ready before artery run

echo "Starting running artery stage 2"
data_dir="../../data/$1/"

echo "enter filtering thread"
echo "link_login_role > llevel5_filtering"
python link_login_role.py "$data_dir"llevel4_filtering.tmp "$data_dir"login_role login when tri  > "$data_dir"llevel5_filtering

echo "filtering thread accomplished"

echo "enter info thread"
echo "link_login_role > llevel5_info"
python link_login_role.py "$data_dir"llevel4_info.tmp "$data_dir"login_role login when tri > "$data_dir"llevel5_info

echo "info thread accomplished"

echo "enter assigning thread"
echo "link_assigning correct > llevel4_assigning_correct.tmp"
python link_assigning_correct.py "$data_dir"llevel4_assigning.tmp "$data_dir"product_convertion > "$data_dir"llevel4_assigning_correct.tmp

echo "link_login_role > llevel4_assigning_login_role.tmp"
python link_login_role.py "$data_dir"llevel4_assigning_correct.tmp "$data_dir"login_role login when tri > "$data_dir"llevel4_assigning_login_role.tmp

echo "link_login_experience > llevel4_assigning_login_experience.tmp"
python link_login_experience.py "$data_dir"llevel4_assigning_login_role.tmp "$data_dir"login_experience "$data_dir"product_convertion > "$data_dir"llevel4_assigning_login_experience.tmp

echo "link_login_peer_info > llevel4_assigning_login_peer_info.tmp"
python link_login_peer_info.py "$data_dir"llevel4_assigning_login_experience.tmp "$data_dir"login_peer_info > "$data_dir"llevel4_assigning_login_peer_info.tmp

echo "link_login_ncomment > llevel4_assigning_login_ncomment.tmp"
python link_login_ncomment.py "$data_dir"llevel4_assigning_login_peer_info.tmp "$data_dir"login_ncomment > "$data_dir"llevel4_assigning_login_ncomment.tmp

echo "link_product_information > llevel4_assigning_product_information.tmp"
python link_product_information.py "$data_dir"llevel4_assigning_login_ncomment.tmp "$data_dir"product_information "$data_dir"product_convertion > "$data_dir"llevel4_assigning_product_information.tmp

echo "link_login_information > llevel4_assigning_login_information.tmp"
python link_login_information.py "$data_dir"llevel4_assigning_product_information.tmp "$data_dir"login_information "$data_dir"product_convertion > "$data_dir"llevel4_assigning_login_information.tmp

echo "link_login_product_information > llevel4_assigning_login_product_information.tmp"
python link_login_product_information.py "$data_dir"llevel4_assigning_login_information.tmp "$data_dir"login_product_information "$data_dir"product_convertion > "$data_dir"llevel5_assigning
