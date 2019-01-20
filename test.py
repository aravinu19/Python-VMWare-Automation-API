import csv
import os
import json
from crontab import CronTab
import fileHandler as fh
import subprocess

# f = open(os.getcwd() + "\\ccc.txt", mode='r')
# lines = f.readlines()
# index = 0
# VMList = []
# for line in lines:
#     if index < 3 :
#         index += 1
#     else :
#         if '\n' in line[0]:
#             break
#         name, state = line.split('   ',2)
#         tempList = {"Name": name, "state": state.split('\n')[0]}
#         VMList.append(tempList)
#         print(name + " " + state.split('\n')[0])
#
# outputDict = {}
#
# count = 0
#
# for element in VMList:
#     outputDict[count] = element
#     count += 1
#
# outputDict = json.dumps(outputDict)
#
# print(outputDict)

# str  = json.load(open("ste.json"))
fhand = fh.FilesHandler()
mdata = fhand.jsonFile_ReadMaintanenceData()
poweredOnVM = []
for index in mdata:
    if mdata[index]['state'] == "PoweredOn":
        poweredOnVM.append(mdata[index]['Name'])
        print(mdata[index])


print(str(poweredOnVM))

count = 0
st = ''
for item in poweredOnVM:
    if count == 0:
        st.join(item)
        count += 1
    else:
        st.join(','.join(item))



process = subprocess.Popen(['powershell', str(".\\PowerShellScripts\\PowerOnVM.ps1 " + )], stdout=subprocess.PIPE, stderr= subprocess.PIPE)
stdout, stderr = process.communicate()

print("Error: " + str(stderr))
print("Output: " + str(stdout))
