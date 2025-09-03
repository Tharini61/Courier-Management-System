from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pickle
import pymysql
import os
from django.core.files.storage import FileSystemStorage
from datetime import date
import matplotlib.pyplot as mplt
import io
import base64
import numpy as np

global uname

def ViewFeedback(request):
    if request.method == 'GET':
        output = '<table border=1><tr>'
        output+='<td><font size="" color="black">Courier&nbsp;ID</td>'
        output+='<td><font size="" color="black">Feedback</td>'
        output+='<td><font size="" color="black">Feedback Date</td>'
        output+='<td><font size="" color="black">Feedback Rank</td></tr>'
        rank = []
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM feedback")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+str(row[0])+'</td>'
                output+='<td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td></tr>'
                rank.append(row[3])
        output += "</table><br/>"
        unique, count = np.unique(np.asarray(rank), return_counts=True)
        mplt.pie(count,labels=unique,autopct='%1.1f%%')
        mplt.title('Feedback Ranking Graph')
        mplt.axis('equal')
        buf = io.BytesIO()
        mplt.savefig(buf, format='png', bbox_inches='tight')
        mplt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()    
        context= {'data':output, 'img': img_b64}
        return render(request, 'ViewFeedback.html', context)

def getDetails(pid):
    status = False
    emp = ""
    sender = ""
    sender_phone = ""
    receiver = ""
    amount= ""
    delivery = ""
    img = ""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select collected_employee,sender_name,sender_phone,receiver_name,amount,expected_delivery,parcel_image FROM parcel where parcel_id = '"+pid+"'")
        rows = cur.fetchall()
        for row in rows:
            emp = row[0]
            sender = row[1]
            sender_phone = row[2]
            receiver = row[3]
            amount = row[4]
            delivery = row[5]
            img = row[6]
            break
    return emp,sender,sender_phone,receiver,amount,delivery,img

def UserMap(request):
    if request.method == 'GET':
        name = request.GET.get('t1', False)
        output = '<iframe width="625" height="650" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q='+name+'&amp;ie=UTF8&amp;&amp;output=embed"></iframe><br/>'
        context= {'data':output}
        return render(request, 'UserMap.html', context)

def CourierTrack(request):
    if request.method == 'GET':
       return render(request, 'CourierTrack.html', {})

def CourierTrackAction(request):
    if request.method == 'POST':
        global uname
        pid = request.POST.get('t1', False)
        emp,sender,sender_phone,receiver,amount,delivery,img = getDetails(pid)
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Collected Employee</th><th><font size="" color="black">Sender Name</th>'
        output+='<th><font size="" color="black">Sender Phone</th><th><font size="" color="black">Receiver Name</th>'
        output+='<th><font size="" color="black">Amount</th><th><font size="" color="black">Expected Delivery</th>'
        output+='<th><font size="" color="black">Current Location</th>'
        output+='<th><font size="" color="black">Updated Date</th><th><font size="" color="black">Status</th>'
        output += '<th><font size="" color="black">Parcel Image</th><th><font size="" color="black">View on Map</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM update_status where parcel_id = '"+pid+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<td><font size="" color="black">'+emp+'</td><td><font size="" color="black">'+sender+'</td>'
                output+='<td><font size="" color="black">'+sender_phone+'</td><td><font size="" color="black">'+receiver+'</td>'
                output+='<td><font size="" color="black">'+amount+'</td><td><font size="" color="black">'+delivery+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td>'
                output+='<td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td>'
                output+='<td><img src="/static/files/'+img+'" width="200" height="200"></img></td>'
                output+='<td><a href=\'UserMap?t1='+str(row[2])+'\'><font size=3 color=black>View on Map</font></a></td></tr>'       
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'UserMap.html', context)     

def EmployeeMap(request):
    if request.method == 'GET':
        name = request.GET.get('t1', False)
        output = '<iframe width="625" height="650" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q='+name+'&amp;ie=UTF8&amp;&amp;output=embed"></iframe><br/>'
        context= {'data':output}
        return render(request, 'EmployeeMap.html', context)

def ViewCurrentStatusAction(request):
    if request.method == 'POST':
        global uname
        pid = request.POST.get('t1', False)
        emp,sender,sender_phone,receiver,amount,delivery,img = getDetails(pid)
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Collected Employee</th><th><font size="" color="black">Sender Name</th>'
        output+='<th><font size="" color="black">Sender Phone</th><th><font size="" color="black">Receiver Name</th>'
        output+='<th><font size="" color="black">Amount</th><th><font size="" color="black">Expected Delivery</th>'
        output+='<th><font size="" color="black">Current Location</th>'
        output+='<th><font size="" color="black">Updated Date</th><th><font size="" color="black">Status</th>'
        output += '<th><font size="" color="black">Parcel Image</th><th><font size="" color="black">View on Map</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM update_status where parcel_id = '"+pid+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<td><font size="" color="black">'+emp+'</td><td><font size="" color="black">'+sender+'</td>'
                output+='<td><font size="" color="black">'+sender_phone+'</td><td><font size="" color="black">'+receiver+'</td>'
                output+='<td><font size="" color="black">'+amount+'</td><td><font size="" color="black">'+delivery+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td>'
                output+='<td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td>'
                output+='<td><img src="/static/files/'+img+'" width="200" height="200"></img></td>'
                output+='<td><a href=\'EmployeeMap?t1='+str(row[2])+'\'><font size=3 color=black>View on Map</font></a></td></tr>'       
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'EmployeeScreen.html', context)  
        

def ViewCurrentStatus(request):
    if request.method == 'GET':
        output = '<tr><td><font size='' color="black"><b>Courier&nbsp;ID</b></td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select parcel_id FROM parcel")
            rows = cur.fetchall()
            for row in rows:
                pid = str(row[0])
                output += '<option value="'+str(pid)+'">'+str(pid)+'</option>'
        context= {'data1': output}
        return render(request, 'ViewCurrentStatus.html', context)

def checkStatus(pid):
    status = False
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM update_status where status = 'Delivered' and parcel_id='"+pid+"'")
        rows = cur.fetchall()
        for row in rows:
            status = True
            break
    return status

def UpdateCourier(request):
    if request.method == 'GET':
        output = '<tr><td><font size='' color="black"><b>Courier&nbsp;ID</b></td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select parcel_id FROM parcel")
            rows = cur.fetchall()
            for row in rows:
                pid = str(row[0])
                status = checkStatus(pid)
                if status == False:
                    output += '<option value="'+str(pid)+'">'+str(pid)+'</option>'
        context= {'data1': output}
        return render(request, 'UpdateCourier.html', context)

def UpdateCourierAction(request):
    if request.method == 'POST':
        global uname
        pid = request.POST.get('t1', False)
        location = request.POST.get('t2', False)
        status = request.POST.get('t3', False)
        today = str(date.today())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO update_status(parcel_id,employee_reporting,current_location,update_date,status) VALUES('"+str(pid)+"','"+uname+"','"+location+"','"+str(today)+"','"+status+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Courier status updated successfully"
        context= {'data': status}
        return render(request, 'EmployeeScreen.html', context)    

def Feedback(request):
    if request.method == 'GET':
       return render(request, 'Feedback.html', {})

def FeedbackAction(request):
    if request.method == 'POST':
        global uname
        pid = request.POST.get('t1', False)
        feedback = request.POST.get('t2', False)
        rating = request.POST.get('t3', False)
        today = str(date.today())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO feedback(username,feedback,feedback_date,feedback_rank) VALUES('"+str(pid)+"','"+feedback+"','"+str(today)+"','"+rating+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Your Feedback Accepted. Our Admin will review"
        context= {'data': status}
        return render(request, 'Feedback.html', context)     

def CollectCourierAction(request):
    if request.method == 'POST':
        global uname
        sender = request.POST.get('t1', False)
        sender_phone = request.POST.get('t2', False)
        sender_address = request.POST.get('t3', False)
        receiver = request.POST.get('t4', False)
        receiver_phone = request.POST.get('t5', False)
        receiver_address = request.POST.get('t6', False)
        desc = request.POST.get('t7', False)
        weight = request.POST.get('t8', False)
        amount = request.POST.get('t9', False)
        delivery = request.POST.get('t10', False)
        image = request.FILES['t11']
        imagename = request.FILES['t11'].name
        status = "none"
        pid = 1
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(parcel_id) FROM parcel")
            rows = cur.fetchall()
            for row in rows:
                pid = row[0]
        if pid is not None:
            pid += 1
        else:
            pid = 1
        today = str(date.today())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO parcel(parcel_id,collected_employee,sender_name,sender_phone,sender_address,receiver_name,receiver_phone,receiver_address,description,parcel_weight,amount,collected_date,expected_delivery,parcel_image) VALUES('"+str(pid)+"','"+uname+"','"+sender+"','"+sender_phone+"','"+sender_address+"','"+receiver+"','"+receiver_phone+"','"+receiver_address+"','"+desc+"','"+weight+"','"+amount+"','"+str(today)+"','"+delivery+"','"+imagename+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            fs = FileSystemStorage()
            if os.path.exists('CourierApp/static/files/'+imagename):
                os.remove('CourierApp/static/files/'+imagename)
            filename = fs.save('CourierApp/static/files/'+imagename, image)
            status = "Courier details added<br/>Courier Tracking ID : "+str(pid)
        context= {'data': status}
        return render(request, 'CollectCourier.html', context)

def CollectCourier(request):
    if request.method == 'GET':
       return render(request, 'CollectCourier.html', {})    

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    

def EmployeeLogin(request):
    if request.method == 'GET':
       return render(request, 'EmployeeLogin.html', {})

def CourierTrack(request):
    if request.method == 'GET':
       return render(request, 'CourierTrack.html', {})

def AddEmployee(request):
    if request.method == 'GET':
       return render(request, 'AddEmployee.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'AdminLogin.html', context)

def EmployeeLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM employee")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'EmployeeScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'EmployeeLogin.html', context)        
    

def AddEmployeeAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        gender = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        qualification = request.POST.get('t5', False)
        experience = request.POST.get('t6', False)
        address = request.POST.get('t7', False)
        username = request.POST.get('t8', False)
        password = request.POST.get('t9', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM employee")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO employee(employee_name,gender,contact_no,email,qualification,experience,address,username,password) VALUES('"+name+"','"+gender+"','"+contact+"','"+email+"','"+qualification+"','"+experience+"','"+address+"','"+username+"','"+password+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Employee details added<br/>Employee can login with "+username
        context= {'data': status}
        return render(request, 'AddEmployee.html', context)

def ViewEmployees(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Employee Name</th><th><font size="" color="black">Gender</th>'
        output+='<th><font size="" color="black">Contact No</th><th><font size="" color="black">Email ID</th>'
        output+='<th><font size="" color="black">Qualification</th><th><font size="" color="black">Experience</th>'
        output+='<th><font size="" color="black">Address</th>'
        output+='<th><font size="" color="black">Username</th><th><font size="" color="black">Password</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from employee")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td><td><font size="" color="black">'+row[5]+'</td>'
                output+='<td><font size="" color="black">'+row[6]+'</td>'
                output+='<td><font size="" color="black">'+row[7]+'</td>'
                output+='<td><font size="" color="black">'+row[8]+'</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)

def ViewCouriers(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Parcel ID</th><th><font size="" color="black">Collected Employee</th>'
        output+='<th><font size="" color="black">Sender Name</th><th><font size="" color="black">Sender Phone</th>'
        output+='<th><font size="" color="black">Receiver Name</th><th><font size="" color="black">Receiver Phone</th>'
        output+='<th><font size="" color="black">Description</th>'
        output+='<th><font size="" color="black">Amount</th><th><font size="" color="black">Collected Date</th>'
        output += '<th><font size="" color="black">Expected Delivery</th><th><font size="" color="black">Parcel Image</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mysql', database = 'courier',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from parcel")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="" color="black">'+str(row[0])+'</td><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[5]+'</td><td><font size="" color="black">'+row[6]+'</td>'
                output+='<td><font size="" color="black">'+row[8]+'</td>'
                output+='<td><font size="" color="black">'+row[10]+'</td><td><font size="" color="black">'+row[11]+'</td>'
                output+='<td><font size="" color="black">'+row[12]+'</td>'
                output+='<td><img src="/static/files/'+row[13]+'" width="200" height="200"></img></td></tr>'             
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)    

