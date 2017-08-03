# Map 1-based optional input ports to variables
rawdata <- maml.mapInputPort(1) # class: data.frame

# Change column type
rawdata[[1]] <- as.character(rawdata[[1]])
rawdata[[2]] <- as.integer(rawdata[[2]])
rawdata[[3]] <- as.numeric(rawdata[[3]])
rawdata[[4]] <- as.character(rawdata[[4]])
rawdata[[5]] <- as.integer(rawdata[[5]])
rawdata[[6]] <- as.integer(rawdata[[6]])
rawdata[[7]] <- as.character(rawdata[[7]])
rawdata[[8]] <- as.character(rawdata[[8]])
rawdata[[9]] <- as.character(rawdata[[9]])
rawdata[[10]] <- as.integer(rawdata[[10]])
rawdata[[11]] <- as.numeric(rawdata[[11]])
rawdata[[12]] <- as.numeric(rawdata[[12]])
rawdata[[13]] <- as.integer(rawdata[[13]])
rawdata[[14]] <- as.integer(rawdata[[14]])
rawdata[[15]] <- as.character(rawdata[[15]])
rawdata[[16]] <- as.integer(rawdata[[16]])
rawdata[[17]] <- as.integer(rawdata[[17]])
rawdata[[18]] <- as.integer(rawdata[[18]])
rawdata[[19]] <- as.integer(rawdata[[19]])
rawdata[[20]] <- as.integer(rawdata[[20]])
rawdata[[21]] <- as.integer(rawdata[[21]])
rawdata[[22]] <- as.numeric(rawdata[[22]])
rawdata[[23]] <- as.numeric(rawdata[[23]])

# Select data.frame to be sent to the output Dataset port
maml.mapOutputPort("rawdata");