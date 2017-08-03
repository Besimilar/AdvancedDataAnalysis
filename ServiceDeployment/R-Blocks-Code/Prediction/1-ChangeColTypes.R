# Map 1-based optional input ports to variables
rawdata <- maml.mapInputPort(1) # class: data.frame

# Change column type
rawdata[[1]] <- as.integer(rawdata[[1]])
rawdata[[2]] <- as.integer(rawdata[[2]])
rawdata[[3]] <- as.character(rawdata[[3]])
rawdata[[4]] <- as.integer(rawdata[[4]])
rawdata[[5]] <- as.character(rawdata[[5]])
rawdata[[6]] <- as.numeric(rawdata[[6]])
rawdata[[7]] <- as.integer(rawdata[[7]])
rawdata[[8]] <- as.character(rawdata[[8]])
rawdata[[9]] <- as.numeric(rawdata[[9]])
rawdata[[10]] <- as.integer(rawdata[[10]])
rawdata[[11]] <- as.integer(rawdata[[11]])
rawdata[[12]] <- as.integer(rawdata[[12]])
rawdata[[13]] <- as.numeric(rawdata[[13]])
rawdata[[14]] <- as.character(rawdata[[14]])
rawdata[[15]] <- as.character(rawdata[[15]])
rawdata[[16]] <- as.character(rawdata[[16]])
rawdata[[17]] <- as.character(rawdata[[17]])
rawdata[[18]] <- as.character(rawdata[[18]])
rawdata[[19]] <- as.character(rawdata[[19]])
rawdata[[20]] <- as.character(rawdata[[20]])
rawdata[[21]] <- as.character(rawdata[[21]])
rawdata[[22]] <- as.integer(rawdata[[22]])
rawdata[[23]] <- as.integer(rawdata[[23]])
rawdata[[24]] <- as.character(rawdata[[24]])
rawdata[[25]] <- as.character(rawdata[[25]])
rawdata[[26]] <- as.character(rawdata[[26]])

# Select data.frame to be sent to the output Dataset port
maml.mapOutputPort("rawdata");