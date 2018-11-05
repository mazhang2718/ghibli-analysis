# Script 2: This script takes in the .csv files and adds a column for the time gap between each subtitle

setwd("~/Desktop/ghibli/r-analysis/csv")

devtools::install_github("fkeck/subtools", force=TRUE)
install.packages("tidytext")
install.packages("dplyr")
install.packages("readr")
library(subtools)
library(tidytext)
library(dplyr)
library(readr)

subsCSV <- read.csv(fileName, stringsAsFactors = F)
  head(subsCSV, 5)

subsLag <- mutate(subsCSV, fromNext=lag(toSeconds)) %>% 
    mutate(silenceSeconds=fromSeconds-fromNext) %>% 
    select(textString, startTime, endTime, fromSeconds, toSeconds, timeLength, fromNext, silenceSeconds)

head(subsLag, 100)
  
write_csv(subsLag, fileName, na="NA")