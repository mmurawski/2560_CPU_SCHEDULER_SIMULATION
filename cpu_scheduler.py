"""
Basic parallel CPU scheduler simulator 

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
import queue

class cpu: 
    
    #processor/core id
    def __init__(self, num):
        self.coreNum = num
        self.curEnd = 0
        self.idle = True
    
    def getCoreNum(self):
        return self.CoreNum
    
    def getEndTime(self):
        return self.curEnd #this is to denote how much bursts cpu needs to complete before its free again.

    def setEndTime(self, endTime):
        self.curEnd = endTime #this is to denote how much bursts cpu needs to complete before its free again.
  
    def setIdle(self, idleStatus):
        self.idle = idle
        
    def getIdle(self):
        return self.idle
    #need to implement overloading. 
    # cpu cores need to be comparable based on their bursts required to be free again.
            
class process:
    #processor/core id
    def __init__(self, id, burst):
        self.id = id
        self.burst = burst
    
    def getid(self):
        return self.id
    
    def setid(self, id):
        self.id = id
    
    def getBurst(self):
        return self.burst #this is to denote how much bursts cpu needs to complete before its free again.

    def setBurst(self, updatedBurst):
        self.burst = updatedBurst #this is to denote how much bursts cpu needs to complete before its free again.
    
    
"""
    Order that job arrives indicates its importance level.
    No matter the length of the job, whatever job comes first
    will be served and completed first.
"""


        
#edit so it takes the list of processes objects
#edit so that it takes an information about current amount of cores
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

#edited dante's code to work with my class representation
def mod_fcfs(listOfJobs, listOfCores):
    noCores = len(listOfCores) #number of cores
    
    
    execTime = 0 #used to calculate average execution time
    cyclesDone = 0; #multicore processors do their own bursts in parallel. This counter counts how many simultaneous bursts were completed
    
    procqueue = []
    for i in range(len(listOfJobs)):
        procqueue.append(listOfJobs[i])
        execTime = execTime + listOfJobs[i].getBurst() #get the burst requirements of all the processes.
        
        
    while procqueue: 
        #executing bursts
        for i in range(noCores):
            currBurst = listOfCores[i].getEndTime()
            print("Processor ",i," is executing ",currBurst) #if it sais '...executing 0' it means its currently free
            if currBurst == 0: #if the process finished execution
                
                try: # this a hacky way of checking if the queue is empty. I am basically catching exception but not doing anything with it. will make it less janky tomorrow.
                    proc = procqueue.pop(0) #get a new process from a queue
                    print("Process with id:",proc.getid(),"and cpu time requirement of",proc.getBurst()," has started execution on processor",i)
                except:
                    pass
                else:
                    listOfCores[i].setEndTime(proc.getBurst()-1)
                    
                #^assigns a process to a currently empty core
            else:
                listOfCores[i].setEndTime(currBurst - 1) #continue
                
        cyclesDone += 1
        
        if not procqueue: #<- if the process queue is empty, check if some processor still needs to finish executing
            for i in range(noCores):           
               currBurst = listOfCores[i].getEndTime()
               if currBurst == 0:
                   pass #this processor finished execution
               else:
                   print("Processor:",i,"is executing its last",currBurst,"bursts of operation")
                   cyclesDone += currBurst
                   '''
                   don't bother with bursts, just add whatever is remaining to the cores total time
                   '''
    
    
    apt = execTime/len(listOfJobs)
    statIncrease = (cyclesDone - execTime)/execTime
    statIncrease = statIncrease * 100
    
    print("\nCycles of CPU operations done:",cyclesDone)
    print("During this time, this many instructions were completed:",execTime)
    print("Average process time:",apt," cpu cycles")
    print("thanks to parallelism of this machine with",noCores,"cores")
    print("we increased proficiency of this system by:",statIncrease.__abs__())
    print("compared to the single core run of those jobs")
    
    
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
 
def LJF(jobs,jobSize):
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
            if jobSize[j] < jobSize[j+1]:
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
    
def main_test():
    #read file maybe
    Jobs = ["Job1","Job2","Job3","Job4","Job5"]
    jobSize = [9,14,8,43,31]
    print("---------------------------")
    print("First come, First Served")
    FCFS(Jobs, jobSize)
    
    print("---------------------------")
    #RoundRobin(Jobs, jobSize,2)
    print("Round Robin with time slice 2")
    
    print("------------------------------")
    print("Shortest Job First ")
    SJF(Jobs, jobSize)
    
    print("------------------------------")
    print("Longest Job First ")
    LJF(Jobs, jobSize)
    
    return

def main():
    
    p1 = process(1,5)
    p2 = process(2,10)
    p3 = process(3,7)
    p4 = process(4,3)
    p5 = process(5,4)
    p6 = process(6,3)
    p7 = process(7,5)
    procList = [p1,p2,p3,p4,p5,p6,p7]
    
    core1 = cpu(1)
    core2 = cpu(2)
    
    cpuList = [core1, core2]    
    
    mod_fcfs(procList, cpuList)

main()