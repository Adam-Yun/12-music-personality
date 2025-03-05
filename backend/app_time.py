from datetime import datetime

# Convert time Object to time Str data type
def timeToString(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')

# Convert time Str to time Object data type
def stringToTime(time):
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')