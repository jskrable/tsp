import subprocess as sub

# script to execute program in sets of 10 with incrementing size
for i in range(68, 100):
    for j in range(1, 3):
        p = sub.Popen('py tsp.py -s '+str(i), shell=True)
        print('running size ' + str(i) + ' simulation ' + str(j))
        p.communicate()
