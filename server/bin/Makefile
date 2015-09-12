
artery = artery/
capillary = capillary/
data = ../data/$(com)/

final = $(data)llevel5_filtering $(data)llevel5_info $(data)llevel5_assigning

llevel5 : $(final)
llevel4 : $(data)llevel4_filtering.tmp $(data)llevel4_info.tmp $(data)llevel4_assigning.tmp
llevel3 : $(data)llevel3.tmp

login_birthday : $(data)login_birthday

cleantmp :
	rm -f $(data)*.tmp

datafiles = $(data)namelist_self_triager $(data)login_role $(data)login_experience $(data)login_general_experience \
	    $(data)login_peer_info $(data)login_ncomment $(data)product_information $(data)login_information $(data)login_product_information  
cleandata :
	rm -f $(datafiles)

cleanfinal :
	rm -f $(final)

clean : cleantmp cleandata cleanfinal
	


# artery stage 1

ifeq ($(skipone),true)
else
$(data)linfo_level2.tmp : $(artery)export_linfo_level2.py $(data)info_level1 
	cat $(data)info_level1 | $(artery)export_linfo_level2.py > $@	
$(data)lcmt_level2.tmp : $(artery)export_lcmt_level2.py $(data)info_level1 
	cat $(data)info_level1 | $(artery)export_lcmt_level2.py > $@
endif

$(data)lactivity_level2.tmp : $(artery)uniform_activity_field_name.py $(data)activity_level2
	$+ > $@

$(data)llevel3.tmp : $(artery)export_llevel3.py $(data)linfo_level2.tmp $(data)lactivity_level2.tmp $(data)lcmt_level2.tmp
	$+ > $@



# fork here
# filtering
$(data)llevel4_filtering_zero.tmp : $(artery)export_llevel4_filtering.py $(data)llevel3.tmp
	$+ > $@

$(data)llevel4_filtering_correct.tmp : $(artery)link_info_correct.py $(data)llevel4_filtering_zero.tmp
	$+ > $@

$(data)llevel4_filtering.tmp : $(artery)link_valid.py $(data)llevel4_filtering_correct.tmp $(data)lactivity_level2.tmp $(data)llevel3.tmp
	$+ 2 > $@
# info
$(data)llevel4_info_zero.tmp : $(artery)export_llevel4_info.py $(data)llevel3.tmp
	$+ > $@

$(data)llevel4_info_correct.tmp : $(artery)link_info_correct.py $(data)llevel4_info_zero.tmp
	$+ > $@

$(data)llevel4_info.tmp : $(artery)link_valid.py $(data)llevel4_info_correct.tmp $(data)lactivity_level2.tmp $(data)llevel3.tmp
	$+ 1 > $@
# assigning
$(data)llevel4_assigning_zero.tmp : $(artery)export_llevel4_assigning.py $(data)llevel3.tmp $(data)product_convertion
	$+ > $@

$(data)llevel4_assigning_correct.tmp : $(artery)link_assigning_correct.py $(data)llevel4_assigning_zero.tmp $(data)product_convertion
	$+ > $@

$(data)llevel4_assigning.tmp : $(artery)link_valid.py $(data)llevel4_assigning_correct.tmp $(data)lactivity_level2.tmp $(data)llevel3.tmp
	$+ 0 > $@

# end of artery stage 1

# capillary
$(data)namelist_non_self_triager : $(capillary)export_non_self_triage_actor.py $(data)linfo_level2.tmp $(data)lactivity_level2.tmp
	$+ > $@

ifeq ($(com),mozilla)
not_use_email = 0
else
not_use_email = 1
endif

ifeq ($(com),mozillaNew)
not_use_email = 0
endif

ifeq ($(com),openoffice)
not_use_email = 0
endif

$(data)login_role : $(capillary)export_login_role.py $(data)namelist_developer $(data)namelist_non_self_triager $(data)namelist_maintainer $(data)lactivity_level2.tmp
	$+ $(not_use_email) > $@

$(data)login_experience : $(capillary)export_login_experience.py $(data)llevel4_filtering.tmp $(data)llevel4_assigning.tmp $(data)llevel4_info.tmp $(data)llevel3.tmp $(data)product_convertion
	$+ > $@

$(data)login_general_experience : $(capillary)export_login_general_experience.py $(data)lactivity_level2.tmp
	$+ > $@

$(data)login_peer_info : $(capillary)export_login_peer_info.py $(data)lcmt_level2.tmp $(data)login_general_experience
	$+ > $@

$(data)login_ncomment : $(capillary)export_login_ncomment.py $(data)lcmt_level2.tmp
	$+ > $@

$(data)product_information_assi : $(capillary)export_product_information.py $(data)llevel4_assigning.tmp $(data)product_convertion
	$+ 0 new > $@

$(data)product_information_info : $(capillary)export_product_information.py $(data)llevel4_info.tmp $(data)product_convertion
	$+ 1 tt_prod > $@

$(data)product_information_filt : $(capillary)export_product_information.py $(data)llevel4_filtering.tmp $(data)product_convertion
	$+ 2 tt_prod > $@

#$(data)login_information : $(capillary)export_login_information.py $(data)llevel4_assigning.tmp $(data)product_convertion $(data)llevel3.tmp
#	$(capillary)export_login_information.py $(data)llevel4_assigning.tmp $(data)product_convertion $(data)llevel3.tmp > $(data)login_information

$(data)login_product_information_assi : $(capillary)export_login_product_information.py $(data)llevel4_assigning.tmp $(data)product_convertion
	$+ 0 new > $@

$(data)login_product_information_info : $(capillary)export_login_product_information.py $(data)llevel4_info.tmp $(data)product_convertion
	$+ 1 tt_prod > $@

$(data)login_product_information_filt : $(capillary)export_login_product_information.py $(data)llevel4_filtering.tmp $(data)product_convertion
	$+ 2 tt_prod > $@

$(data)login_birthday : $(capillary)export_login_birthday.py $(data)login_role
	$+ > $@

# end of capillary

# artery stage 2
# link role
$(data)llevel4_info_login_role.tmp : $(artery)link_login_role.py $(data)llevel4_info.tmp $(data)login_role
	$+ login when tri > $@

$(data)llevel4_filtering_login_role.tmp : $(artery)link_login_role.py $(data)llevel4_filtering.tmp $(data)login_role
	$+ login when tri > $@

$(data)llevel4_assigning_login_role.tmp : $(artery)link_login_role.py $(data)llevel4_assigning.tmp $(data)login_role
	$+ login when tri > $@

# link peer info
$(data)llevel4_info_login_peer_info.tmp : $(artery)link_login_peer_info.py $(data)llevel4_info_login_role.tmp $(data)login_peer_info
	$+ > $@

$(data)llevel4_assigning_login_peer_info.tmp : $(artery)link_login_peer_info.py $(data)llevel4_assigning_login_role.tmp $(data)login_peer_info
	$+ > $@

$(data)llevel4_filtering_login_peer_info.tmp : $(artery)link_login_peer_info.py $(data)llevel4_filtering_login_role.tmp $(data)login_peer_info
	$+ > $@

# link comment
$(data)llevel4_info_login_ncomment.tmp : $(artery)link_login_ncomment.py $(data)llevel4_info_login_peer_info.tmp $(data)login_ncomment
	$+ > $@

$(data)llevel4_assigning_login_ncomment.tmp : $(artery)link_login_ncomment.py $(data)llevel4_assigning_login_peer_info.tmp $(data)login_ncomment
	$+ > $@

$(data)llevel4_filtering_login_ncomment.tmp : $(artery)link_login_ncomment.py $(data)llevel4_filtering_login_peer_info.tmp $(data)login_ncomment
	$+ > $@

# link product information
$(data)llevel4_info_product_information.tmp : $(artery)link_product_information.py $(data)llevel4_info_login_ncomment.tmp $(data)product_information_info $(data)product_convertion
	$+ tt_prod > $@

$(data)llevel4_assigning_product_information.tmp : $(artery)link_product_information.py $(data)llevel4_assigning_login_ncomment.tmp $(data)product_information_assi $(data)product_convertion
	$+ new > $@

$(data)llevel4_filtering_product_information.tmp : $(artery)link_product_information.py $(data)llevel4_filtering_login_ncomment.tmp $(data)product_information_filt $(data)product_convertion
	$+ tt_prod > $@

# link login product information
$(data)llevel5_info : $(artery)link_login_product_information.py $(data)llevel4_info_product_information.tmp $(data)login_product_information_info $(data)product_convertion
	$+ tt_prod > $@

$(data)llevel5_assigning : $(artery)link_login_product_information.py $(data)llevel4_assigning_product_information.tmp $(data)login_product_information_assi $(data)product_convertion
	$+ new > $@

$(data)llevel5_filtering : $(artery)link_login_product_information.py $(data)llevel4_filtering_product_information.tmp $(data)login_product_information_filt $(data)product_convertion
	$+ tt_prod > $@

# end of artery stage 2

