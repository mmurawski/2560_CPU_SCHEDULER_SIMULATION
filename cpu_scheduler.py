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
def FCFS(jobs, jobSize):
    totalJobLength = 0 # initialized totaljoblength as zero
    ATAT = 0
    TimeSum = 0
    JobEndTime  = []
    
    for i in range(len(jobs)):
        totalJobLength = totalJobLength + jobSize[i]
        JobEndTime.insert(len(JobEndTime),totalJobLength)
        
    print("\n Job Name \t | \t Job Endtime \n")
    print("------------------------------------")
    for j in range(len(jobs)):
        print(jobs[j], "\t | \t",JobEndTime[j],"ms \n")
        TimeSum = TimeSum + JobEndTime[j]
        
    ATAT = TimeSum / len(jobs)
    print("\n Average Turnaround Time:",ATAT,"ms \n")
    return

def RoundRobin(jobs,jobSize,Slice):
    FinalJob = []
    tempEndTime = []
    finalJobTime = []
    totalJobLength = 0
    newSize = 0
    
    while len(jobSize) > 0:
        for i in range(len(jobSize)-1):  
            print("i==",i)
            if jobSize[i] <= Slice:
                print("deleting")
                newSize = newSize + jobSize[i]
                tempEndTime.insert(len(tempEndTime),newSize)
                finalJobTime.insert(len(finalJobTime),newSize)
                FinalJob.insert(len(FinalJob),jobs[i])
                del jobSize[i]# Since the job is completed, we can erase the current job length from circulation.
                del jobs[i] # The corresponding job name is also erased from circulation.
                totalJobLength = totalJobLength + newSize
                print("newsize",newSize)
                print("totaljoblen",totalJobLength)
                
                i = i - 1
                print("i",i)
                print("======")
            else:
                newSize = newSize + Slice
                jobSize[i] = jobSize[i] - Slice
                tempEndTime.insert(len(tempEndTime),newSize)
                print(newSize)
                print(jobSize[i])
                print("----")
    
    print("| \n Job Name \t | \t Job Endtime \n")
    print("------------------------------------")
    for j in range(len(FinalJob)):
        print(FinalJob[i],"\t | \t", finalJobTime[i], "ms \n")
    print("\n Average Turnaround Time: ",(totalJobLength/len(FinalJob)),"ms \n")
    
    return
    

def SJF(jobs,jobSize):
    FinalJob = []
    finalJobTime = []
    totalJobLength = 0
    TimeSum = 0
    ATAT = 0
    
    for i in range(len(jobSize)-1):
        for j in range(len(jobSize)-1):
            temp1 = 0
            temp2 = 0
            temp3 = ""
            temp4 = ""
            if jobSize[j] > jobSize[j+1]:
                temp1 = jobSize[j]
                temp2 = jobSize[j + 1]
                temp3 = jobs[j]
                temp4 = jobs[j + 1]
                jobSize[j] = temp2 
                jobSize[j + 1] = temp1
                jobs[j] = temp4
                jobs[j] = temp3
                
    for k in range(len(jobSize)):
        totalJobLength = totalJobLength + jobSize[k]
        finalJobTime.insert(len(finalJobTime),totalJobLength)
        
    print("\n Job Name \t|\t Job Endtime \n")
    print("------------------------------------")
    for cur in range(len(finalJobTime)):
        print(jobs[cur],"\t|\t", finalJobTime[cur],"ms \n")
        TimeSum = TimeSum + finalJobTime[cur]
    ATAT = TimeSum/ len(jobs)
    print("\n Average Turnaround Time:", ATAT, "ms \n")
    return
    
    
def main():
    #read file maybe
    Jobs = ["Job1","Job2","Job3","Job4","Job5"]
    jobSize = [9,14,8,43,31]
    print("---------------------------")
    print("First come, First Served")
    FCFS(Jobs, jobSize)
    
    print("---------------------------")
    print("Round Robin with time slice 2")
    #RoundRobin(Jobs, jobSize,2)
    
    print("------------------------------")
    print("Shortest Job First ")
    SJF(Jobs, jobSize)
    
    return

main()