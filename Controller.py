import powershell_handler
import fileHandler
import json

class Creds:
    def __init__(self, hostip, username, password):
        self.set_hostip(hostip=hostip)
        self.set_username(username=username)
        self.set_password(password=password)

    def set_hostip(self, hostip):
        self._hostip = hostip

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def get_hostip(self):
        return self._hostip

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def connect(self):
        print(self.get_hostip())
        powershellObj = powershell_handler.PowerShellHandler()
        arguments = " " + str(self.get_hostip()) + " " + str(self.get_username()) + " " + str(self.get_password())
        if powershellObj.runTestCmds(".\\PowerShellScripts\\ConnectAndListVM.ps1", arguments=arguments) is True :
            FileObj = fileHandler.FilesHandler()
            return FileObj.read_vmlist();
        else:
            return "<h2>Some Error Occured while reading VM Details :(</h2>"

    def powerOn(self, vmname):
        powershellObj = powershell_handler.PowerShellHandler()
        arguments = " " + str(self.get_hostip()) + " " + str(self.get_username()) + " " + str(self.get_password() + " " + str(vmname))

        if powershellObj.runTestCmds(".\\PowerShellScripts\\PowerOnVM.ps1", arguments=arguments) is True:
            FileObj = fileHandler.FilesHandler()

            if FileObj.check_vm_power_operation(state="PoweredOn"):
                return json.dumps({"operation": "Success"})
            else:
                return json.dumps({"operation": "Pending"})
        else:
            return "<h2>Something went wrong :(</h2>"

    def powerOff(self, vmname):
        powershellObj = powershell_handler.PowerShellHandler()
        arguments = " " + str(self.get_hostip()) + " " + str(self.get_username()) + " " + str(self.get_password() + " " + str(vmname))

        if powershellObj.runTestCmds(".\\PowerShellScripts\\PowerOffVM.ps1", arguments=arguments) is True:
            FileObj = fileHandler.FilesHandler()

            if FileObj.check_vm_power_operation(state="PoweredOff"):
                return json.dumps({"operation": "Success"})
            else:
                return json.dumps({"operation": "Pending"})
        else:
            return "<h2>Something went wrong :(</h2>"

    def MaintanenceModeOn(self, mdata):
        mdata = json.loads(str(mdata))
        poweredOnVM = []

        for index in mdata:
            print(mdata[index])
            if mdata[index]['state'] == "PoweredOn":
                poweredOnVM.append(mdata[index]['Name'])

        return poweredOnVM

    def MaintanenceModeOff(self, mdata):
        mdata = json.loads(str(mdata))
        poweredOnVM = []

        for index in mdata:
            if mdata[index]['state'] == "PoweredOn":
                poweredOnVM.append(mdata[index]['Name'])

        return poweredOnVM

    def CreateVM(self, memory, diskspace, vmname):
        psHandler = powershell_handler.PowerShellHandler()
        arguments = " " + str(vmname) + " " + str(memory) + " " + str(diskspace)
        if psHandler.runTestCmds(psFile=".\\PowerShellScripts\\CreateVM.ps1", arguments=arguments):
            return json.dumps({"operation":"VM Created"})
        else:
            return json.dumps({"operation":"Error in Creation"})
