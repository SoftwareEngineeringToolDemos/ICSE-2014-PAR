#!/bin/bash

# Author: Xie Jialiang
# Date: 2013-02-20
# Function: generate data for artery

echo "Starting capillary"
data_dir="../../data/$1/"

echo "generating login_role"
echo "export_self_triage_actor"
python export_self_triage_actor.py "$data_dir"linfo_level2.tmp "$data_dir"activity_level2 > "$data_dir"namelist_self_triager

echo "export_login_role"

email_or_only=0
if [ "$1"x = "gnome"x ]; then
	email_or_only=1
	echo "use not email"
fi
python export_login_role.py "$data_dir"namelist_developer "$data_dir"namelist_self_triager "$data_dir"namelist_maintainer "$data_dir"activity_level2 "$email_or_only" > "$data_dir"login_role

echo "generation login_experience"
python export_login_experience.py "$data_dir"llevel4_filtering.tmp "$data_dir"llevel4_assigning.tmp "$data_dir"llevel4_info.tmp "$data_dir"llevel3.tmp "$data_dir"product_convertion > "$data_dir"login_experience

echo "generate login_general_experience"
python export_login_general_experience.py "$data_dir"activity_level2 > "$data_dir"login_general_experience

echo "generate login_peer_info"
python export_login_peer_info.py "$data_dir"lcmt_level2.tmp "$data_dir"login_general_experience > "$data_dir"login_peer_info

echo "generate login_ncomment"
python export_login_ncomment.py "$data_dir"lcmt_level2.tmp > "$data_dir"login_ncomment

echo "generate product_information"
python export_product_information.py "$data_dir"llevel4_assigning.tmp "$data_dir"product_convertion "$data_dir"llevel3.tmp > "$data_dir"product_information

echo "generate login_information"
python export_login_information.py "$data_dir"llevel4_assigning.tmp "$data_dir"product_convertion "$data_dir"llevel3.tmp > "$data_dir"login_information

echo "generate login_product_information"
python export_login_product_information.py "$data_dir"llevel4_assigning.tmp "$data_dir"product_convertion "$data_dir"llevel3.tmp > "$data_dir"login_product_information
