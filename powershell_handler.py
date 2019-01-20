import subprocess
import re

class PowerShellHandler:
    def runTestCmds(self, psFile, arguments):
        process = subprocess.Popen(['powershell', str(psFile + arguments)], stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        stdout, stderr = process.communicate()

        print("Error: " + str(stderr))
        print("Output: " + str(stdout))

        if stderr ==  b'':
            return True
        else:
            return False
