# Map 1-based optional input ports to variables
rawdata <- maml.mapInputPort(1) # class: data.frame

# pre-processing
  # rawdata <- svcgfile_Qnyyyy
  # names(rawdata)
  # [1] "id_loan"           "svcg_cycle"        "current_upb"       "delq_sts"          "loan_age"         
  # [6] "mths_remng"        "repch_flag"        "flag_mod"          "cd_zero_bal"       "dt_zero_bal"      
  # [11] "current_int_rt"    "non_int_brng_upb"  "dt_lst_pi"         "mi_recoveries"     "net_sale_proceeds"
  # [16] "non_mi_recoveries" "expenses"          "legal_costs"       "maint_pres_costs"  "taxes_ins_costs"  
  # [21] "misc_costs"        "actual_loss"       "modcost"  
  # dim(rawdata)
  
  ## v1: Loan Sequence number
  ## remove this column
  # names(rawdata)[1]
  remove.columns <- c(1)
  # remove.columns
  
  ## v2: monthly reporting period
  ## remove this column
  # names(rawdata)[2]
  remove.columns <- c(remove.columns, 2)
  # remove.columns
  
  ## v3: current actual upb
  ## no missing values, do nothing
  # data.backup <- rawdata
  # names(rawdata)[3]
  # summary(rawdata[[3]])
  
  ## v4: current loan delinquency status
  ## if (value != 0), set to 1
  ## if (value == 0), set to 0
  # data.backup <- rawdata
  # names(rawdata)[4]
  # table(rawdata[[4]])
  rawdata[[4]][rawdata[[4]] != 0] <- 1
  # table(rawdata[[4]])
  rawdata[[4]] <- factor(rawdata[[4]],
                         levels=c(0,1),
                         labels=c("N","Y"))
  # str(rawdata[[4]])
  # table(rawdata[[4]])
  
  ## v5: loan age
  # data.backup <- rawdata
  # names(rawdata)[5]
  # summary(rawdata[[5]])
  
  ## v6: remaining months to legal maturity
  # data.backup <- rawdata
  # names(rawdata)[6]
  # summary(rawdata[[6]])
  
  ## v7: repurchase flag
  ## This field is only populated only at loan termination month
  ## set N to N
  ## set Y to Y
  ## set NA to O
  # data.backup <- rawdata
  # names(rawdata)[7]
  # table(rawdata[[7]])
  rawdata[[7]][is.na(rawdata[[7]])] <- "O"
  rawdata[[7]] <- factor(rawdata[[7]])
  # str(rawdata[[7]])
  # table(rawdata[[7]])
  
  ## v8: modification flag
  ## set NA to N
  # data.backup <- rawdata
  # names(rawdata)[8]
  # table(rawdata[[8]])
  rawdata[[8]][is.na(rawdata[[8]])] <- 0
  rawdata[[8]][rawdata[[8]] == "N"] <- 0
  rawdata[[8]][rawdata[[8]] == "Y"] <- 1
  # table(rawdata[[8]])
  rawdata[[8]] <- factor(rawdata[[8]],
                         levels=c(0,1),
                         labels=c("N","Y"))
  # summary(rawdata[[8]])
  
  ## v9: zero balance code
  ## set NA to 00
  ## 01: Prepaid or Matured
  ## 03: Foreclosure Alternative Group
  ## 06: Repurchase prior to Property Disposition
  ## 09: REO Disposition
  # data.backup <- rawdata
  # names(rawdata)[9]
  # table(rawdata[[9]])
  rawdata[[9]][is.na(rawdata[[9]])] <- "00"
  # table(rawdata[[9]])
  rawdata[[9]] <- factor(rawdata[[9]])
  # str(rawdata[[9]])
  
  ## v10: zero balance effective date
  ## remove this column
  # names(rawdata)[10]
  remove.columns <- c(remove.columns, 10)
  # remove.columns
  
  ## v11: current interest rate
  # data.backup <- rawdata
  # names(rawdata)[11]
  # summary(rawdata[[11]])
  
  ## v12: current deferred upb
  # data.backup <- rawdata
  # names(rawdata)[12]
  # summary(rawdata[[12]])
  
  ## v13: due date of last paid installment(DDLP)
  ## remove this column
  # names(rawdata)[13]
  remove.columns <- c(remove.columns, 13)
  # remove.columns
  
  ## v14: MI Recoveries
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[14]
  # summary(rawdata[[14]])
  rawdata[[14]][is.na(rawdata[[14]])] <- 0
  # summary(rawdata[[14]])
  
  ## v15: Net Sales Proceeds
  ## Set C to max
  ## set U to 0
  # data.backup <- rawdata
  # names(rawdata)[15]
  # table(rawdata[[15]])
  # sum(rawdata[[15]] == "C")
  # sum(rawdata[[15]] == "U")
  
  rawdata[[15]][is.na(rawdata[[15]])] <- 0
  rawdata[[15]][rawdata[[15]] == "U"] <- 0
  max <- max(rawdata[[15]][rawdata[[15]] != "C"])
  rawdata[[15]][rawdata[[15]] == "C"] <- max
  rawdata[[15]] <- as.numeric(rawdata[[15]])
  # summary(rawdata[[15]])
  
  ## v16: NON MI Recoveries
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[16]
  # summary(rawdata[[16]])
  rawdata[[16]][is.na(rawdata[[16]])] <- 0
  # summary(rawdata[[16]])
  
  ## v17: Expenses
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[17]
  # summary(rawdata[[17]])
  rawdata[[17]][is.na(rawdata[[17]])] <- 0
  # summary(rawdata[[17]])
  
  ## v18: Legal Costs
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[18]
  # summary(rawdata[[18]])
  rawdata[[18]][is.na(rawdata[[18]])] <- 0
  # summary(rawdata[[18]])
  
  ## v19: Maintenance and Preservation Costs
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[19]
  # summary(rawdata[[19]])
  rawdata[[19]][is.na(rawdata[[19]])] <- 0
  # summary(rawdata[[19]])
  
  ## v20: Taxes and Insurance
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[20]
  # summary(rawdata[[20]])
  rawdata[[20]][is.na(rawdata[[20]])] <- 0
  # summary(rawdata[[20]])
  
  ## v21: Miscellaneous Expenses
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[21]
  # summary(rawdata[[21]])
  rawdata[[21]][is.na(rawdata[[21]])] <- 0
  # summary(rawdata[[21]])
  
  ## v22: actual loss calculation
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[22]
  # summary(rawdata[[22]])
  rawdata[[22]][is.na(rawdata[[22]])] <- 0
  # summary(rawdata[[22]])
  
  ## v23: Modification Cost
  ## set NA to 0
  # data.backup <- rawdata
  # names(rawdata)[23]
  # summary(rawdata[[23]])
  rawdata[[23]][is.na(rawdata[[23]])] <- 0
  # summary(rawdata[[23]])
  
  
  # save necessary columns, and get clean data
  # data.backup <- rawdata
  # summary(rawdata)
  # str(rawdata)
  
  # remove.columns
  # remove #1, 2, 10, 13 colums
  cleandata <- rawdata[, -remove.columns]
  # return(cleandata)
  # str(cleandata)

# Select data.frame to be sent to the output Dataset port
maml.mapOutputPort("cleandata");