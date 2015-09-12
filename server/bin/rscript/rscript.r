read_assigning <- function(file){
	act_assi <- read.table(file, sep=";", quote="", header=T, comment.char="")
	act_assi$valid <- as.logical(act_assi$valid_t >= 0)
	act_assi$correct <- as.logical(act_assi$correct)
	act_assi
}

get_sub_assi <- function(act_assi, from_year, to_year){
	#%act_assi[act_assi$field == "product" & act_assi$tri_role=="triager" & act_assi$valid & toyear(act_assi$when)>=from_year & toyear(act_assi$when)<=to_year,]
	act_assi[act_assi$field == "product" & act_assi$valid & toyear(act_assi$when)>=from_year & toyear(act_assi$when)<=to_year,]
}

get_sub_mod <- function(act, from_year, to_year){
	act[toyear(act$when)>=from_year & toyear(act$when)<to_year,]
}

get_sub_cor <- function(act, from_year, to_year){
	act[toyear(act$when)>=from_year & toyear(act$when)<to_year & act$valid,]
}

get_impact <- function(act, con){
	a <- data.frame(length(unique(act$bug_id[con & act$tri_role=="triager"])), length(unique(act$bug_id[con & act$tri_role=="dev"])), length(unique(act$bug_id[con & act$tri_role=="maint"])), length(unique(act$bug_id[con & act$tri_role=="self"])),length(unique(act$bug_id[con])))
	names(a) <- c("triager","dev","maint","reporter" ,"total")
	a
}


calculate_metrics <- function(act_assi){
	act_assi$PErr <- 1.0 - act_assi$nPrdCorTri/(act_assi$nPrdTri+1)
	act_assi$TrPErr <- 1.0 - act_assi$nLogPrdCorTri/(act_assi$nLogPrdTri+1)

	act_assi$Role <- act_assi$tri_role	
	act_assi$MaxSNExp <- act_assi$cnt_max_exp
	act_assi$SNSize <- act_assi$cnt_num
	act_assi$AvgSNDep <- act_assi$cmt_num / (act_assi$cnt_num + 1)
	act_assi$P <- as.factor(act_assi$new)

	act_assi
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


toyear <- function(second){
	second / 3600.0 / 24.0 / 365.25 + 1970
}

pnr <- function(con1, con2){
	tmp <- table(con1, con2)
	tmp <- data.frame(tmp[2,2]/(tmp[2,2]+tmp[1,2]), tmp[2,2]/(tmp[2,2]+tmp[2,1]), tmp[2,1]/(tmp[2,1]+tmp[2,2]), tmp[1,2]/(tmp[1,1]+tmp[1,2]))
	names(tmp) <- c("precision","recall","type-1","type-2")
	tmp
}

prepare_data <- function(filtering, info, assigning, begin_year, end_year){
	tdata <- list()
        
	# read filtering
	"Loading filtering observations"
	act_fil <- read.table(filtering, sep=";", quote="", header=T, comment.char="")
	act_fil$correct <- (act_fil$new == act_fil$final)
	tdata$mod_fil <- get_sub_mod(act_fil, begin_year, end_year)
	tdata$cor_fil <- tdata$mod_fil
	
	# read info
	"Loading filling information observations"
	act_info <- read.table(info, sep=";", quote="", header=T, comment.char="")
	act_info$old <- as.character(act_info$old)
	act_info$new <- as.character(act_info$new)
	act_info$valid <- as.logical(act_info$valid)
	act_info$correct <- (act_info$new == act_info$final)
	tdata$mod_info <- get_sub_mod(act_info, begin_year, end_year)
	tdata$cor_info <- get_sub_cor(act_info, begin_year, end_year)

	# read assigning
	"Loading product assigning observations"
	act_assi <- read_assigning(assigning)
	act_assi$old <- as.character(act_assi$old)
	act_assi$new <- as.character(act_assi$new)
	tdata$act_assi <- act_assi
	tdata$mod_assi <- get_sub_mod(act_assi, begin_year, end_year)
	tdata$cor_assi <- get_sub_cor(act_assi, begin_year, end_year)

	tdata
}

show_triage_practice <- function(tdata){
	total_issue <- length(unique(union(union(tdata$mod_fil$bug_id, tdata$mod_info$bug_id), tdata$mod_assi$bug_id)))
	severity <- length(unique(tdata$mod_info$bug_id[tdata$mod_info$field == "severity" & tdata$mod_info$old != tdata$mod_info$new]))
	priority <- length(unique(tdata$mod_info$bug_id[tdata$mod_info$field == "priority" & tdata$mod_info$old != tdata$mod_info$new]))
	version <- length(unique(tdata$mod_info$bug_id[tdata$mod_info$field == "version" & tdata$mod_info$old != tdata$mod_info$new]))
	os <- length(unique(tdata$mod_info$bug_id[tdata$mod_info$field == "os" & tdata$mod_info$old != tdata$mod_info$new]))
	assi <- length(unique(tdata$mod_assi$bug_id[tdata$mod_assi$field == "product" & tdata$mod_assi$old != tdata$mod_assi$new]))
	modlist <- data.frame(number=c(severity, priority, version, os, assi, total_issue), ratio=c(severity, priority, version, os, assi, total_issue)/total_issue)
	row.names(modlist) <- c("severity", "priority", "version", "os", "product assigning", "total")
	
	modlist
}

get_one_impact_for_roles <-function(act, roles, con){
	impacts <- list()
	for(role in roles){
		impacts[role] <- length(unique(act$bug_id[con & act$tri_role == role]))
	}
	impacts
}

get_tot_impact_for_roles <- function(actFilter, actInfo, actAssi, roles){
	impacts <- list()
	for(role in roles){
		modFilter <- unique(actFilter$bug_id[actFilter$tri_role == role])
		modInfo <- unique(actInfo$bug_id[actInfo$tri_role == role])
		modAssi <- unique(actAssi$bug_id[actAssi$tri_role == role])
		impacts[role] <- length(unique(union(modFilter,union(modInfo,modAssi))))
	}
	impacts
}

get_triager_notriager_modification <- function(actFilter, actInfo, actAssi){
	filTriager <- unique(actFilter$bug_id[actFilter$tri_role == "triager"])
	infoTriager <- unique(actInfo$bug_id[actInfo$tri_role == "triager"])
	assiTriager <- unique(actAssi$bug_id[actAssi$tri_role == "triager"])
	
	filNonTriager <- unique(actFilter$bug_id[actFilter$tri_role != "triager"])
	infoNonTriager <- unique(actInfo$bug_id[actInfo$tri_role != "triager"])
	assiNonTriager <- unique(actAssi$bug_id[actAssi$tri_role != "triager"])

	res <- list()
	res["Triager"] <- length(unique(union(filTriager, union(infoTriager,assiTriager))))
	res["NonTriager"] <- length(unique(union(filNonTriager, union(infoNonTriager,assiNonTriager)))) 
	res
}

show_triage_impact_number <- function(tdata){
	total_issue <- length(unique(union(union(tdata$mod_fil$bug_id, tdata$mod_info$bug_id), tdata$mod_assi$bug_id)))
	roles = c("triager","dev","maint","self")
	show_roles = c("triager","dev","maint","reporter")

	reject <- get_one_impact_for_roles(tdata$mod_fil, roles, tdata$mod_fil$new == "reject")
	confirm <- get_one_impact_for_roles(tdata$mod_fil, roles, tdata$mod_fil$new == "confirm")

	severity <- get_one_impact_for_roles(tdata$mod_info, roles, tdata$mod_info$field == "severity")
	priority <- get_one_impact_for_roles(tdata$mod_info, roles, tdata$mod_info$field == "priority")
	version <- get_one_impact_for_roles(tdata$mod_info, roles, tdata$mod_info$field == "version")
	os <- get_one_impact_for_roles(tdata$mod_info, roles, tdata$mod_info$field == "os")
	
	product <- get_one_impact_for_roles(tdata$mod_assi, roles, tdata$mod_assi$field == "product")

	tot <- get_tot_impact_for_roles(tdata$mod_fil, tdata$mod_info, tdata$mod_assi, roles)

	impact_number <- data.frame(rbind(reject, confirm, severity, priority, version, os, product, tot))
	names(impact_number) <- paste(show_roles,"num",sep="_")
	impact_number$triager_num <- as.numeric(impact_number$triager_num) 
	impact_number$triager_ratio <- impact_number$triager_num/total_issue

	impact_number
}

show_triage_mistaken_confirm <- function(tdata){
	final_reso <- table(tdata$cor_fil$final_reso[tdata$cor_fil$new=="confirm" & tdata$cor_fil$correct==F & tdata$cor_fil$tri_role=="triager" & tdata$cor_fil$final_reso!=""])
	total <- sum(final_reso)
	final_reso <- data.frame(final_reso)
	names(final_reso) <- c("Final Resolution", "Number")
	final_reso$ratio <- round(final_reso$Number/total,2)

	final_reso
}

get_one_quality_for_roles <- function(act, roles, con){
	quality <- list()
	
	for(role in roles){
		tmp <- table(act$correct[act$tri_role == role & con])
		quality[paste(role,"#cor",sep="_")] <- tmp[2]
		quality[paste(role,"#inc",sep="_")] <- tmp[1]
		quality[paste(role,"#rat",sep="_")] <- tmp[2]/sum(tmp)
	}
	
	quality
}

show_triage_impact_quality <- function(tdata){
	roles = c("triager","dev")
	
	reject <- get_one_quality_for_roles(tdata$cor_fil, roles, tdata$cor_fil$new == "reject")
	confirm <- get_one_quality_for_roles(tdata$cor_fil, roles, tdata$cor_fil$new == "confirm")

	severity <- get_one_quality_for_roles(tdata$cor_info, roles, tdata$cor_info$field == "severity")
	priority <- get_one_quality_for_roles(tdata$cor_info, roles, tdata$cor_info$field == "priority")
	version <- get_one_quality_for_roles(tdata$cor_info, roles, tdata$cor_info$field == "version")
	os <- get_one_quality_for_roles(tdata$cor_info, roles, tdata$cor_info$field == "os")

	product <- get_one_quality_for_roles(tdata$cor_assi, roles, tdata$cor_assi$field == "product")

	impact_quality <- data.frame(rbind(reject, confirm, severity, priority, version, os, product))
	row.names(impact_quality) <- c("reject", "confirm", "severity", "priority", "version", "os", "product")

	title <- c()
	for(role in roles){
		title <- c(title, rep(role,3))
	}
	names(impact_quality) <- paste(title, rep(c("#cor", "#inc", "#rat"), length(roles)),sep="_")
	
	impact_quality	
}

show_assigning_model <- function(tdata, begin_year=2001, end_year=2009){
	model_assi <- list()
	fac_assi <- calculate_metrics(get_sub_assi(tdata$act_assi, begin_year, end_year))
	model_assi$correlation <- round(cor(fac_assi[,c("correct","SNSize", "AvgSNDep","PErr","TrPErr","MaxSNExp")], method="spearman"),2)
	
	glm_assi <- glm(correct~PErr+TrPErr+log(SNSize+1)+log(MaxSNExp+1)+Role+log(AvgSNDep+1)+P, data=fac_assi, family=binomial)
	anova_assi <- anova(glm_assi)
	model_assi$explain_deviance <- sum(anova_assi[-1,2])/anova_assi[1,4]
	
	summary_assi <- summary(glm_assi)$coefficients[1:10,c(1,4)]
	ExpDev <- anova_assi[c(1:5,6,6,6,7:8),2]
	model_assi$summary <- cbind(summary_assi, ExpDev)
	
	model_assi
}

get_prf <- function(ttable){
	precision = ttable[2,2]/(ttable[2,1]+ttable[2,2])
	recall = ttable[2,2]/(ttable[1,2]+ttable[2,2])
	f1score = (2*precision*recall)/(precision+recall)
	
	c(precision, recall, f1score)
}

show_predict <- function(tdata, learn_begin_year=2008, learn_end_year=2009, test_begin_year=2009, test_end_year=2010){
	learn_set <- calculate_metrics(get_sub_assi(tdata$act_assi, learn_begin_year, learn_end_year))
	glm_learn <- glm(I(correct)~I(PErr)+I(TrPErr)+I(log(MaxSNExp+1))+I(log(SNSize+1))+Role+I(log(AvgSNDep+1))+I(P), data=learn_set, family=binomial)
	
	test_set <- calculate_metrics(get_sub_assi(tdata$act_assi, test_begin_year, test_end_year))
	oldP <- names(table(as.character(learn_set$P)))
	newP <- names(table(as.character(test_set$P)))
	remP <- newP[is.na(match(newP,oldP))]
	test_set <- test_set[is.na(match(test_set$P,remP)),]
	prd <- predict(glm_learn, test_set)
	test_set$prd <- exp(prd)/(1+exp(prd))

    write.table(test_set, file="predictedIssues.res", sep=";", row.names=F, append=T)

	prediction <- list()
	prediction$ProbabilityQuantile <- round(quantile(test_set$prd,0:10/10),2)
	
    redlist <- c(sum(!test_set$correct)/length(test_set$correct), NA, NA)
	for(quan in seq(.05, .95, by=.05)){
        redtable <- table(test_set$prd<=quantile(test_set$prd, quan), !test_set$correct)
        redpr <- get_prf(redtable)
        redlist <- rbind(redlist, redpr)
    }
    redframe <- data.frame(redlist)
    names(redframe) <- c("Precision", "Recall", "F1Score")
    row.names(redframe) <- cbind("Random", t(seq(.05, .95, by=.05)))[1,]
    prediction$Warning_PRF <- redframe

    greenlist <- c(sum(test_set$correct)/length(test_set$correct), NA, NA)
	for(quan in seq(.05, .95, by=.05)){
        greentable <- table(test_set$prd>=quantile(test_set$prd, quan), test_set$correct)
        greenpr <- get_prf(greentable)
        greenlist <- rbind(greenlist, greenpr)
    }
    greenframe <- data.frame(greenlist)
    names(greenframe) <- c("Precision", "Recall", "F1Score")
    row.names(greenframe) <- cbind("Random", t(seq(.05, .95, by=.05)))[1,]
    prediction$Recommended_PRF <- greenframe
	
	prediction
}

run <- function(community, data_dir = "../../data/"){
	dir <- paste(data_dir, community, sep="")
	begin_year <- 2001
	end_year <- 2010
	if(community == "mozilla"){
		end_year <- 2010
	}
    if(community == "mozillaNew"){
        end_year <- 2012
    }
	if(community == "gnome"){
		end_year <- 2011
	}
	tdata <- prepare_data(paste(dir, "llevel5_filtering",sep="/"), paste(dir, "llevel5_info",sep="/"), paste(dir, "llevel5_assigning",sep="/"), begin_year, end_year)
	
	info <- list()
	info$TriagePractice <- show_triage_practice(tdata)
	info$TriagerImpactByNumber <- show_triage_impact_number(tdata)
	info$TriagerImpactByQuality <- show_triage_impact_quality(tdata)
	info$TriageMistakenConfirm <- show_triage_mistaken_confirm(tdata)

	if(community == "mozilla" | community == "openoffice"){
		info$TriagerAssigningModel <- show_assigning_model(tdata, 2001, 2009)
		info$TriagerAssigningPrediction <- show_predict(tdata, 2008, 2009, 2009, 2010)
	}
	if(community == "mozillaNew"){
		info$TriagerAssigningModel <- show_assigning_model(tdata, 2001, 2011)
		#info$TriagerAssigningPrediction <- show_predict(tdata, 2010, 2011, 2011, 2012)
	 
        sink("rPredict.res") 
        yres <- show_predict(tdata, 2001, 2002, 2002, 2003)
        RecommendPRF <- yres$Recommended_PRF
        WarningPRF <- yres$Warning_PRF
        print(yres) 

        for(year in 2002:2010){
            ylearn <- year
            ytest <- year+1
            yres <- show_predict(tdata, ylearn, ylearn+1, ytest, ytest+1)
            RecommendPRF <- RecommendPRF + yres$Recommended_PRF
            WarningPRF <- WarningPRF + yres$Warning_PRF
            print(yres)
        }
        sink()

        RecommendPRF <- RecommendPRF/(2010-2001+1)
        WarningPRF <- WarningPRF/(2010-2001+1)
        info$RecommendPRF <- RecommendPRF
        info$WarningPRF <- WarningPRF
    }
	if(community == "gnome"){
		info$TriagerAssigningModel <- show_assigning_model(tdata, 2001, 2009)
		info$TriagerAssigningPrediction <- show_predict(tdata, 2008, 2009, 2009, 2010)
	}
	
	info
}

show_roles <- function(tdata){
	
nTriageActor <- length(unique(union(union(tdata$mod_fil$login,tdata$mod_info$login),tdata$mod_assi$login)))
TriagerLogins <- (unique(union(union(tdata$mod_fil$login[tdata$mod_fil$tri_role=="triager"],tdata$mod_info$login[tdata$mod_info$tri_role=="triager"]),tdata$mod_assi$login[tdata$mod_assi$tri_role=="triager"])))
nTriager <- length(TriagerLogins) 
ReporterLogins <- (unique(union(union(tdata$mod_fil$login[tdata$mod_fil$tri_role=="self"],tdata$mod_info$login[tdata$mod_info$tri_role=="self"]),tdata$mod_assi$login[tdata$mod_assi$tri_role=="self"])))
nReporter <- length(ReporterLogins)
DeveloperLogins <- (unique(union(union(tdata$mod_fil$login[tdata$mod_fil$tri_role=="dev"],tdata$mod_info$login[tdata$mod_info$tri_role=="dev"]),tdata$mod_assi$login[tdata$mod_assi$tri_role=="dev"])))
nDeveloper <- length(DeveloperLogins)
nMaintainer <- length(unique(union(union(tdata$mod_fil$login[tdata$mod_fil$tri_role=="maint"],tdata$mod_info$login[tdata$mod_info$tri_role=="maint"]),tdata$mod_assi$login[tdata$mod_assi$tri_role=="maint"])))
nTriager2Developer <- length(unique(intersect(TriagerLogins, DeveloperLogins)))
nReporter2Developer <- length(unique(intersect(ReporterLogins, DeveloperLogins)))

nTriageActorIssues <- length(unique(union(union(tdata$mod_fil$bug_id,tdata$mod_info$bug_id),tdata$mod_assi$bug_id)))
nTriagerIssues <- length(unique(union(union(tdata$mod_fil$bug_id[tdata$mod_fil$tri_role=="triager"],tdata$mod_info$bug_id[tdata$mod_info$tri_role=="triager"]),tdata$mod_assi$bug_id[tdata$mod_assi$tri_role=="triager"])))
nReporterIssues <- length(unique(union(union(tdata$mod_fil$bug_id[tdata$mod_fil$tri_role=="self"],tdata$mod_info$bug_id[tdata$mod_info$tri_role=="self"]),tdata$mod_assi$bug_id[tdata$mod_assi$tri_role=="self"])))
nDeveloperIssues <- length(unique(union(union(tdata$mod_fil$bug_id[tdata$mod_fil$tri_role=="dev"],tdata$mod_info$bug_id[tdata$mod_info$tri_role=="dev"]),tdata$mod_assi$bug_id[tdata$mod_assi$tri_role=="dev"])))
nMaintainerIssues <- length(unique(union(union(tdata$mod_fil$bug_id[tdata$mod_fil$tri_role=="maint"],tdata$mod_info$bug_id[tdata$mod_info$tri_role=="maint"]),tdata$mod_assi$bug_id[tdata$mod_assi$tri_role=="maint"])))

	out <- data.frame(TriageActor=c(nTriageActor,nTriageActorIssues,nTriageActorIssues/nTriageActor),Triager=c(nTriager,nTriagerIssues,nTriagerIssues/nTriager),Developer=c(nDeveloper,nDeveloperIssues,nDeveloperIssues/nDeveloper),Maintainer=c(nMaintainer,nMaintainerIssues,nMaintainerIssues/nMaintainer),Reporter=c(nReporter,nReporterIssues,nReporterIssues/nReporter), Triager2Developer=c(nTriager2Developer, 0,0), Reporter2Developer=c(nReporter2Developer, 0, 0))
	row.names(out) <- c("Login","Issue","Issue/Login")
	out
}

show_issues_story <- function(tdata){

nReported <- length(unique(tdata$cor_fil$bug_id))
rejectedIssues <- unique(tdata$cor_fil$bug_id[tdata$cor_fil$new=="reject" & tdata$cor_fil$final=="reject"])
rejConIssues <- unique(tdata$cor_fil$bug_id[tdata$cor_fil$new=="reject" & tdata$cor_fil$final=="confirm"])
confirmedIssues <- unique(tdata$cor_fil$bug_id[tdata$cor_fil$new=="confirm" & tdata$cor_fil$final=="confirm"])
conRejIssues <- unique(tdata$cor_fil$bug_id[tdata$cor_fil$new=="confirm" & tdata$cor_fil$final=="reject"])

out <- data.frame(nReported, length(rejectedIssues), length(rejConIssues), length(confirmedIssues), length(conRejIssues),
       length(intersect(rejectedIssues, conRejIssues)), length(intersect(confirmedIssues, rejConIssues)))
names(out)<- c("Rep Issues","RejRej Issues","RejCon Issues","ConCon Issues","ConRej Issues","CRRej Issues","RCCon Issues")
out
}

# the function may cause segment fault by far
show_triage_by_age <- function(tdata, nl){
	stop("this function may cause segment fault by far.")
	names(nl)[2] <- "birth"
	resn <- list()
	tbs <- c("cor_fil", "cor_info", "cor_assi")
	for(tb in tbs){
		fk <- tdata[tb]
		lt <- merge(fk, nl, x.by=login, y.by=login)
		lt$age <- lt$when - lt$birth
		tmp <- table(lt$correct[lt$age/3600/24/365.25 < 3 & lt$valid_t >= 0])
		tmpl <- list()
		tmpl$cor <- tmp[2]
		tmpl$tot <- tmp[1] + tmp[2]
		tmpl$rat <- tmp[2] / (tmp[1] + tmp[2])
		resn[tb]$all_lt3 <- tmpl
	}
	resn
}
