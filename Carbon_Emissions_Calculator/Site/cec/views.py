from django.shortcuts import render, redirect
from django.http import HttpResponse
from .calculator import SARCEC
from .models import Survey, Entry, Airport, TrainStation, OperatorEntry, OperatorReport
from .forms import NewPlaneEntry,NewTrainEntry,NewOtherEntry, NoneSurvey, ModifyEntry, DeleteEntry, ChangeUserAttributes, CarbonCalculator, AddSurvey, DeleteSurvey, OrganizeEntries, ChangeSurvey
from register.models import User
import register.views as v
from register.forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
import openpyxl
import pandas as pd

# Create your views here.
def home(response):
    messages = []
    for S in Survey.objects.all():
        status = S.status
        responses = len(Entry.objects.filter(survey=S,name=response.user))
        if responses == 0 and status != "Disabled":
            message = ["Survey \""+S.title+"\" have "+str((S.deadline-datetime.datetime.now().date()).days)+" days remaining before closing",status]
            if status == "Urge":
                message = ["Survey \""+S.title+"\" have "+str((S.deadline-datetime.datetime.now().date()).days)+" day remaining before closing",status]
            messages.append(message)
    return render(response,"cec/home.html",{"messages":messages, "user":response.user}) 

def login_success(response):
    return render(response, "cec/login_success.html")

def logout_success(response):
    logout(response)
    return redirect('/carbon_emissions_calculator/home/')

def display_entry(response,title,id):
    this_entry = Survey.objects.get(title=title).entry_set.get(id=id)
    survey = Survey.objects.get(title=title).title
    return render(response, "cec/entry.html", 
                  {"s":this_entry,"n":survey})

def display_survey(response,title):
    survey = Survey.objects.get(title=title).entry_set.filter(name=response.user)
    return render(response, "cec/survey.html", 
             {"title":title,"ls":survey,"current_username":response.user, "survey_name":title,"length":len(survey)})

def survey_report(response,title):
    survey = Survey.objects.get(title=title)
    entries = survey.entry_set.all()
    houses = ["Bari","Ikhaya","Ruka","Meraki","Baile","Hogan","Heimat","Bandele","Bayt","Efie","Ohana","Other"]
    indices = [0,1,2,3,4,5,6,7,8,9,10]
    house_users = [0,0,0,0,0,0,0,0,0,0,0,0]
    response_users = [0,0,0,0,0,0,0,0,0,0,0,0]
    entry_subsets = []
    for house in houses:
        entry_subsets.append(entries.filter())
    users = []
    cohorts = []
    transportations = []
    emission_sum = 0
    reviews = 0
    for entry in entries:
        users.append(User.objects.get(username=entry.name).username)
        cohorts.append(entry.cohort)
        transportations.append(entry.transportation)
        if entry.carbon_emissions != -1:
            emission_sum += entry.carbon_emissions
        else:
            reviews += 1
    users = list(set(users))
    cohort_percentage=[round(100*cohorts.count("FP")/len(cohorts),2),
                       round(100*cohorts.count("DP1")/len(cohorts),2),
                       round(100*cohorts.count("DP2")/len(cohorts),2),
                       round(100*cohorts.count("Faculty")/len(cohorts),2)]
    transportation_percentage=[round(100*transportations.count("Plane")/len(transportations),2),
                       round(100*transportations.count("Train")/len(transportations),2),
                       round(100*transportations.count("Other")/len(transportations),2),
                       round(100*transportations.count("None")/len(transportations),2)]
    responses = len(entries)
    users_responded = len(users)
    response_rate = round(100*users_responded/(len(User.objects.all().filter(account_type="Resident"))+len(User.objects.all().filter(account_type="Administrator"))),2)
    mobility = round(100*(responses-transportations.count("None"))/responses,2)
    emission_pc = round(emission_sum/users_responded,3)
    revrate = 100-round(reviews/responses*100,2)
    return render(response,"cec/survey_report.html",{"title":title,"responses":responses,"users_responded":users_responded,"response_rate":response_rate,"mobility":mobility,"emission_sum":round(emission_sum,3),"emission_pc":emission_pc,"revrate":revrate,"survey":survey,"cohort_percentage":cohort_percentage,"transportation_percentage":transportation_percentage})


def new(response):
    return render(response,"cec/new_entry.html")

def surveys(response):
    list_of_surveys = Survey.objects.all()
    return render(response,"cec/surveys.html",{"list_of_surveys":list_of_surveys})

def admin_entry(response):
    list_of_entries = Entry.objects.all()
    form = OrganizeEntries()
    return render(response,"cec/admin_entry.html",{"list_of_entries":list_of_entries,"form":form})

def admin_survey(response):
    list_of_surveys = Survey.objects.all()
    return render(response,"cec/admin_survey.html",{"list_of_surveys":list_of_surveys})

def admin_user(response):
    list_of_users = User.objects.all()
    return render(response,"cec/admin_user.html",{"list_of_users":list_of_users})

def plane_survey(response):
    form = NewPlaneEntry()
    airports=Airport.objects.all()
    return render(response,"cec/plane_survey.html",{"form":form,"airports":airports})

def train_survey(response):
    form = NewTrainEntry()
    stations=TrainStation.objects.all()
    return render(response,"cec/train_survey.html",{"form":form,"stations":stations})

def none_survey(response):
    form = NoneSurvey()
    return render(response,"cec/none_survey.html",{"form":form})

def none_entry_finish(response):
    if response.method == "POST": 
        form = NoneSurvey(response.POST)
        if form.is_valid():
            n = form.cleaned_data["survey"]
            s = Survey.objects.get(title=n)
            if form.cleaned_data["confirm"] == ["Yes, I confirm"]:
                entry = s.entry_set.create(name=response.user,
                                       house=response.user.house,
                                          cohort=form.cleaned_data["cohort"],
                                          transportation="None",
                                          start="",
                                          end="",
                                          identification="",
                                          carbon_emissions=0,
                                          further_review=False)
                print(entry)
                return redirect("/carbon_emissions_calculator/home/")
            else:
                return redirect("/carbon_emissions_calculator/new_entry/")

    else:
        form = NoneSurvey()
    return(response,"cec/none_survey_finished.html")

def other_survey(response):
    form = NewOtherEntry()
    return render(response,"cec/other_survey.html",{"form":form})

def other_entry_finish(response):    
    if response.method == "POST": 
        form = NewOtherEntry(response.POST)
        print(form.is_valid())
        if form.is_valid():
            n = form.cleaned_data["survey"]
            s = Survey.objects.get(title=n)
            entry = s.entry_set.create(name=response.user,
                                       house=response.user.house,
                                          cohort=form.cleaned_data["cohort"],
                                          transportation="Other",
                                          start="",
                                          end="",
                                          identification=form.cleaned_data['identification'],
                                          carbon_emissions=-1,
                                          further_review=True)
    else:
        form = NewOtherEntry()
    return render(response, "cec/other_entry_finished.html",{"result":SARCEC("Other",[],"None","","")})


def plane_entry_finish(response):
    if response.method == "POST": 
        print("Response:")
        print(response.POST.get('departure'))
        form = NewPlaneEntry(response.POST)
        if form.is_valid():
            result = SARCEC("Plane",[],response.POST.get('departure'),end=response.POST.get('arrival'),identification=form.cleaned_data["identification"])
            n = form.cleaned_data["survey"]
            s = Survey.objects.get(title=n)
            entry = s.entry_set.create(name=response.user,
                                       house=response.user.house,
                                          cohort=form.cleaned_data["cohort"],
                                          transportation="Plane",
                                          start=response.POST.get('departure'),
                                          end=response.POST.get('arrival'),
                                          identification=form.cleaned_data["identification"],
                                          carbon_emissions=result if (type(result) != str) else (-1),
                                          further_review=True if (type(result)==str) else (False))
            review = entry.further_review

    else:
        form = NewPlaneEntry()
    return render(response, "cec/plane_entry_finished.html",{"result":result,"review":review})

def train_entry_finish(response):
    if response.method == "POST": 
        form = NewTrainEntry(response.POST)

        if form.is_valid():
            n = form.cleaned_data["survey"]
            result = SARCEC("Train",[],response.POST.get('departure'),response.POST.get('arrival'),form.cleaned_data["identification"])
            s = Survey.objects.get(title=n)
            entry = s.entry_set.create(name=response.user,
                                       house=response.user.house,
                                          cohort=form.cleaned_data["cohort"],
                                          transportation="Train",
                                          start=response.POST.get('departure'),
                                          end=response.POST.get('arrival'),
                                          identification=form.cleaned_data["identification"],
                                          carbon_emissions=result if (type(result) != str) else (-1),
                                          further_review=True if (type(result)==str) else (False))

    else:
        form = NewTrainEntry()
    return render(response, "cec/train_entry_finished.html",{"result":SARCEC("Train",[],response.POST.get('departure'),response.POST.get('arrival'),form.cleaned_data["identification"])})

def entry_edit(response,id):
    obj = Entry.objects.get(id=id)
    form = CarbonCalculator()
    return render(response,"cec/entry_edit.html",{"id":id,"obj":obj,"form":form})

def entry_edited(response,id):
    if response.method == "POST": 
        form=CarbonCalculator(response.POST)
        if form.is_valid():
            obj=Entry.objects.get(id=id)
            if form.cleaned_data['emission'] == None:
                obj.carbon_emissions=-1 if (type(SARCEC(obj.transportation,[form.cleaned_data['distance'],form.cleaned_data['type']],"","","")) == str) else (SARCEC(obj.transportation,[form.cleaned_data['distance'],form.cleaned_data['type']],"","",""))
            else:
                obj.carbon_emissions = form.cleaned_data['emission']       
            obj.further_review=True if obj.carbon_emissions==-1 else (False)
            obj.save()
            print("modified")
            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_entry/")
    else:
        form = ModifyEntry()
    return render(response, "cec/entry_edited.html")

def entry_delete(response,id):
    obj = Entry.objects.get(id=id)
    form = DeleteEntry()
    return render(response,"cec/entry_delete.html",{"id":id,"obj":obj,"form":form})

def entry_deleted(response,id):
    if response.method == "POST": 
        form=DeleteEntry(response.POST)
        if form.is_valid():
            obj=Entry.objects.get(id=id)
            obj.delete()
            print("deleted")
            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_entry/")
    else:
        form = DeleteEntry()
    return render(response, "cec/entry_edited.html")

def user_change(response,name):
    obj = User.objects.get(username=name)
    form = ChangeUserAttributes()
    return render(response,"cec/user_change.html",{"name":name,"obj":obj,"form":form})

def user_changed(response,name):
    if response.method == "POST": 
        form=ChangeUserAttributes(response.POST)
        response.POST.get("account")
        if form.is_valid():
            obj=User.objects.get(username=name)
            obj.account_type=response.POST.get("account")
            obj.save()
            print("modified")
            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_user/")
    else:
        form = ChangeUserAttributes()
    return render(response, "cec/entry_edited.html")

def add_survey(response):
    form = AddSurvey()
    return render(response, "cec/add_survey.html",{"form":form})

def survey_change(response,title):
    form = ChangeSurvey()
    return render(response, "cec/change_survey.html",{"form":form,"title":title})

def survey_changed(response,title):
    if response.method == "POST": 
        form = ChangeSurvey(response.POST)
        if form.is_valid():
            obj = Survey.objects.get(title=title)
            obj.deadline = form.cleaned_data['deadline']
            obj.opening = form.cleaned_data['opening']
            obj.save()
            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_survey/")
    else:
        form = ChangeSurvey()
    return render(response,"cec/survey_organize_redirect.html")


def survey_added(response):
    if response.method == "POST": 
        form=AddSurvey(response.POST)
        if form.is_valid():
            obj=Survey.objects.create(title=form.cleaned_data['title'],opening=form.cleaned_data['opening'],deadline=form.cleaned_data['deadline'])
            print(form.cleaned_data)
            obj.save()
            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_survey/")
    else:
        form = AddSurvey()
    return render(response, "cec/entry_edited.html")

def delete_survey(response,title):
    obj = Survey.objects.get(title=title)
    form = DeleteSurvey()
    return render(response, "cec/delete_survey.html",{"form":form,"obj":obj})

def survey_deleted(response,title):
    if response.method == "POST": 
        form=DeleteSurvey(response.POST)
        if form.is_valid():
            obj=Survey.objects.get(title=title)
            obj.delete()
            print(Survey)
            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_survey/")
    else:
        form = AddSurvey()
    return render(response, "cec/survey_deleted.html")

def entry_organize_redirect(response):
    if response.method == "POST": 
        form = OrganizeEntries(response.POST)
        if form.is_valid():
            title = form.cleaned_data['survey']
            transportation = form.cleaned_data['transportation']
            review = form.cleaned_data['only_review']
            category = form.cleaned_data['category']
            order = form.cleaned_data['order']

            return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/admin_page/entry_organize/survey="+str(title)+"/transportation="+str(transportation)+"/review="+str(review)+"/category="+str(category)+"/order="+str(order)+"/")
    else:
        form = OrganizeEntries()
    return render(response,"cec/entry_organize_redirect.html")


def entry_organize(response,title,transportation,review,category,order):
    objs = Entry.objects.all()
    form = OrganizeEntries()
    if title != "All":
        objs = objs.filter(survey=Survey.objects.get(title=title))
    if transportation != "All":
        objs = objs.filter(transportation=transportation)
    if review == "True":
        objs=objs.filter(further_review=True)
    keyword = ""
    if category == "Emissions":
        keyword = "carbon_emissions"
    else:
        keyword = "id"
    if order == "Descending":
        keyword = "-" + keyword
    objs = objs.order_by(keyword)
    print(objs)
    return render(response,"cec/entry_organize.html",{"length":len(objs),"objs":objs,"form":form})

def operator_entry(response):
    return render(response,'cec/entry_operator.html')

def operator_entry_submitted(response):
    def find(num1,num2):
        number = "L"+str(num1)+"-"+str(num2)
        return int(df[df[1]==number][2])
    if response.method == "POST":
        workbook = response.FILES['files']
        obj = OperatorEntry.objects.create(file=workbook)
        path = workbook.file
        df = pd.read_excel(path,header=None)
        print("Time:",str(df.iloc[1,2])+" "+str(df.iloc[0,2]))
        code = [None,None,5,5,2,5,0,0,0,1,1,2,5,5,2,1,1,2,2,5,5,5,0,0,0,5,1,5,5,5,5,5,5,5,5,2,5,0,0,5,5,5,5,5,2,5,5,5,1,5,5,5,5,5,5,5,1,1,1,5,5,5,0,0,5,0,0,0,5,0,0,5,1,5,5,5,5,5,5,5,0,5,5,5,5,5,5,5,5,2,5,5,5,1,1,5,5,5,5,5,3,4,5,5,5,4,3,3,5,3,4,5,5,3,5,5,4,5,5,3,3,5,5,5,5,3,5,4,5,5,3,3,5,5,5,4,4,5,5,5,5,4,5,5,5,4,3,5,5,5]
        sums = [0,0,0,0,0,0]
        coefficient = 823.446*pow(0.986415,int(df.iloc[0,2])-2000)/1000
        for row in df.iterrows():
            category = code[row[0]]
            if category == None:
                pass
            elif category == -1:
                sums[0] += coefficient * row[1][2]/3
                sums[1] += coefficient * row[1][2]/3
                sums[2] += coefficient * row[1][2]/3
            else:
                sums[category] += coefficient * row[1][2]
        months = ["Jan","Feb","Mar","Apr",
                  "May","Jun","Jul","Aug",
                  "Sep","Oct","Nov","Dec",]
        OperatorReport.objects.create(
            Month_Text = str(df.iloc[1,2]),
            Month = months.index(str(df.iloc[1,2]))+1,
            Year = int(df.iloc[0,2]),
            ALL_ELE=sum(sums),
            RES=sums[0],
            ACA=sums[1],
            SCI=sums[2],
            THE=sums[3],
            GYM=sums[4],
            RESL=round(coefficient * (find(12,5)+find(12,6)+find(14,4)+find(23,3)+find(23,4)),2),
            ACAL=round(coefficient * (find(12,8)+find(12,9)+find(13,6)+find(22,6)+find(22,7)+find(22,8)),2),
            SCIL=round(coefficient * (find(12,3)+find(13,7)),2),
            THEL=round(coefficient * (find(34,2)+find(34,5)),2),
            GYML=round(coefficient * (find(34,1)+find(34,6)),2),
            RESE=round(coefficient * (find(16,5)+find(16,6)+find(26,3)),2),
            ACAE=round(coefficient * (find(15,2)+find(25,2)),2),
            SCIE=round(coefficient * (find(16,3)),2),
            THEE=round(coefficient * (find(35,1)),2),
            GYME=round(coefficient * (find(44,4)),2),
            RESA=round(coefficient * (find(14,5)+find(23,6)+find(24,3)),2),
            ACAA=round(coefficient * (find(13,5)),2),
            SCIA=round(coefficient * (find(13,1)),2),
            THEA=round(coefficient * (find(33,1)),2)
        )
        return render(response,'cec/entry_operator_submitted.html')

def operation_reports(response):
    reports = OperatorReport.objects.all()

    return render(response,'cec/operation_reports.html',{"reports":reports})

def view_operation_report(response,year,month):
    report = OperatorReport.objects.filter(Year=year,Month=month)[0]
    print(report)
    return render(response,'cec/operation_report.html',{"report":report})

