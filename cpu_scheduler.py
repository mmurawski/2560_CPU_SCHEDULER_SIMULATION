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
        
        
"""
    Order that job arrives indicates its importance level.
    No matter the length of the job, whatever job comes first
    will be served and completed first.
"""
def FCFS(Jobs, Jobsize):
    totalJobLength = 0 # initialized totaljoblength as zero
    ATAT = 0
    TimeSum = 0
    JobEndTime  = []
    
    for i in range(len(Jobs)):
        totalJobLength = totalJobLength + Jobsize[i]
        JobEndTime.insert(len(JobEndTime),totalJobLength)
        
    print("\n Job Name \t | \t Job Endtime \n")
    print("------------------------------------")
    for j in range(len(Jobs)):
        print(Jobs[j], "\t | \t",JobEndTime[j],"ms \n")
        TimeSum = TimeSum + JobEndTime[j]
        
    ATAT = TimeSum / len(Jobs)
    print("\n Average Turnaround Time:",ATAT,"ms \n")
    return

def RoundRobin(Jobs,Jobsize,Slice):
    FinalJob = []
    tempEndTime = []
    finalJobTime = []
    totalJobLength = 0
    newSize = 0
    
    while len(Jobsize)!=0:
        for i in range(len(Jobsize)):
            if Jobsize[i] <= Slice:
                newSize = newSize + Jobsize[i]
                tempEndTime.insert(len(tempEndTime),newSize)
                finalJobTime.insert(len(finalJobTime),newSize)
                FinalJob.insert(len(FinalJob),Jobs[i])
               # Jobsize.erase(Jobsize.begin() + i)  # Since the job is completed, we can erase the current job length from circulation.
				#Jobs.erase(Jobs.begin() + i)	# The corresponding job name is also erased from circulation.
                totalJobLength = totalJobLength + newSize
                i = i - 1
            else:
                newSize = newSize + Slice
                Jobsize[i] = Jobsize[i] - Slice
                tempEndTime.insert(len(tempEndTime),newSize)
    
    print("| \n Job Name \t | \t Job Endtime \n")
    print("------------------------------------")
    for j in range(len(FinalJob)):
        print(FinalJob[i],"\t | \t", finalJobTime[i], "ms \n")
    print("\n Average Turnaround Time: ",(totalJobLength/len(FinalJob)),"ms \n")
    
    return
    

def main():
    #read file maybe
    Jobs = ["Job1","Job2","Job3","Job4","Job5"]
    Jobsize = [7,18,10,4,12]
    print("---------------------------")
    print("First come, First Served")
    FCFS(Jobs, Jobsize)
    
    print("---------------------------")
    print("Round Robin with time slice 2")
    RoundRobin(Jobs, Jobsize,2)
    
    
    return

main() 
        
        
        
    
