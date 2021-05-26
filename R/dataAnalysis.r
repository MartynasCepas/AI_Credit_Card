install.packages("ggpubr")
install.packages("Hmisc")
install.packages("pastecs")
install.packages("ggstatsplot")

library(pastecs)
library("ggpubr")
library(corrplot)
library(Hmisc)

# read data

data <- read.csv(file = 'data.csv', header=TRUE, stringsAsFactors = TRUE, sep = ';')
names(data)[names(data) == "ï.¿LIMIT_BAL"] <- "LIMIT_BAL"

head(data)

# correlation matrix

data_m<-cor(data)
corrplot(data_m, type = "upper", order = "hclust", tl.col = "black", tl.srt = 45)


# analysis

summary(data)
Hmisc::describe(data)
stat.desc(data)

sd(data~.)

# get means for column groups

data$PAY_MEAN <- rowMeans(subset(data, select = c(PAY_0, PAY_2, PAY_3, PAY_4, PAY_5)), na.rm = FALSE)
data$BILL_MEAN <- rowMeans(subset(data, select = c(BILL_AMT1, BILL_AMT2, BILL_AMT3, BILL_AMT4, BILL_AMT5)), na.rm = FALSE)
data$PAY_AMT_MEAN <- rowMeans(subset(data, select = c(PAY_AMT1, PAY_AMT2, PAY_AMT3, PAY_AMT4, PAY_AMT5)), na.rm = FALSE)

# fixing outliers

Q <- quantile(data$BILL_MEAN, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(data$BILL_MEAN)
data<- subset(data, data$BILL_MEAN > (Q[1] - 1.5*iqr) & data$BILL_MEAN < (Q[2]+1.5*iqr))

Q <- quantile(data$PAY_AMT_MEAN, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(data$PAY_AMT_MEAN)
data<- subset(data, data$PAY_AMT_MEAN > (Q[1] - 1.5*iqr) & data$PAY_AMT_MEAN < (Q[2]+1.5*iqr))

# modify dataset structure

data<-data[ -c(6:23)]

data <- transform(data, PAY_DIFF = BILL_MEAN - PAY_MEAN)

colnames(data)

data <- data[c("LIMIT_BAL","SEX","EDUCATION","MARRIAGE","AGE","PAY_MEAN","BILL_MEAN","PAY_AMT_MEAN","PAY_DIFF","default.payment.next.month")]

data_m<-cor(data)
corrplot(data_m, type = "full", order = "hclust", tl.col = "black", tl.srt = 45)


# dataset visualisation

plot(data$BILL_MEAN, data$PAY_AMT_MEAN, main="Bills vs Paid amount", xlab="Bill amount", ylab="Paid amount", pch=5)

# export dataset to csv

write.csv(data,"data_updated.csv", row.names = FALSE)


