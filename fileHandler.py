import os
import json
from pathlib import Path

class FilesHandler:
    def readFile(self, path):
        file = open(path, mode='r')
        return file

    def json_generator(self, listObj):
        outputDict = {}
        count = 0

        for element in listObj:
            outputDict[count] = element
            count += 1

        outputDict = json.dumps(outputDict)
        return outputDict

    def jsonFile_writer(self, credsData):
        with open('creds.json', 'w') as jsonFile:
            json.dump(credsData, jsonFile)
        print("Credentials Stored to creds.json")

    def jsonFile_CreateMaintanenceData(self, data):
        with open('Mmode.json', 'w') as jsonFile:
            json.dump(data, jsonFile)
        print("Maintanence Data stored to Mmode.json")

    def creds_check(self):
        file = Path(os.getcwd() + "\\creds.json")
        if file.is_file():
            return True
        else:
            return False

    def mode_check(self):
        file = Path(os.getcwd() + "\\Mmode.json")
        if file.is_file():
            return True
        else:
            return False

    def jsonFile_Reader(self):
        with open('creds.json') as jsonFile:
            credsData = json.load(jsonFile)
            print(credsData)
            return credsData

    def jsonFile_ReadMaintanenceData(self):
        with open('Mmode.json') as jsonFile:
            ModeData = json.load(jsonFile)
            print(ModeData)
            return ModeData

    def jsonFile_delete(self):
        os.remove("creds.json")
        return json.dumps({"operation": "Sign Out Completed"})

    def jsonFile_deleteMaintanenceData(self):
        os.remove("Mmode.json")
        return json.dumps({"operation": "VM restoration Completed"})

    def read_vmlist(self):
        file = self.readFile(os.getcwd() + "\\txtFiles\\vmlist.txt")
        lines = file.readlines()

        index = 0
        VMList = []

        for line in lines:
            if index < 3 :
                index += 1
            else :
                if '\n' in line[0]:
                    break
                name, state = line.split('   ',2)
                tempList = {"Name": name, "state": state.split('\n')[0]}
                VMList.append(tempList)
                print(name + " " + state.split('\n')[0])

        return self.json_generator(VMList)

    def check_vm_power_operation(self, state):
        file = self.readFile(os.getcwd() + "\\txtFiles\\vmstate.txt")
        lines = file.readlines()

        if state in lines[3]:
            return True
        else:
            return False
