# First try: http://www.pieceofk.fr/?p=437

setwd("~/Desktop/ghibli")

devtools::install_github("fkeck/subtools", force=TRUE)
install.packages("tidytext")
install.packages("dplyr")
install.packages("readr")
library(subtools)
library(tidytext)
library(dplyr)
library(readr)

subs <- read.subtitles("srt-raw/yesterday2-raw.srt")
subsSent <- sentencify(subs)
write.subtitles(subsSent, "srt-edit/yesterday2-edit.srt") #just spits out the same text but with the subtitles joined as sentences

lines <- readLines("srt-edit/yesterday2-edit.srt")
listOfEntries <- 
  lapply(split(1:length(lines),cumsum(grepl("^\\s*$",lines))),function(blockIdx){
    block <- lines[blockIdx]
    block <- block[!grepl("^\\s*$",block)]
    if(length(block) == 0){return(NULL)}
    if(length(block) < 3){warning("a block not respecting srt standards has been found")}
    return(data.frame(id=block[1], 
                      times=block[2], 
                      textString=paste0(block[3:length(block)],collapse="\n"),
                      stringsAsFactors = FALSE))
  })

m <- do.call(rbind,listOfEntries)
tmp <- do.call(rbind,strsplit(m[,'times'],' --> ')) # split start and end times
m$startTime <- tmp[,1]
m$endTime <- tmp[,2]
tmp <- do.call(rbind,lapply(strsplit(m$startTime,':|,'),as.numeric)) # parse times
m$fromSeconds  <- tmp %*% c(60*60,60,1,1/1000)
tmp <- do.call(rbind,lapply(strsplit(m$endTime,':|,'),as.numeric)) # parse times
m$toSeconds  <- tmp %*% c(60*60,60,1,1/1000)
m$timeLength <- m$toSeconds - m$fromSeconds # compute time difference in seconds
write_csv(m, "csv/yesterday2.csv", na="NA")

#Figure out how to iterate a function over all the files in a folder.
#Figure out the lag function
#figure out the summarize function

