def __init__(self,inputTaskFile="inputs.txt"):
        self.inputTaskFile = inputTaskFile
        self.processes = []
        self.maxExecTime = 0
        self.currentProc = None
        self.doneTasks = []
        self.quantomSpent = 0
        self.avgWaitTime = 0
        self.avgResponseTime = 0
        self.avgTurnAroundTime = 0
        self.ganttList = []
        self.labelDict = {}
        self.idleGanttList=[]
        # tempTaskInfoFile = open(os.getcwd()+"/"+self.inputTaskFile,'r')
        # counter = 0
        # for proc in tempTaskInfoFile.readlines():
        #     info = proc.split(" ")
        #     print info
        #     temp = Process(info[0],int(info[1]),int(info[2]))
        #     self.labelDict[info[0]] = counter
        #     counter += 1
        #     self.processes.append(temp)
        #     if temp.execTime > self.maxExecTime:
        #         self.maxExecTime = temp.execTime
        # self.labelDict['idle'] = counter
        # print "maximum exec time: ",self.maxExecTime
        # self.taskQueue = []
        # self.tik = 0
        # self.HRNN()
    def loadInput(self,inputText):
        self.processes = []
        self.maxExecTime = 0
        self.currentProc = None
        self.doneTasks = []
        self.quantomSpent = 0
        self.avgWaitTime = 0
        self.avgResponseTime = 0
        self.avgTurnAroundTime = 0
        self.ganttList = []
        self.labelDict = {}
        self.idleGanttList=[]
        counter = 0
        inputText = inputText.strip()
        for proc in inputText.split("\n"):

            info = proc.split(" ")
            print info
            temp = Process(info[0],int(info[1]),int(info[2]))
            self.labelDict[info[0]] = counter
            counter += 1
            self.processes.append(temp)
            if temp.execTime > self.maxExecTime:
                self.maxExecTime = temp.execTime
        self.labelDict['idle'] = counter
        print "maximum exec time: ",self.maxExecTime
        self.taskQueue = []
        self.tik = 0








def SJF(self):
        while True:
            for proc in self.processes:
                if proc.arrivalTime == self.tik:
                    count = 0
                    while len(self.taskQueue) > count and proc.execTime > self.taskQueue[count].execTime: # the = makes it choose the former rather than latter
                        count += 1
                    self.taskQueue.insert(count,proc)
                    print "process ",proc.name," arrived, putting it in: ", count
            if self.currentProc:
                self.stepGantt()
                self.currentProc.remainingTime -= 1
                self.quantomSpent += 1
                if self.currentProc.remainingTime == 0: #task Done
                    print "process ", self.currentProc.name," done..."
                    self.currentProc.finishTime = self.tik + 1
                    self.doneTasks.append(self.currentProc)
                    self.currentProc = None
            else: #no process
                if len(self.taskQueue) > 0:
                    self.currentProc = self.taskQueue.pop(0) #new task comming in
                    if len(self.doneTasks) > 0 :
                        self.stepGantt(self.doneTasks[-1])
                    else:
                        self.stepGantt()
                    self.currentProc.startTime = self.tik
                    self.currentProc.remainingTime -= 1
                    self.quantomSpent += 1
                    if self.currentProc.remainingTime == 0:
                        print "process ", self.currentProc.name," done..."
                        self.currentProc.finishTime = self.tik + 1
                        self.doneTasks.append(self.currentProc)
                        self.currentProc = None
                else:
                    if len(self.doneTasks) == len(self.processes): # all processes done
                        print "all processes done..."
                        self.tik += 1
                        break
                    else:
                        self.stepGantt('idle')
            self.tik += 1
        for proc in self.doneTasks:
            print proc.name," ",proc.arrivalTime," ",proc.startTime," ",proc.finishTime
        self.stepGantt(self.doneTasks[-1])
        self.drawChart()
        self.calcResults()







def RoundRobin(self,quantom):
        stateForChart='begining'
        lastProc = None
        self.quantomSpent = 0
        while True:
            for proc in self.processes:
                if proc.arrivalTime == self.tik:
                    self.taskQueue.append(proc)
                    print "process ",proc.name," arrived"
            if self.currentProc:
                self.stepGantt()
                self.currentProc.remainingTime -= 1
                self.quantomSpent += 1
                if self.currentProc.remainingTime == 0: #task Done
                    print "process ", self.currentProc.name," done..."
                    self.currentProc.finishTime = self.tik + 1
                    self.doneTasks.append(self.currentProc)
                    self.currentProc = None
                    self.quantomSpent = 0
                    stateForChart = 'done'
                elif self.quantomSpent == quantom:
                    self.taskQueue.append(self.currentProc)
                    print "process ",self.currentProc.name," going to the end of line..."
                    self.quantomSpent = 0
                    lastProc = self.currentProc
                    self.currentProc = None
                    stateForChart = 'quantom'


            else: #no process
                if len(self.taskQueue) > 0:
                    self.currentProc = self.taskQueue.pop(0) #new task comming in
                    if stateForChart == 'done':
                        if len(self.doneTasks) > 0:
                            self.stepGantt(self.doneTasks[-1])
                        else:
                            self.stepGantt()
                    elif stateForChart == 'quantom':
                        print "last proc: ",lastProc.name
                        self.stepGantt(lastProc)
                        lastProc= None
                    elif stateForChart == 'begining':
                        self.stepGantt()
                    else:
                        print "error", lastProc
                    if self.currentProc.startTime == None:
                        self.currentProc.startTime = self.tik
                    self.currentProc.remainingTime -= 1
                    self.quantomSpent += 1
                    if self.currentProc.remainingTime == 0:
                        stateForChart = 'done'
                        print "process ", self.currentProc.name," done..."
                        self.currentProc.finishTime = self.tik + 1
                        self.doneTasks.append(self.currentProc)
                        self.currentProc = None
                        self.quantomSpent = 0
                    elif self.quantomSpent == quantom:
                        stateForChart = 'quantom'
                        lastProc = self.currentProc
                        self.taskQueue.append(self.currentProc)
                        print "process ",self.currentProc.name," going to the end of line..."
                        self.quantomSpent = 0
                        self.currentProc = None
                else:
                    if len(self.doneTasks) == len(self.processes): # all processes done
                        print "all processes done..."
                        self.tik += 1
                        break
                    else:
                        self.stepGantt('idle')

            self.tik += 1
        self.stepGantt(self.doneTasks[-1])
        self.drawChart()
        for proc in self.doneTasks:
            print proc.name," ",proc.arrivalTime," ",proc.startTime," ",proc.finishTime
        self.calcResults()