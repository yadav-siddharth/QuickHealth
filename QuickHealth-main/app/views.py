from email import message
from importlib import import_module
from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from email.mime import audio
import speech_recognition as sr

# Create your views here.

def IndexView(request):
    return render(request,"app/index.html")

def DoctorView(request):
    return render(request,"app/doc_details.html")

def WalletView(request):
    return render(request,"app/wallet.html")

def BalanceView(request):
    if request.method == "POST":
        u_name = request.POST['p_uname']
        user = Patient.objects.get(Username=u_name)
        bal = "₹"+str(user.Wallet)
        return render(request,"app/wallet.html",{'bal':bal})

def Addmoney(request):
    if request.method == "POST":
        money = request.POST['paisa']
        u_name = request.POST['p_uname']
        
        user = Patient.objects.get(Username=u_name)
        user.Wallet=int(user.Wallet)+int(money)
        user.save()
    
        message = "Money successfully added."
        return render(request,"app/wallet.html",{'msg':message})

def DoctorPage(request):
    return render(request,"app/doctor_page.html")


def Signup(request):
    return render (request,"app/signup_login.html")

def Appointpage (request):
    return render (request,"app/appointment.html")

def Mainpage (request):
    return render (request,"app/main_page.html")


def Book(request):
    if request.method == "POST":
        username = request.POST['username']
        user = Doctor.objects.get(Username=username)
        u_name = username
        full_name = user.Firstname + " " + user.Lastname
        sp = user.Speciality
        fees = user.C_fees
        slot = user.Slots.split(",")
        print(len(slot))

        if(len(slot)==1):
            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'count':len(slot)})
        elif(len(slot)==2):
            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'count':len(slot)})
        elif(len(slot)==3):
            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'count':len(slot)})
        elif(len(slot)==4):
            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'slot3':slot[3],'count':len(slot)})
  
def Record (request):
    
    if request.method == "POST":
        #recognizer = sr.Recognizer
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 0.5
        mic = sr.Microphone()

        with mic as source:
            print("Say something\n")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            recognizer.dynamic_energy_threshold = True
            print("Ready to record\n")
            audio = recognizer.listen(source)
            print("Audio captured\n")
        try:
            searched = recognizer.recognize_google(audio).lower()
            print(searched)
            doct=Doctor.objects.filter(Speciality__contains=searched)
            
            if doct:
                message = searched
                return render (request,"app/appointment.html",{'searched':searched,'doct':doct,'msg':message})
            else:
                message = "No Doctors Found.."
                return render (request,"app/appointment.html",{'msg2':message})
        except sr.UnknownValueError:
            message = "No Doctors Found.."
            return render (request,"app/appointment.html",{'msg2':message})
        except sr.RequestError:
            message = "No Doctors Found.."
            return render (request,"app/appointment.html",{'msg2':message})
        

def Searchpage (request):
    if request.method == "POST":
        searched=request.POST['searched'].lower()
        doct=Doctor.objects.filter(Speciality__contains=searched)
        
    if doct:
        message = searched
        return render (request,"app/appointment.html",{'searched':searched,'doct':doct,'msg':message})
    else:
        message = "No Doctors Found.."
        return render (request,"app/appointment.html",{'msg2':message})

def InsertData(request):
                if request.method == "POST" :  
                    username=request.POST['username']
                    password=request.POST['password'] 
                    fname=request.POST['fname']
                    lname=request.POST['lname']
                    email=request.POST['email']
                    contact=request.POST['contact']
                    category=request.POST['category']
                    speciality=request.POST['speciality'].lower()

                    if category == 'patient':
                        user=Patient.objects.filter(Username=username)
                   
                        if user:
                            message="User already exists"
                            return render (request,"app/signup_login.html",{'msg':message})
                        
                        elif category == 'patient':
                            wallet=0
                            default=""
                            newuser = Patient.objects.create(Username=username,Password=password,Firstname=fname,Lastname=lname,
                                                      Email=email,Contact=contact,Wallet=wallet,Date=default,Time=default,Doctors=default)
                            message="User Successfully Registered"
                            # After inserting data  reneder on login    
                            return render (request,"app/signup_login.html",{'msg1':message})
                
                    if category == 'doctor':
                        user=Doctor.objects.filter(Username=username)
                    
                        if user:
                            message="User already exists"
                            return render (request,"app/signup_login.html",{'msg':message})
                        
                        elif category == 'doctor':
                            default=0
                            slots=""
                            newuser = Doctor.objects.create(Username=username,Password=password,Firstname=fname,Lastname=lname,
                                                      Email=email,Contact=contact,Speciality=speciality,Experience=default,Slots=slots,C_fees=default,Wallet=default)
                            u_name = username
                            # After inserting data  reneder on login    
                            return render (request,"app/doc_details.html",{'u_name':u_name})

    
                        
                        
                     
def Loginpage(request):
               return render(request,"app/signup_login.html")

def LoginUser(request):
                if request.method=="POST":
                    username=request.POST.get('username')
                    password=request.POST.get('password')
                    category=request.POST.get('category')


                    if category == 'patient':
                        usr=Patient.objects.filter(Username=username)

                        if usr:
                            user=Patient.objects.get(Username=username)
                            if user.Password == password:
                                request.session['Username']=user.Username
                                request.session['Firstname']=user.Firstname
                                request.session['Lastname']=user.Lastname
                                request.session['Email']=user.Email
                                request.session['Contact']=user.Contact

                                return render (request,"app/main_page.html")

                            else:
                                message="Incorrect password."
                                return render (request,"app/signup_login.html",{'msg2':message})
                        else:
                            message="Incorrect username."
                            return render(request,"app/signup_login.html",{'msg2':message})
                    
                    elif category == 'doctor':
                        usr=Doctor.objects.filter(Username=username)

                        if usr:
                            user=Doctor.objects.get(Username=username)
                            if user.Password == password:
                                request.session['Username']=user.Username
                                request.session['Firstname']=user.Firstname
                                request.session['Lastname']=user.Lastname
                                request.session['Email']=user.Email
                                request.session['Contact']=user.Contact
                                request.session['Wallet']=user.Wallet

                                user1 = Appointment.objects.filter(DoctorId=username)
                                if user1:
                                    user2 = Appointment.objects.get(DoctorId=username)
                                    in_patients = user2.PatientId
                                    patients = in_patients.split(",")
                                    stu = []
                                    final_dates = []
                                    final_slots = []
                                    for i in range(len(patients)-1):
                                        stu.append(Patient.objects.get(Username=patients[i]))
                                    for i in stu:
                                        in_doctors = i.Doctors
                                        in_dates = i.Date
                                        dates = in_dates.split(",")
                                        in_slots = i.Time
                                        slots = in_slots.split(",")
                                        doctors = in_doctors.split(",")
                                        for j in range(len(doctors)-1):
                                            if(username==doctors[j]):
                                                final_dates.append(dates[j])
                                                final_slots.append(slots[j])
                                    list1 = zip(stu,final_dates,final_slots)    
                                    message = "Appointments"
                                    return render (request,"app/doctor_page.html",{'stu' : list1,'msg':message})
                                else:
                                    message = "No Appointments"
                                    return render (request,"app/doctor_page.html",{'msg':message})
                                    

                            else:
                                message="Incorrect password."
                                return render (request,"app/signup_login.html",{'msg2':message})
                        else:
                            message="Incorrect username."
                            return render(request,"app/signup_login.html",{'msg2':message})
                else:
                    return HttpResponse('Invalid Request')

def doctorFormView(request):
    if request.method == 'POST':
        years = request.POST['years']
        fees = request.POST['fees']
        u_name = request.POST['username']
        slots = request.POST['slots']
        
        user = Doctor.objects.get(Username=u_name)
        user.Experience=years
        user.save()
        user.Slots=slots
        user.save()
        user.C_fees=fees
        user.save()
        
        message="User Successfully Registered"
        return render(request,"app/signup_login.html",{'msg1':message})
        # if request.POST.get('coursename'):
        #     savedata = Doctor()
        #     savedata.ts1 = request.POST.get('coursename')
        #     savedata.save()
        #     # new = DoctInfo.objects.create(exp = years, fees = fees)  #update 
        #     savedata.exp = request.POST.get('years')
        #     savedata.save()
        #     savedata.fees = request.POST.get('fees')
        #     savedata.save()
            

        #     return redirect('doctorForm')
                        
def Selectdoctor(request):
    if request.method=="POST":
        name=request.POST['clicked']
        
        return render(request,"app/book_meet.html",{'name': name})
    
def DeleteData(request, pk):
    if request.method == "POST":
        print(pk)
        d_uname = request.POST['d_uname']
        p_uname = pk
        p_user = Patient.objects.get(Username=p_uname)
        email = p_user.Email
        in_docs = p_user.Doctors
        docs = in_docs.split(",")
        docs.remove(docs[len(docs)-1])
        in_dates = p_user.Date
        dates = in_dates.split(",")
        dates.remove(dates[len(dates)-1])
        in_slots = p_user.Time
        slots = in_slots.split(",")
        slots.remove(slots[len(slots)-1])
        print(docs)
        print(len(docs))
        
        # delete_id = pk + ","
        # delete_date=""
        # delete_slot=""
        
        for i in range(len(docs)):
            if (docs[i]==d_uname):
                # delete_date=dates[i] + ","
                # delete_slot=slots[i] + ","
                docs.pop(i)
                dates.pop(i)
                slots.pop(i)
                break
        
        for i in range(len(docs)):
            docs[i]=docs[i]+","  
            dates[i]=dates[i]+","
            slots[i]=slots[i]+","
        
        new_docs=""  
        new_docs = new_docs.join(docs)
        new_dates=""
        new_dates = new_dates.join(dates)
        new_slots=""
        new_slots = new_slots.join(slots)
        
        p_user.Doctors = new_docs
        p_user.Date = new_dates
        p_user.Time = new_slots
        
        ap_user = Appointment.objects.get(DoctorId=d_uname)
        ap_patient_ids = ap_user.PatientId
        a_ids = ap_patient_ids.split(",")
        a_ids.remove(a_ids[len(a_ids)-1])
        ap_dates = ap_user.Dates
        a_dates = ap_dates.split(",")
        a_dates.remove(a_dates[len(a_dates)-1])
        ap_slots = ap_user.Slots
        a_slots = ap_slots.split(",")
        a_slots.remove(a_slots[len(a_slots)-1])
        
        for i in range(len(a_ids)):
            if(a_ids[i]==p_uname):
                a_ids.pop(i)
                a_dates.pop(i)
                a_slots.pop(i)
                break
                
        for i in range(len(a_ids)):
            a_ids[i]=a_ids[i]+","
            a_dates[i]=a_dates[i]+","
            a_slots[i]=a_slots[i]+","
        
        new_patient_ids=""  
        new_patient_ids = new_patient_ids.join(a_ids)
        new_ap_dates=""
        new_ap_dates = new_ap_dates.join(a_dates)
        new_ap_slots=""
        new_ap_slots = new_ap_slots.join(a_slots)
        
        # new_patient_ids = ap_patient_ids.replace(delete_id,"")
        # new_ap_dates = ap_dates.replace(delete_date,"")
        # new_ap_slots = ap_slots.replace(delete_slot,"")
        ap_user.PatientId = new_patient_ids
        ap_user.Dates = new_ap_dates
        ap_user.Slots = new_ap_slots
        ap_user.save()
        p_user.save()
        
        # return render(request, "app/table.html")
    
        send_mail(
                'QuickHealth',
                'Sorry sir, your appointment with the doctor has been cancelled.\nYou can reschedule it later.',
                'abhishekshirke502@gmail.com',
                [email,],
                fail_silently = False,
            )
        user2 = Appointment.objects.get(DoctorId=d_uname)
        if (user2.PatientId != ""):
            user2 = Appointment.objects.get(DoctorId=d_uname)
            inn_patients = user2.PatientId
            patients = inn_patients.split(",")
            stu = []
            final_dates = []
            final_slots = []
            for i in range(len(patients)-1):
                stu.append(Patient.objects.get(Username=patients[i]))
            for i in stu:
                in_doctors = i.Doctors
                inn_dates = i.Date
                ddates = inn_dates.split(",")
                in_slots = i.Time
                sslots = in_slots.split(",")
                doctors = in_doctors.split(",")
                for j in range(len(doctors)-1):
                    if(d_uname==doctors[j]):
                        final_dates.append(ddates[j])
                        final_slots.append(sslots[j])
            list1 = zip(stu,final_dates,final_slots)    
            message = "Appointments"
            return render (request,"app/doctor_page.html",{'stu' : list1,'msg':message})
        else:
            message = "No Appointments"
            return render (request,"app/doctor_page.html",{'msg':message})
    else:
        return HttpResponse('Invalid Request')

def send_email(request):
    return render(request, 'app/send_email.html')

def SendEmail(request):
    if request.method == 'POST':
        d_uname = request.POST['d_uname']
        p_uname = request.POST['p_uname']
        date = request.POST['inputDate']
        slot = request.POST['slots']
        inputEmail = request.POST['inputEmail']
        user = Appointment.objects.filter(DoctorId=d_uname)
        link = "https://us04web.zoom.us/j/73698392345?pwd=b2mkmPEvhyL9j5X6_HorkI-rJ4aKSP.1"
        
        # if((d_uname=="adifaze") and (date=="2022-05-13") and (slot=="10:00-10:30 AM")):
        #     link = "https://us04web.zoom.us/j/76027597976?pwd=iFnn8qvz0-U8zpW9pZTjy5RMUbDDOb.1"
        # elif((d_uname=="adifaze") and (date=="2022-05-22") and (slot=="3:00-3:30 AM")):
        #     link = "https://us04web.zoom.us/j/78067989834?pwd=RB6RzePOlv64mLTilI_PLay4JwwFAx.1"
                
        if user:
            user1 = Appointment.objects.get(DoctorId=d_uname)
            in_dates = user1.Dates
            dates = in_dates.split(",")
            in_slots = user1.Slots
            slots = in_slots.split(",")
            patients = user1.PatientId
            p = patients.split(",")
            flag1=0
            flag2=0
            
            user4 = Doctor.objects.get(Username=d_uname)
            user2 = Patient.objects.get(Username=p_uname)
            for i in p:
                if(p_uname==i):
                    u_name = d_uname
                    full_name = user4.Firstname + " " + user4.Lastname
                    sp = user4.Speciality
                    fees = user4.C_fees
                    slot = user4.Slots.split(",")
                    message = "You have already booked an appointment with this doctor."
                    print(len(slot))

                    if(len(slot)==1):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'count':len(slot),'bal':message})
                    elif(len(slot)==2):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'count':len(slot),'bal':message})
                    elif(len(slot)==3):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'count':len(slot),'bal':message})
                    elif(len(slot)==4):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'slot3':slot[3],'count':len(slot),'bal':message})
            
            for i in range(len(dates)):
                if(dates[i]==date):
                    flag1=1
            if(flag1==1):
                for i in range(len(slots)):
                    if(slots[i]==slot):
                        flag2=1
                if(flag2==1):
                    user4 = Doctor.objects.get(Username=d_uname)
                    u_name = d_uname
                    full_name = user4.Firstname + " " + user4.Lastname
                    sp = user4.Speciality
                    fees = user4.C_fees
                    slot = user4.Slots.split(",")
                    val_slot = "Slot unavailable."
                    if(len(slot)==1):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'count':len(slot),'val_slot':val_slot})
                    elif(len(slot)==2):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'count':len(slot),'val_slot':val_slot})
                    elif(len(slot)==3):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'count':len(slot),'val_slot':val_slot})
                    elif(len(slot)==4):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'slot3':slot[3],'count':len(slot),'val_slot':val_slot})
                elif(flag2==0):  
                    user4 = Doctor.objects.get(Username=d_uname)
                    user2 = Patient.objects.get(Username=p_uname)
                            
                    if(int(user2.Wallet)<int(user4.C_fees)):
                        u_name = d_uname
                        full_name = user4.Firstname + " " + user4.Lastname
                        sp = user4.Speciality
                        fees = user4.C_fees
                        slot = user4.Slots.split(",")
                        message = "Insufficient balance."
                        print(len(slot))

                        if(len(slot)==1):
                            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'count':len(slot),'bal':message})
                        elif(len(slot)==2):
                            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'count':len(slot),'bal':message})
                        elif(len(slot)==3):
                            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'count':len(slot),'bal':message})
                        elif(len(slot)==4):
                            return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'slot3':slot[3],'count':len(slot),'bal':message})
                    else:
                        user2.Wallet=int(user2.Wallet)-int(user4.C_fees)
                        user4.Wallet=int(user4.Wallet)+int(user4.C_fees)
                        user2.Date = user2.Date+date+","
                        user2.Time = user2.Time+slot+","
                        user2.Doctors = user2.Doctors+d_uname+","
                        user2.save()
                        user4.save()
                                
                        user1.Dates = in_dates+date+","
                        user1.Slots = in_slots+slot+","
                        user1.PatientId = patients+p_uname+","
                        user1.save()

                        inputEmail = request.POST['inputEmail']
                        name = request.POST['f_name']
                        full_dname = user4.Firstname + " " + user4.Lastname
                        sp = user4.Speciality
                        
                        d_email = user4.Email
                        full_pname = user2.Firstname + " " + user2.Lastname
                        # print(name, subjects, messages)

                        send_mail(
                        subject='Meeting Details',
                        # message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details:\nDoctor Name: {full_dname}\nSpeciality: {sp}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                        message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details:\nDoctor Name: {full_dname}\nSpeciality: {sp}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: {link}',
                        # 'abhishekshirke502@gmail.com',
                        # ['abhishekshirke263@gmail.com']
                        from_email= 'abhishekshirke502@gmail.com',
                        # recipient_list= ['abhishekshirke263@gmail.com'],
                        recipient_list= [inputEmail, ],
                        fail_silently=False,
                        )
                        
                        send_mail(
                        subject='Meeting Details',
                        # message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details of your patient:\nPatient Name: {full_pname}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                        message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details of your patient:\nPatient Name: {full_pname}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: {link}',
                        # 'abhishekshirke502@gmail.com',
                        # ['abhishekshirke263@gmail.com']
                        from_email= 'abhishekshirke502@gmail.com',
                        # recipient_list= ['abhishekshirke263@gmail.com'],
                        recipient_list= [d_email, ],
                        fail_silently=False,
                        )
    
                        return render(request, 'app/send_email.html')
                        # return HttpResponseRedirect(reverse('send_email'))
            elif(flag1==0):
                user4 = Doctor.objects.get(Username=d_uname)
                user2 = Patient.objects.get(Username=p_uname)
                            
                if(int(user2.Wallet)<int(user4.C_fees)):
                    u_name = d_uname
                    full_name = user4.Firstname + " " + user4.Lastname
                    sp = user4.Speciality
                    fees = user4.C_fees
                    slot = user4.Slots.split(",")
                    message = "Insufficient balance."
                    print(len(slot))

                    if(len(slot)==1):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'count':len(slot),'bal':message})
                    elif(len(slot)==2):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'count':len(slot),'bal':message})
                    elif(len(slot)==3):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'count':len(slot),'bal':message})
                    elif(len(slot)==4):
                        return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'slot3':slot[3],'count':len(slot),'bal':message})
                else:
                    user2.Wallet=int(user2.Wallet)-int(user4.C_fees)
                    user4.Wallet=int(user4.Wallet)+int(user4.C_fees)
                    user2.Date = user2.Date + date + ","
                    user2.Time = user2.Time + slot + ","
                    user2.Doctors = user2.Doctors + d_uname + ","
                    user2.save()
                    user4.save()
                                
                    user1.Dates = in_dates+date+","
                    user1.Slots = in_slots+slot+","
                    user1.PatientId = patients+p_uname+","
                    user1.save()
                            
                    inputEmail = request.POST['inputEmail']
                    name = request.POST['f_name']
                    full_dname = user4.Firstname + " " + user4.Lastname
                    sp = user4.Speciality
                    
                    d_email = user4.Email
                    full_pname = user2.Firstname + " " + user2.Lastname
                    # print(name, subjects, messages)

                    send_mail(
                    subject='Meeting Details',
                    # message=f'Greetings from QuickHealth, {name} \n Meeting Date: {date} \n Meeting Time: {slot} \n Zoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                    # message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details:\nDoctor Name: {full_dname}\nSpeciality: {sp}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                     message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details:\nDoctor Name: {full_dname}\nSpeciality: {sp}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                    # 'abhishekshirke502@gmail.com',
                    # ['abhishekshirke263@gmail.com']
                    from_email= 'abhishekshirke502@gmail.com',
                    # recipient_list= ['abhishekshirke263@gmail.com'],
                    recipient_list= [inputEmail, ],
                    fail_silently=False,
                    )
                    
                    send_mail(
                    subject='Meeting Details',
                    # message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details of your patient:\nPatient Name: {full_pname}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                    message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details of your patient:\nPatient Name: {full_pname}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/73698392345?pwd=b2mkmPEvhyL9j5X6_HorkI-rJ4aKSP.1',
                    # 'abhishekshirke502@gmail.com',
                    # ['abhishekshirke263@gmail.com']
                    from_email= 'abhishekshirke502@gmail.com',
                    # recipient_list= ['abhishekshirke263@gmail.com'],
                    recipient_list= [d_email, ],
                    fail_silently=False,
                    )
    
                    return render(request, 'app/send_email.html')
                    # return HttpResponseRedirect(reverse('send_email'))
        else:
            user4 = Doctor.objects.get(Username=d_uname)
            user2 = Patient.objects.get(Username=p_uname)
                            
            if(int(user2.Wallet)<int(user4.C_fees)):
                u_name = d_uname
                full_name = user4.Firstname + " " + user4.Lastname
                sp = user4.Speciality
                fees = user4.C_fees
                slot = user4.Slots.split(",")
                message = "Insufficient balance."
                print(len(slot))

                if(len(slot)==1):
                    return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'count':len(slot),'bal':message})
                elif(len(slot)==2):
                    return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'count':len(slot),'bal':message})
                elif(len(slot)==3):
                    return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'count':len(slot),'bal':message})
                elif(len(slot)==4):
                    return render (request,"app/book_meet2.html",{'u_name':u_name,'full_name':full_name,'sp':sp,'fees':fees,'slot0':slot[0],'slot1':slot[1],'slot2':slot[2],'slot3':slot[3],'count':len(slot),'bal':message})
            else:
                user2.Wallet=int(user2.Wallet)-int(user4.C_fees)
                user4.Wallet=int(user4.Wallet)+int(user4.C_fees)
                user2.Date = user2.Date + date+","
                user2.Time = user2.Time + slot+","
                user2.Doctors = user2.Doctors + d_uname + ","
                user2.save()
                user4.save()
                
                new_date=date+","
                new_slot=slot+","
                new_patient=p_uname+","
                new_user=Appointment.objects.create(DoctorId=d_uname,PatientId=new_patient,Dates=new_date,Slots=new_slot)
                            
                inputEmail = request.POST['inputEmail']
                name = request.POST['f_name']
                full_dname = user4.Firstname + " " + user4.Lastname
                sp = user4.Speciality
                
                d_email = user4.Email
                full_pname = user2.Firstname + " " + user2.Lastname
                # print(name, subjects, messages)

                send_mail(
                subject='Meeting Details',
                # message=f'Greetings from QuickHealth, {name} \n Meeting Date: {date} \n Meeting Time: {slot} \n Zoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                # message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details:\nDoctor Name: {full_dname}\nSpeciality: {sp}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details:\nDoctor Name: {full_dname}\nSpeciality: {sp}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: {link}',
                # 'abhishekshirke502@gmail.com',
                # ['abhishekshirke263@gmail.com']
                from_email= 'abhishekshirke502@gmail.com',
                # recipient_list= ['abhishekshirke263@gmail.com'],
                recipient_list= [inputEmail, ],
                fail_silently=False,
                )
                
                send_mail(
                subject='Hello',
                # message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details of your patient:\nPatient Name: {full_pname}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: https://us04web.zoom.us/j/79700775470?pwd=1qG_SUadnZ_HXbjJ55The_u9hk9ulp.1',
                message=f'Greetings from QuickHealth, {name}\n\nThe following are the appointment details of your patient:\nPatient Name: {full_pname}\nMeeting Date: {date}\nMeeting Time: {slot}\nZoom link: {link}',
                # 'abhishekshirke502@gmail.com',
                # ['abhishekshirke263@gmail.com']
                from_email= 'abhishekshirke502@gmail.com',
                # recipient_list= ['abhishekshirke263@gmail.com'],
                recipient_list= [d_email, ],
                fail_silently=False,
                )
    
                return render(request, 'app/send_email.html')
                # return HttpResponseRedirect(reverse('send_email'))
    else:
        return HttpResponse('Invalid Request')
        # link = request.POST['link']

        # newuser = Patient.objects.create(Firstname = names, Email = inputEmail, Contact = phone, Date = date, Time = time)

        #  return render(request, "app/table.html")  