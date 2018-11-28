import pysrt
import os
import csv
import statistics

def parseFiles(rootdir, writer):
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".srt"):
                analyzeSrt(file, filepath, writer)

def analyzeSrt(file, filepath, writer):
    print(filepath, file)
    subs = pysrt.open(filepath)
    movie = file
    runtime = calculateMovieRuntime(subs)
    pauseLengths = getPauseLengths(subs, runtime)
    totalPauseDuration = sum(pauseLengths)
    pauseRatio = totalPauseDuration / float(runtime)
    medianPauseLength = statistics.median(pauseLengths)
    meanPauseLength = statistics.mean(pauseLengths)
    stdevPauses = statistics.stdev(pauseLengths)
    numPauses = numPausesAboveMean(subs, meanPauseLength, pauseLengths)

    writer.writerow({'Movie': movie, 'TotalPauseTime': totalPauseDuration,
        'Runtime': runtime, 'PauseToRuntimeRatio': pauseRatio,
        'MeanPauseLength': meanPauseLength, 'MedianPauseLength': medianPauseLength,
        'PauseStDev': stdevPauses, 'NumPausesAboveMean': numPauses})

def calculateMovieRuntime(subs):
    lastSub = subs[-1]
    subEndtime = lastSub.end
    runtime = timeInSeconds(subEndtime)
    return runtime

def numPausesAboveMean(subs, mean, pauseLengths):
    numPauses = 0
    for pause in pauseLengths:
        if pause > mean:
            numPauses += 1
    return numPauses

def getPauseLengths(subs, runtime):
    pauseLengths = []
    timeToFirstSubtitle = timeInSeconds(subs[0].start)
    pauseLengths.append(timeToFirstSubtitle)
    for i in range(len(subs)):
        sub = subs[i]
        if (i == len(subs) - 1):
            pauseLength = runtime - timeInSeconds(sub.end)
        else:
            nextSub = subs[i+1]
            pauseLength = timeInSeconds(nextSub.start) - timeInSeconds(sub.end)
        pauseLengths.append(pauseLength)
    return pauseLengths

def timeInSeconds(subTime):
    time = subTime.hours * 60 * 60
    time += subTime.minutes * 60
    time += subTime.seconds
    return time

def calculateRatio(subs, movieRuntime):
    dialogueTime = calculateDialogueTime(subs)
    pauseTime = movieRuntime - dialogueTime
    ratioTime = pauseTime / float(movieRuntime)
    return ratioTime

if __name__ == "__main__":
    rootdir = "../srt-files"
    with open('srtAnalysis.csv', 'w', newline='') as csvfile:
        fieldnames = ['Movie', 'Runtime', 'TotalPauseTime', 'PauseToRuntimeRatio', 'MeanPauseLength', 'MedianPauseLength', 'PauseStDev', 'NumPausesAboveMean']
        #fieldnames = ['Movie', 'Runtime', 'PauseToRuntimeRatio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        parseFiles(rootdir, writer)
