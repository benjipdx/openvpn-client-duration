#! /usr/bin/env python

#parser of openvpn log files to output when a user logs into openvpn and then leaves
import time,datetime

def get_epoch(line):
    timestamp = str(line[4:24])
    datetime = time.strptime(timestamp,'%b %d %H:%M:%S %Y')
    epochtime = time.mktime(datetime)
    epochtime = int(epochtime)
    return epochtime

def main():
    try:

        with open("/var/log/openvpn.log", "r") as logfile:
            data = logfile.read()

        for index,element in list(enumerate(data.split('\n'))):
            if("Initiated") in element:
                init = get_epoch(element)
                for line in data.split('\n')[index:]:
                    if("Inactivity" in line):
                        term = get_epoch(line)
                        parse_list = element.split(' ')
                        if( '' in parse_list):
                            parse_list.remove('')
                        duration = (term-init)/60
                        seconds_of_day = 87000
                        if((int(time.time())-term)<seconds_of_day): #only print out last days worth of logs
                            print("%s connection from %s at %s for %s minutes" %(line[0:24],parse_list[6],parse_list[5],duration))
                        break

            else:
                continue
    except IOError:
        print "log file not found or permissions are wrong. Are you running this as root?"
    except:
        print "error parsing log"
        raise


main()
