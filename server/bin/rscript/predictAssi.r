read_assigning <- function(file){
	act_assi <- read.table(file, sep=";", quote="", header=T, comment.char="")
	act_assi$valid <- as.logical(act_assi$valid_t >= 0)
	act_assi$correct <- as.logical(act_assi$correct)
	act_assi
}

toyear <- function(second){
	second / 3600.0 / 24.0 / 365.25 + 1970
}

get_sub_assi <- function(act_assi, from_year, to_year){
	act_assi[act_assi$field == "product" & act_assi$valid & toyear(act_assi$when)>=from_year & toyear(act_assi$when)<=to_year,]
}

calculate_metrics_apply_prediction <- function(act_assi){
	act_assi$PErr <- 1.0 - act_assi$nPrdCorTri/(act_assi$nPrdTri+1)
	act_assi$TrPErr <- 1.0 - act_assi$nLogPrdCorTri/(act_assi$nLogPrdTri+1)

	act_assi$Role <- act_assi$tri_role	
	act_assi$MaxSNExp <- act_assi$cnt_max_exp
	act_assi$SNSize <- act_assi$cnt_num
	act_assi$AvgSNDep <- act_assi$cmt_num / (act_assi$cnt_num + 1)
	act_assi$P <- as.factor(act_assi$new)
	
	act_assi
}

predict_from_file <- function(file, modelFile){
	act_assi <- read.table(file, sep=";", header=T)
	
	predict_share(modelFile, act_assi)
}

predict_from_input <- function(modelFile, nPrdCorTri, nPrdTri, nLogPrdCorTri, nLogPrdTri, cnt_max_exp, cnt_num, cmt_num, tri_role, new){
	act_assi <- data.frame(nPrdCorTri, nPrdTri, nLogPrdCorTri, nLogPrdTri, cnt_max_exp, cnt_num, cmt_num, new, tri_role)
	
	predict_share(modelFile, act_assi)
}

predict_share <- function(modelFile, act_assi){
	act_assi <- calculate_metrics_apply_prediction(act_assi)
	load(modelFile)
	prd <- predict(glm_assi, act_assi)
	prd <- exp(prd)/(1+exp(prd))

	prd
}

set_threshold <- function(modelFile, low, high){

	load(modelFile)
	prd <- predict(glm_assi)
	prd <- exp(prd)/(1+exp(prd))

	out <- quantile(prd,c(low,high))
	names(out) <- c(low, high)
	out
}

generate_model <- function(learn_file, mod_file,begin_year, end_year){
	read_file <- read_assigning(learn_file)
	sub_assi <- get_sub_assi(read_file, begin_year, end_year)
	sub_assi <- calculate_metrics_apply_prediction(sub_assi)
	
	glm_assi <- glm(correct~PErr+TrPErr+log(SNSize+1)+log(MaxSNExp+1)+Role+log(AvgSNDep+1)+P, data=sub_assi, family=binomial)

	rm(read_file)
	rm(sub_assi)
	save(glm_assi, file=mod_file)
}
