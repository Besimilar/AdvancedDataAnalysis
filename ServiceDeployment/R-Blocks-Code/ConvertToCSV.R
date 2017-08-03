# test code
quarter <- "Q1"
year <- "2005"

# historical_data1_QY
get_data1_QY <- function(q, y) {
  quarter <- q
  year <- y
  time <- paste(quarter, year, sep = "")
  # filename <- "data/historical_data1_Q12005/historical_data1_Q12005.txt"
  filename <- paste("data/historical_data1_", time, "/historical_data1_", time, ".txt", sep = "")
  csvname <- paste("data/historical_data1_", time, "/historical_data1_", time, ".csv", sep = "")
  
  origclass <- c('integer','integer','character', 'integer', 'character', 'numeric', 'integer', 'character','numeric','integer','integer','integer','numeric','character','character','character','character', 'character','character','character','character', 'integer', 'integer','character','character','character')
  library(data.table)
  rawdata <- fread(filename, sep="|", header=FALSE, colClasses=origclass)
  rawdata <- as.data.frame(rawdata)
  names(rawdata)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv' ,'dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
  write.csv(rawdata, file = csvname, row.names = FALSE)
  return(NULL)
}

# historical_data1_time_QY
get_data1_time_QY <- function(q, y) {
  quarter <- q
  year <- y
  time <- paste(quarter, year, sep = "")
  # filename <- "data/historical_data1_Q12005/historical_data1_time_Q12005.txt"
  filename <- paste("data/historical_data1_", time, "/historical_data1_time_", time, ".txt", sep = "")
  csvname <- paste("data/historical_data1_", time, "/historical_data1_time_", time, ".csv", sep = "")
  
  svcgclass <- c('character','integer','numeric','character', 'integer','integer','character','character', 'character','integer','numeric','numeric','integer', 'integer', 'character','integer','integer', 'integer','integer','integer','integer','numeric','numeric')
  library(data.table)
  rawdata <- fread(filename, sep="|", header=FALSE, colClasses=svcgclass)
  rawdata <- as.data.frame(rawdata)
  names(rawdata)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')
  write.csv(rawdata, file = csvname, row.names = FALSE)
}

get_data1_QY("Q1", "2005")
get_data1_QY("Q2", "2005")
get_data1_time_QY("Q1", "2005")
get_data1_time_QY("Q2", "2005")


