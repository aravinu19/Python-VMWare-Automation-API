from flask import Flask, render_template, request, Response
import json
import Controller
import fileHandler

controller = ""

app = Flask(__name__, template_folder='public_html')

@app.route('/home')
def indexPage():
    return render_template("index.html")


@app.route('/loginPortal')
def loginPortal():
    return render_template("loginportal.html")


@app.route('/preloader')
def preloader():
    return render_template("preloader.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/test')
def testPage():
    return render_template("test.html")


@app.route('/connect', methods = ['POST', 'GET'])
def HyperConnect():
    if request.method == 'POST':
        print(request.get_json(force=True))

        host_ip = request.get_json(force=True)['hostip']
        username = request.get_json(force=True)['username']
        password = request.get_json(force=True)['password']

        fileObj = fileHandler.FilesHandler()
        fileObj.jsonFile_writer({
            "hostip": host_ip,
            "username": username,
            "password": password
        })

        controller = Controller.Creds(hostip=host_ip, username= username, password= password)

        return Response(controller.connect(), mimetype='application/json')
    else:
        return "<h1>Not Proper</h1>"


@app.route('/getvms', methods = ['POST', 'GET'])
def get_vm_list():
    if request.method == 'POST':
        fileObj = fileHandler.FilesHandler()

        if fileObj.creds_check():
            credsData = fileObj.jsonFile_Reader()
            controller = Controller.Creds(hostip=credsData["hostip"], username=credsData["username"], password=credsData["password"])
            return Response(controller.connect(), mimetype='application/json')
        else:
            return "<h1> Please login before you can get vm list </h1>"

    else:
        return "<h1>Please Send a POST Request</h1>"


@app.route('/power_on', methods = ['POST','GET'])
def powerOn():
    if request.method == 'POST':
        print(request.get_json(force=True))
        vmname = request.get_json(force=True)["vmname"]
        fileObj = fileHandler.FilesHandler()

        if fileObj.creds_check():
            credsData = fileObj.jsonFile_Reader()
            controller = Controller.Creds(hostip=credsData["hostip"], username=credsData["username"], password=credsData["password"])
            return Response(controller.powerOn(vmname=vmname), mimetype='application/json')
        else:
            return "<h1> Please login before you can get vm list </h1>"
    else:
        return "<h1>Send a Post Request</h1>"


@app.route('/power_off', methods = ['POST','GET'])
def powerOff():
    if request.method == 'POST':
        print(request.get_json(force=True))
        vmname = request.get_json(force=True)["vmname"]
        fileObj = fileHandler.FilesHandler()

        if fileObj.creds_check():
            credsData = fileObj.jsonFile_Reader()
            controller = Controller.Creds(hostip=credsData["hostip"], username=credsData["username"], password=credsData["password"])
            return Response(controller.powerOff(vmname=vmname), mimetype='application/json')
        else:
            return "<h1> Please login before you can get vm list </h1>"
    else:
        return "<h1>Send a Post Request</h1>"


@app.route('/maintanence', methods= ['POST', 'GET'])
def EnterMaintanenceMode():
    if request.method == 'POST':
        print(request.get_json(force=True))
        mode = request.get_json(force=True)["mode"]
        fileObj = fileHandler.FilesHandler()
        if mode == 'ON':
            if fileObj.creds_check():

                credsData = fileObj.jsonFile_Reader()
                controller = Controller.Creds(hostip=credsData["hostip"], username=credsData["username"], password=credsData["password"])
                listvm = controller.connect()
                fileObj.jsonFile_CreateMaintanenceData(data=listvm)
                listvm = controller.MaintanenceModeOn(mdata=listvm)

                for vm in listvm:
                    controller.powerOff(vmname=str(vm))

                return json.dumps({"mode":"Activated"})

            else:
                return "<h1> Please login before you can get vm list </h1>"
        else:

            if fileObj.creds_check():

                credsData = fileObj.jsonFile_Reader()
                controller = Controller.Creds(hostip=credsData["hostip"], username=credsData["username"], password=credsData["password"])

                if fileObj.mode_check():
                    listvm = fileObj.jsonFile_ReadMaintanenceData()
                    listvm = controller.MaintanenceModeOff(mdata=listvm)
                    listvm = json.loads(str(listvm))
                    for vm in listvm:
                        controller.powerOn(vmname=str(vm))

                    return json.dumps({"mode":"Deactivated"})
                else:
                    return "<h2>Please Turn On Maintanence Mode Before Turning Off :) </h2>"

            else:
                return "<h1> Please login before you can get vm list </h1>"

    else:
        return "<h2>Send a POST Request</h2>"


@app.route('/createvm', methods = ['POST', 'GET'])
def CreateVM():
      if request.method == 'POST':
          print(request.get_json(force=True))
          vmname = request.get_json(force=True)['vmname']
          memory = request.get_json(force=True)['memory']
          vdisk = request.get_json(force=True)['vdisk']
          fileObj = fileHandler.FilesHandler()

          if fileObj.creds_check():
              credsData = fileObj.jsonFile_Reader()
              controller = Controller.Creds(hostip=credsData["hostip"], username=credsData["username"], password=credsData["password"])
              return Response(controller.CreateVM(vmname=vmname, memory=memory, diskspace=vdisk), mimetype='application/json')
          else:
              return "<h1> Please login before you can get vm list </h1>"
      else:
         return "<h1>Send a POST Request</h1>"


@app.route('/sign_out', methods = ['POST', 'GET'])
def signOut():
    fileObj = fileHandler.FilesHandler()

    if fileObj.creds_check():
        return Response(fileObj.jsonFile_delete(), mimetype='application/json')
    else:
        return "<h1> Please login before you can get vm list </h1>"


@app.route('/h2', methods = ['POST', 'GET'])
def H2():
    if request.method == 'POST':
        firstName = request.form['firstname']
        lastName = request.form['lastname']
        return "<h2>Hello " + str(firstName) + " " + str(lastName) + "</h2>"
    return "<h2>Send a POST Request</h2>"


if __name__ == '__main__':
    app.run(debug = True, host = 'localhost')
