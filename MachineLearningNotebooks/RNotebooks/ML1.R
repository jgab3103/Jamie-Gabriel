# libraries
library(dplyr)
library(ggplot2)
library(caret)
library(vip)
library(rsample)
library(h2o)
library(AmesHousing)
set.seed(123)
library(modeldata)
library(visdat)


## ISSUES IN SAMPLING 
# Get data 
data("attrition", package = "modeldata")
ames <- AmesHousing::make_ames()
ames.h2o <- as.h2o(ames)


# Tidy data 
churn <- attrition %>% 
  mutate_if(is.ordered, .funs = factor, ordered = FALSE)
churn.h2o <- as.h2o(churn)


# Base data split
index1 <- sample(1:nrow(ames), round(nrow(ames) * .7))
train1 <- ames[index_1,]
test1 <- ames[-index_1,]

# Caret data split
index2 <- caret::createDataPartition(ames$Sale_Price, p = 0.7,
                                     list = FALSE)
train2 <- ames[index2,]
test2 <- ames[-index2, ]

# Stratified sampling 
table(churn$Attrition)

splitStrat <- rsample::initial_split(churn, prop = 0.7,
                                     strata = "Attrition")
trainStrat <- rsample::training(splitStrat)
testStrat <- rsample::testing(splitStrat)

table(testStrat$Attrition) %>% prop.table()

# redressing class imbalance 
# Down sampling, reducing size in abundant classes to match frequencies 
# in least prev class, Up sampling is opposite



### MODELS 

bootstraps(ames, times = 10)


# Bias
# how wrong we are in general to predcitions
# high variance = how much overfitting 

# Accuracy - how often correct
# Precision - how often preduct events - trued positive to false postive ratio



cv <- trainControl(
  method = "repeatedcv", 
  number = 10, 
  repeats = 5
)

# Create grid of hyperparameter values
hyper_grid <- expand.grid(k = seq(2, 25, by = 1))

# Tune a knn model using grid search
knn_fit <- train(
  Sale_Price ~ ., 
  data = train2, 
  method = "knn", 
  trControl = cv, 
  tuneGrid = hyper_grid,
  metric = "RMSE"
)

ggplot(knn_fit)



################ FEATURE AND TARGET ENG #############

# Observe: linear regression assumes predictions are normally distributed 

# fixing positvely skewed target variables 
