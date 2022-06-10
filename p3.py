import time

"""
 Function return arrival times
"""
def getArrivalTimes(interArrivalTimes):
    arrivals = []
    for i in range(len(interArrivalTimes)):
        if i == 0:
            arrivals.append(interArrivalTimes[0])
            continue
        else:
            arrivals.append(interArrivalTimes[i] + arrivals[i - 1])
    return arrivals

"""
Function to determine if server is free or not
"""
def isAvailable(worker):
    if worker != 0:
        worker -= 1
    return worker

if __name__ == '__main__':
    # Initialize the variables:
    interArrivalTimes = [0, 2, 4, 4, 2, 2]
    serviceTimes = [5, 3, 3, 5, 6, 3]

    arrivalTimes = getArrivalTimes(interArrivalTimes)

    worker = {
        'ServiceTime': 0,
        'ServiceStart': 0,
        'serviceEnd': 0
    }
    
    queue = []
    totalWaiting = 0
    timeClock = 0
    
    endSimu = arrivalTimes[-1] + serviceTimes[-1] + 1
    workerFree = worker['serviceEnd']

    # Starting Simulation
    serviceId = 0
    numberOfWaitings = 0
    
    servicesTotal = len(serviceTimes)
    serviceTotalTime = sum(serviceTimes)
    
    while timeClock < 30 :
        
        print('\nt=', timeClock)
        workerFree = isAvailable(workerFree)

        try:
            workerCheck = timeClock >= worker['serviceEnd']

            #There is an arrival event exist
            if len(arrivalTimes) == 0:
                arrivalTimes.append(-10)

            #There is services in the queue
            if (len(queue) > 0 and workerCheck) or (timeClock == arrivalTimes[0]):
                if queue and workerCheck:
                    waitService = queue.pop(0)
                    start = timeClock
                    serviceTime = waitService['serviceTimes']
                    serviceId = waitService['serviceId']
                    print('waiting for customer..')
                # There is no services in queue but there is a new service
                else:
                    print('new customer arrived..')
                    serviceId = timeClock
                    start = arrivalTimes.pop(0)
                    serviceTime = serviceTimes.pop(0)
                    
                end = start + serviceTime

                #Server is now free after ending its service
                if workerCheck:
                    worker = {
                        'ServiceTime': serviceTime,
                        'ServiceStart': start,
                        'serviceEnd': end
                    }
                    workerFree = worker['ServiceTime'] - 1
                    
                    print('worker is', serviceId, 'serving for', serviceTime, 's')

                #Server is now busy
                else:
                    services = [serv['serviceId'] for serv in queue]
                    serviceId = timeClock
                    
                    if serviceId not in services:
                        if len(queue) == 0:
                            pastEnd = worker['serviceEnd']
                        else:
                            pastEnd = queue[-1]['serviceEnd']
                            
                        waitingAmount = pastEnd - serviceId
                        serviceEnd =  pastEnd + serviceTime

                        # dictionary to save the data of the waiting service.
                        queue.append({
                            'serviceId': serviceId,
                            'serviceTimes': serviceTime,
                            'ServiceStart': pastEnd,
                            'amountOfWait': waitingAmount,
                            'serviceEnd': serviceEnd
                        })
                        totalWaiting += waitingAmount
                        numberOfWaitings += 1
                    
                    print('worker is busy, please wait..')
        except:
            pass

        """There is only one service in the queue but there is no arrival services
           so the end of this service is the end of simulation"""
        if (len(queue) == 1) and (arrivalTimes[0] < 0):
            endSimu = queue[0]['serviceEnd'] 
        
        if timeClock == endSimu: 
            break
        
        time.sleep(1)
        timeClock += 1
    
    print('\nSimulation is DONE\n')
    
    print(
        'Average Waiting time of those who wait in queue d(n)= ', round(totalWaiting / numberOfWaitings, 2),
        '\nTime-average number in queue q(n)= ', round(totalWaiting / endSimu, 2),
        '\nTotal Busy Time B(t)= ', round(serviceTotalTime, 2),
        '\nUtilization u(n) of the worker= ', round(serviceTotalTime / endSimu, 2),
        '\nAverage service time= ', round(serviceTotalTime / servicesTotal, 2),
        '\nAverage waiting time= ', round(totalWaiting / servicesTotal, 2),
        '\nAverage time customer spends in the system= ', round((serviceTotalTime + totalWaiting) / servicesTotal, 2),
        '\nThroughput= ', round(servicesTotal / endSimu, 2),
    )
    