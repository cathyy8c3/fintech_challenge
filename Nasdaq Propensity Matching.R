

# Install packages 
install.packages("MatchIt")  
install.packages("AER")  

# Clear existing data
rm(list=ls())
# Load dataset
Fintech = read.csv("Nasdaq.csv", stringsAsFactors =FALSE)




# Build a Linear Regression model
LinearRegModel = lm(songsListened ~ age + friend_cnt + lovedTracks + posts + playlists + 
                      shouts, data = Fintech)

# summary of the results of the model
summary(LinearRegModel)

# Logistic Model
LogisticModel = glm(adopter ~ tenure + good_country + songsListened + male + friend_cnt + shouts + 
                      posts + playlists, data = Fintech, family = binomial)

# View a summary of the results of the model
summary(LogisticModel)

# Calculate the Odds Ratio for each independent variable.
exp(coef(LogisticModel))


###############################
## Propensity Score Matching ##
###############################

# For now, setting all NA values to 0 (because propensity score matching won't work with 
# missing values)
write.csv(Fintech,"data.csv",na="0")
Fintech=read.csv("data.csv")

# Load package for propensity score matching
library(MatchIt)

# For demonstrative purposes, I'm running my analysis on a sample of 10,000 observations
# from the dataset, since propensity matching takes a while (10 mins) on the overall dataset
mysample <- Fintech[sample(1:nrow(Fintech), 10000, replace=FALSE),]

# R Function for propensity score matching
# 1 to 1 match (because ratio = 1); can change to ratio = 2 for 1 to 2 match 
matchprocess = matchit(adopter ~ lovedTracks + posts + playlists + shouts + tenure,
                data = mysample, method = "nearest", ratio = 1)

# View summary statistics on 'treatment'/'control' groups, before and after matching
# See how the mean difference between the 2 groups decreases significantly after matching
summary(matchprocess)

# Export the matched observations to a new dataframe
matchdata<- match.data(matchprocess) 

# See how this new 'matched' dataset now has half adopters and half non adopters
table(matchdata$adopter)
View(matchdata)


# Load package for instrumental variables
library(AER)

# Simultaneity bias between playlists and songs listened.
regmodel <- lm(playlists ~ songsListened + age, data = Fintech)
summary(regmodel)

# Assume you have determined that lovedTracks is a good instrumental variable for 
# songs listened. Then you can redo the regression as follows:
ivmodel<- ivreg(playlists ~ age + songsListened | age + lovedTracks, data = Fintech)
summary(ivmodel)

