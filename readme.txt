Cpu Scheduler simulation for single core and multi core architectures by Mateusz Murawski and Dante Martinez for CS 2520 Class, Cal Poly Pomona Spring 2020

This program simulates three algorithms: First Come First Serve, Shortest Job First and Longest Job First. Those algorithms can be tested in a single core scenario or a multi core scenario with user choosing the amount of cores in the architecture. All tasks are assumed to arrive at the 0 cpu cycle. 

Running ============================
To run this code, User has to make user they have python installed on their computer.
After that they have to open up their command line or terminal application and navigate to where the program is stored and run it with a command: python cpu_scheduler.py

Program works on Windows, Mac OS X and Linux

How it works =======================
Processes for the simulator can be read from a file or randomly generated. This program comes with three test processes files that can be used in this simulation called test1.txt, test2.txt and test3.txt. Custom files can also be used.

Main Menu ==========================

When a user launches the program, they are greeted with three choices. They can open up a file by inputing its name or they can choose to randomly generate tasks to be used in the algorithm. 

After generating tasks or reading them from a file users can choose to perform various algorithms in either single or multi core scenerio. Multiple Tests can be perform on the same set of tasks for the performance evaluation of the algorithm. If a user chooses to load another set of jobs (either from a file or randomly generated) they can exit out of the algorithm choice menu by typing x and pressing enter. 

Exiting the program ================
When user is in the main menu they can exit the whole program by typing x and pressing enter again

Putting custom files ===============
Additionally, User can supply their own plain text document with jobs. Specific formatting is required. A single job has a format "pid	cpu_requirement" with a single tab separating pid and cpu_requirement. Both fields have to be numerical values. 

An example custom file looks like this:
1	5
2	10
3	15

This means that we want to test three processes with pids: 1,2 and 3 that have cpu requirements 5, 10 and 15 respectively. 