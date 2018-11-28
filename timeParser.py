import pysrt
import os
import csv
import json

def parseFiles(rootdir):
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".srt"):
                analyzeSrt(file, filepath)
                break

def analyzeSrt(file, filepath):
    subs = pysrt.open(filepath)
    movie = file
    runtime = calculateMovieRuntime(subs)
    pauseSegments = getPauseSegments(subs, runtime)

    with open('data.json', 'w') as f:
        json.dump(pauseSegments, f, ensure_ascii=False)

def calculateMovieRuntime(subs):
    lastSub = subs[-1]
    subEndtime = lastSub.end
    runtime = timeInSeconds(subEndtime)
    return runtime

def getPauseSegments(subs, runtime):
    pauseSegments = []
    timeToFirstSubtitle = timeInSeconds(subs[0].start)
    firstPauseSegment = {'start': 0, 'end': timeToFirstSubtitle}
    pauseSegments.append(firstPauseSegment)
    for i in range(len(subs)):
        sub = subs[i]
        if (i == len(subs) - 1):
            pauseSegment = {'start': timeInSeconds(sub.end), 'end': runtime}
        else:
            nextSub = subs[i+1]
            pauseSegment = {'start': timeInSeconds(sub.end), 'end': timeInSeconds(nextSub.start)}
        pauseSegments.append(pauseSegment)
    return pauseSegments

def timeInSeconds(subTime):
    time = subTime.hours * 60 * 60
    time += subTime.minutes * 60
    time += subTime.seconds
    return time

if __name__ == "__main__":
    rootdir = "srtFiles"
    parseFiles(rootdir)
    # with open('srtAnalysis.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['Movie', 'Runtime', 'TotalPauseTime', 'PauseToRuntimeRatio', 'MeanPauseLength', 'MedianPauseLength', 'PauseStDev', 'NumPausesAboveMean']
    #     #fieldnames = ['Movie', 'Runtime', 'PauseToRuntimeRatio']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     parseFiles(rootdir, writer)
