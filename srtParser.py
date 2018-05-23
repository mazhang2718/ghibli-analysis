import pysrt

def calculateElapsedTime(filename):
    totalElapsed = 0
    subs = pysrt.open(filename)
    for i in range(len(subs)):
        sub = subs[i]
        subStart = sub.start
        subEnd = sub.end
        elapsedTime = timeInSeconds(subEnd) - timeInSeconds(subStart)
        totalElapsed += elapsedTime
    return totalElapsed

def timeInSeconds(subTime):
    time = subTime.hours * 60 * 60
    time += subTime.minutes * 60
    time += subTime.seconds
    return time

def calculateRatio(filename, totalTime):
    dialogueTime = calculateElapsedTime(filename)
    ratioTime = dialogueTime / float(totalTime)
    
    print('Total dialogue time for ' + filename + ' is: ' + str(dialogueTime))
    print('Total movie time for ' + filename + ' is: ' + str(totalTime))
    print('Ratio of dialogue to movie for ' + filename + ' is: ' + str(ratioTime))

if __name__ == "__main__":
    totalTimeTotoro = 1*60*60 + 40*60
    calculateRatio('srtFiles/totoro.srt', totalTimeTotoro)

    print('\n')

    totalTimeCoco = 1*60*60 + 49*60
    calculateRatio('srtFiles/coco.srt', totalTimeCoco)
