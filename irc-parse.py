import re
from datetime import datetime

#file to read from
logFile = open("#file.log", "r", encoding='UTF-8')
newFile = open("channel.csv", "w", encoding='UTF-8')

#inital constants
lineNum = 1
channel = '#'
sessTime = 'Hello World!'
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
months = ['January','February','March','April','May','June',
        'July','August','September','October','November','December']

#initial csv header
newFile.write('line,channel,date,time,year,month,week_num,weekday,user,nick,message\n')

for line in logFile:
    #gets channel
    if len(channel) == 1:
        chanMatch = re.compile(r'Session Ident: (.*)').search(line)
        if chanMatch:
            channel = chanMatch.group(1)

     #reads Session line for day and year
        sessMatch = re.compile(r'(\w\w\w)\s(\w\w\w)\s(\d\d)\s(\d\d\:\d\d\:\d\d)\s(\d\d\d\d)').search(line)
        if sessMatch:
            sessTime = sessMatch.group()
            dateObj = datetime.strptime(sessTime, '%a %b %d %H:%M:%S %Y')
            timestamp = dateObj.timetuple()     #timestamp in tuple formatted [year, month, day, hr, min, sec, weekday, #day in year, -1] in ints
            year = timestamp[0]
            month = timestamp[1]                #Jan = 1, Dec = 12, etc.
            weekday = timestamp[6]              #Mon = 0, Sun = 6, etc.
            weekNum = dateObj.isocalendar()     #list with [Year, Week of year, Day of Week] in ints
            date = f'{year}-{month}-{timestamp[2]}'

    #Grabs line time and nick
    timeMatch = re.compile(r'(\d\d\:\d\d)').search(line)
    nickMatch = re.compile(r'<(.*?)>').search(line)
    if nickMatch:
        nick = nickMatch.group(1)
        #skip robot lines
        if 'bot' in nick:
            lineNum = lineNum + 1
            continue

    #Retrieves everything after nick bracket
    message = line.split('> ', 1)
    
    #Changes nick to system and grabs message if matches format
    sysMsgMatch = re.compile(r'\:\d\d\]\s\*').search(line)
    if sysMsgMatch:
        nick = 'System'
        message = line.split('* ', 1)

    #Ignores lines that dont fit standard line format
    if timeMatch == None or len(message) == 1:
        #print('Line ' + str(lineNum) + ' is missing a data type')
        lineNum = lineNum + 1
        continue 

    #Prints information in csv format
    else:        
        #strips message of \n character
        message[1] = re.sub("\n", '', message[1])
        newFile.write(f'{str(lineNum)},{channel},{date},{timeMatch.group(1)},{year},{months[month-1]},{weekNum[1]},{days[weekday]},,{nick},"{message[1]}"\n')
        lineNum = lineNum + 1

## [07/25/19 10:29] <palomino> rip
      