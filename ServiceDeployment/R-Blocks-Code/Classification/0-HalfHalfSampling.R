# Map 1-based optional input ports to variables
rawdata <- maml.mapInputPort(1) # class: data.frame

# half-half dataset
negative.data <- rawdata[rawdata$delq_sts != 0, ]
positive.data <- rawdata[rawdata$delq_sts == 0, ]

# sampling
smp_size <- nrow(negative.data)
set.seed(21)
index <- sample(1:nrow(positive.data), size = smp_size)
positive.data <- positive.data[index, ]
rawdata <- rbind(negative.data, positive.data)
rawdata <- rawdata[sample(nrow(rawdata)), ]

table(rawdata$delq_sts)

# Select data.frame to be sent to the output Dataset port
maml.mapOutputPort("rawdata");