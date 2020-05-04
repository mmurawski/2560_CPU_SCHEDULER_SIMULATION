"""
Basic CPU scheduler simulator
It takes jobs in form:
'p' 'pid' 'burst' 'priority' 
separated by the \t 
pid is the process id, burst is how much cpu bursts are required to finish the process.
priority is the number stating the importance of the process. (lower number means higher priority)

CPU can read one line at a time (to simulate one burst)
if at specific burst no process arrives it will be denoted as 0 in the file

This is example of a simple usage where 3 processes arrive at the beginning 
and then a 4th process arrives after two bursts
p 1 10 1 p 2 10 1 p 3 13 3
0
0
p 4 10 4.
end of file.

four algorithms will be simulated
First Come First Serve
    It will begin completing a job and won't stop until its finished even if new jobs were posted in the queue

Shortest Job First
    Shortest Jobs in the queue will be completed first

Longest Job first
    Longest Jobs in the queue will be completed first

Round Robin
    A process will be switched for another one in the queue after being worked on a specific number of bursts
    
This program will simulate those algorithms scheduling for parallel systems (ie. with multiple cores or processors)

"""

class cpu: 
    
    #processor/core id
    def __init__(self, id):
        self.id = id
    
    def getid(self):
        return self.id
    
    def setid(self, id):
        self.id = id
    
    def getCurrentEndTime(self):
        return self.curEnd #this is to denote how much bursts cpu needs to complete before its free again.

    def setCurrentEndTime(self, endTime):
        self.curEnd = endTime #this is to denote how much bursts cpu needs to complete before its free again.
    
    #need to implement overloading. 
    # cpu cores need to be comparable based on their bursts required to be free again.
        
