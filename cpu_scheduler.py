"""
Basic parallel CPU scheduler simulator 

Three algorithms will be simulated
First Come First Serve
    It will begin completing a job and won't stop until its finished even if new jobs were posted in the queue

Shortest Job First
    Shortest Jobs in the queue will be completed first

Longest Job first
    Longest Jobs in the queue will be completed first

This program will simulate those algorithms scheduling for parallel systems (ie. with multiple cores or processors)

"""
from queue import PriorityQueue
import random

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
        self.idle = idleStatus
        
    def getIdle(self):
        return self.idle
    #need to implement overloading. 
    # cpu cores need to be comparable based on their bursts required to be free again.
            
class process:
    #processor/core id
    def __init__(self, pid, burst):
        self.id = pid
        self.burst = burst
    
    def getid(self):
        return self.id
    
    def setid(self, pid):
        self.id = pid
    
    def getBurst(self):
        return self.burst #this is to denote how much bursts cpu needs to complete before its free again.

    def setBurst(self, updatedBurst):
        self.burst = updatedBurst #this is to denote how much bursts cpu needs to complete before its free again.
    
    def __lt__(self, proc2):
        return self.burst < proc2.burst

    def __str__(self):
        string1 = "Process: "+str(self.id)+" with burst requirements:"+str(self.burst)
        return string1
        
def FCFS(procList):
    jobs = []
    jobSize = []
    jobs, jobSize = decoupleJobs(procList)
    
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


def multicore_fcfs(listOfJobs): #works single core
    noCpu = input("Input how many cpu cores there are:")
    listOfCores = prepareCores(noCpu)
        
    noCores = len(listOfCores) #number of cores
    execTime = 0 #used to calculate average execution time
    cyclesDone = 0; #multicore processors do their own bursts in parallel. This counter counts how many simultaneous bursts were completed
    procqueue = []
    
    for i in range(len(listOfJobs)):
        procqueue.append(listOfJobs[i])
        execTime = execTime + listOfJobs[i].getBurst() #get the burst requirements of all the processes.
        
    while procqueue: #executing bursts
        for i in range(noCores):
            currBurst = listOfCores[i].getEndTime()
            #print("Processor ",i," is executing ",currBurst) #if it sais '...executing 0' it means its currently free
            if currBurst == 0: #if the process finished execution
                try:
                    proc = procqueue.pop(0) #get a new process from a queue
                    print("Process with id:",proc.getid(),"and cpu time requirement of",proc.getBurst()," has started execution on processor",i)
                except:
                    print("Core ",i," is idle")
                    
                    pass
                else:
                    listOfCores[i].setEndTime(proc.getBurst()-1)
                #^assigns a process to a currently empty core
            else:
                listOfCores[i].setEndTime(currBurst - 1) #continue
                
        cyclesDone += 1
        
        listOfBursts = [] #used to find the remining time cpu has to be operational when queue is empty
        if not procqueue: #<- if the process queue is empty, check if some processor still needs to finish executing
            for i in range(noCores):           
               currBurst = listOfCores[i].getEndTime()
               if currBurst == 0:
                   pass #this processor finished execution
               else:
                   print("Processor:",i,"is executing its last",currBurst,"bursts of operation")
                   listOfBursts.append(currBurst)
               
            listOfBursts.sort()
            cyclesDone += listOfBursts[-1] #adding the work of a last cpu to finish to our cycles count 

    apt = execTime/len(listOfJobs)
    statIncrease = (cyclesDone - execTime)/execTime
    statIncrease = statIncrease * 100
    
    print("\nCycles of CPU operations done:",cyclesDone)
    print("During this time, this many instructions were completed:",execTime)
    print("Average process time:",apt," cpu cycles")
    print("thanks to parallelism of this machine with",noCores,"cores")
    print("we increased proficiency of this system by:",statIncrease.__abs__())
    print(" percents compared to the single core run of those jobs")
    
    for i in range(noCores):           
        currBurst = listOfCores[i].setEndTime(0) #reset the processors

    return
    
def multicore_sjf(listOfJobs): #works single core
    noCpu = input("Input how many cpu cores there are:")
    listOfCores = prepareCores(noCpu)

    noCores = len(listOfCores) #number of cores 
    execTime = 0 #used to calculate average execution time
    cyclesDone = 0; #multicore processors do their own bursts in parallel. This counter counts how many simultaneous bursts were completed 
    procqueue = PriorityQueue()

    for i in range(len(listOfJobs)):
        procqueue.put(listOfJobs[i])
        execTime = execTime + listOfJobs[i].getBurst() #get the burst requirements of all the processes.
        
    while not procqueue.empty():     #executing bursts
        for i in range(noCores):
            currBurst = listOfCores[i].getEndTime()
            #print("Processor ",i," is executing ",currBurst) #if it sais '...executing 0' it means its currently free
            if currBurst == 0: #if the process finished execution
                    proc = procqueue.get() #get a new process from a queue
                    if proc:
                        print("Process with id:",proc.getid(),"and cpu time requirement of",proc.getBurst()," has started execution on core",i)
                    else:
                        print("Core ",i," is idle")
                        pass
                    
                    listOfCores[i].setEndTime(proc.getBurst()-1)
                #^assigns a process to a currently empty core
            else:
                listOfCores[i].setEndTime(currBurst - 1) #continue
                
        cyclesDone += 1
        listOfBursts = [] #used to find the remining time cpu has to be operational when queue is empty
        if procqueue.empty(): #<- if the process queue is empty, check if some processor still needs to finish executing
            for i in range(noCores):           
               currBurst = listOfCores[i].getEndTime()
               if currBurst == 0:
                   pass #this processor finished execution
               else:
                   print("Processor:",i,"is executing its last",currBurst,"bursts of operation")
                   listOfBursts.append(currBurst)    
                   
            listOfBursts.sort()
            cyclesDone += listOfBursts[-1] #adding the work of a last cpu to finish to our cycles count 
     
    apt = execTime/len(listOfJobs)
    statIncrease = (cyclesDone - execTime)/execTime
    statIncrease = statIncrease * 100
    
    print("\nCycles of CPU operations done:",cyclesDone)
    print("During this time, this many instructions were completed:",execTime)
    print("Average process time:",apt," cpu cycles")
    print("thanks to parallelism of this machine with",noCores,"cores")
    print("we increased proficiency of this system by:",statIncrease.__abs__())
    print("percents compared to the single core run of those jobs")
    
    for i in range(noCores):           
        currBurst = listOfCores[i].setEndTime(0) #reset the processor
    
    return

def multicore_ljf(listOfJobs): #works single core
    noCpu = input("Input how many cpu cores there are:")
    listOfCores = prepareCores(noCpu)
        
    noCores = len(listOfCores) #number of cores
    execTime = 0 #used to calculate average execution time
    cyclesDone = 0; #multicore processors do their own bursts in parallel. This counter counts how many simultaneous bursts were completed    
    procqueue = PriorityQueue()

    for i in range(len(listOfJobs)):
        newValue = listOfJobs[i].getBurst()
        listOfJobs[i].setBurst(newValue*-1) #done so the priorityQueue works in reverse and longests jobs are first
        procqueue.put(listOfJobs[i])
        execTime = execTime + listOfJobs[i].getBurst() #get the burst requirements of all the processes.
        
    while not procqueue.empty():         #executing bursts
        for i in range(noCores):
            currBurst = listOfCores[i].getEndTime()
            if currBurst == 0: #if the process finished execution
                    proc = procqueue.get() #get a new process from a queue
                    if proc:
                        print("Process with id:",proc.getid(),"and cpu time requirement of",proc.getBurst()*-1," has started execution on core",i)
                    else:
                        print("Core ",i," is idle")
                        pass
                    
                    listOfCores[i].setEndTime(proc.getBurst()+1)
                #^assigns a process to a currently empty core
            else:
                listOfCores[i].setEndTime(currBurst +1) #continue
                
        cyclesDone += 1        
        
        listOfBursts = [] #used to find the remining time cpu has to be operational when queue is empty
        if procqueue.empty(): #<- if the process queue is empty, check if some processor still needs to finish executing
            for i in range(noCores):           
               currBurst = listOfCores[i].getEndTime()
               if currBurst == 0:
                   pass #this processor finished execution
               else:
                   print("Processor:",i,"is executing its last",currBurst*-1,"bursts of operation")
                   listOfBursts.append(currBurst*-1)               
            listOfBursts.sort()
            cyclesDone += listOfBursts[-1] #adding the work of a last cpu to finish to our cycles count    

    execTime = execTime*-1
    apt = (execTime/len(listOfJobs))
    statIncrease = (cyclesDone - execTime)/execTime
    statIncrease = statIncrease * 100
    
    print("\nCycles of CPU operations done:",cyclesDone)
    print("During this time, this many instructions were completed:",execTime)
    print("Average process time:",apt," cpu cycles")
    print("thanks to parallelism of this machine with",noCores,"cores")
    print("we increased proficiency of this system by:",statIncrease.__abs__())
    print("percents compared to the single core run of those jobs")
    
    
    for i in range(len(listOfJobs)):
        newValue = listOfJobs[i].getBurst()
        listOfJobs[i].setBurst(newValue*-1) #this is to fix the list back to normal 
        #print(listOfJobs[i])
    for i in range(noCores):           
        currBurst = listOfCores[i].setEndTime(0) #reset the processor
    
    return
   

def SJF(procList):
    jobs = []
    jobSize = []
    jobs, jobSize = decoupleJobs(procList)
    
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
 
def LJF(procList):
    jobs = []
    jobSize = []
    jobs, jobSize = decoupleJobs(procList)
    
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
    
def generateRandomJobs(noJobs):
    jobs = list()
    for i in range(1, noJobs+1):
        jobs.append(process(i,random.randint(1,25)))
        
    return jobs

def prepareCores(noCores):
    numCores = int(noCores)
    cpuList = []
    for i in range(1, numCores+1):
        cpuList.append(cpu(i))
    
    return cpuList

def printJobs(jobs):
    for i in range(len(jobs)):
        print(jobs[i])

def decoupleJobs(jobs): #this method exists to bridge how Matt and Dante approach enumarating lists
    #this method will convert Matt's way of making jobs to one that works with Dante's code
    jobid = []
    jobsize = []
    
    for i in range(len(jobs)):
        print(jobs[i].getid()," and their requirement:",jobs[i].getBurst())
        jobid.append(jobs[i].getid())
        jobsize.append(jobs[i].getBurst())

    return jobid, jobsize

def openFile():
    try:
        name = input("Please enter the file name: ")
        file1 = open(name, 'r')
    except FileNotFoundError:
        print("File not found")
        return 0
    else:
        file1.close
        return file1
    
def readFileIntoTasks(file1):
    procList = []
    
    if file1 != 0:
        for line in file1:
            lineList = line.split() 
            
            try:
                pid = int(lineList[0])
                burst = int(lineList[1])
                procList.append(process(pid, burst))
            except IndexError:
                print("Wrong format of the file")
            except:
                print("Something went wrong")
                
    return procList    
 
def introMsg():
    print("Welcome to CPU scheduling simulator of single and multi core architectures. \n",
              "-"*15,"\nTo start, choose if you want to test the algorithms against a list of tasks or "
              ,"from a file or tasks that are randomly generated. This program comes with three ",
              "example test files: test1.txt, test2.txt, test3.txt. \nReadme includes details on how to ",
              "create your own testing text files for this simulation.")    

def testTypeMsg():
    print("What type of test to you want perform?")
    print("1. Single-Core First Come, First Serve")
    print("2. Single-Core Shortest Job First")
    print("3. Single-Core Longest Job First")
    print("4. Multi-Core First Come, First Serve")
    print("5. Mutli-Core Shortest Job First")
    print("6. Multi-Core Longest Job First")
    print('x. Go back and generate or read other jobs')

def repeatedTestMsg():
    print("You can repeat the test on the same tasks but with different simulation settings:")
    print("Press m to display the test menus again: ")

def main():
    #loop unless x is pressed
    #do you want to read from a file or generate jobs?
    #if read a file, loop until it does not fail (or x is pressed)
    #single core or multiple core?
    #single core uses dante code and perform decouple before it starts
    #multicore asks for range of cpus check if its more than 2 but less than 64
    
    exitSymbol = False
    introMsg()
    
    while not exitSymbol:
               
        print("Enter your selection: ")
            
        choice = input("1. Tasks from a file\n2. Randomly generated tasks\nx. Quit the program\n")
        if choice == '1':
            file = openFile()
            procList = readFileIntoTasks(file)
            
        elif choice == '2':
            noJobs = input("Enter number of tasks you want to test: ")
            try:
                noJobs = int(noJobs)
                procList = generateRandomJobs(noJobs)
            except TypeError:
                print("Number has to be typed")
        elif choice == 'x':
            print("Goodbye")
            exitSymbol = True;
            break
        else:
            print("Wrong choice, try again.")
        
        
        
        while choice != 'x':
            testTypeMsg()
            choice = input("What is your test selection:" )
            if choice == '1':
                print("---------------------------")
                print("First come, First Served")
                FCFS(procList)
            elif choice == '2':
                print("------------------------------")
                print("Shortest Job First ")
                SJF(procList)
            elif choice == '3':
                print("------------------------------")
                print("Longest Job First ")
                LJF(procList)
            elif choice == '4':  
                print("---------------------------")
                print("Multi-Core FCFS")
                multicore_fcfs(procList)
            elif choice == '5':
                print("---------------------------")
                print("Multi-Core SJF")
                multicore_sjf(procList)
            elif choice == '6':
                print("---------------------------")
                print("Multi-Core LJF")
                multicore_ljf(procList)
            elif choice == 'x':
                break
            elif choice == 'm':
                testTypeMsg()
        
            

    return


main()