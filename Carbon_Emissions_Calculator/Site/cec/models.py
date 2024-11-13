import django
from django.db import models
import datetime

# Create your models here.
trans_choice = [
    ("Plane","Plane"),
    ("Train","Train"),
    ("Other","Other")
]

houses = [
    ('Bari', 'Bari'),
    ('Ikhaya', 'Ikhaya'),
    ('Ruka', 'Ruka'),
    ('Meraki', 'Meraki'),
    ('Baile', 'Baile'),
    ('Hogan', 'Hogan'),
    ('Heimat', 'Heimat'),
    ('Bandele', 'Bandele'),
    ('Bayt', 'Bayt'),
    ('Efie', 'Efie'),
    ('Ohana', 'Ohana'),
    ('Other', 'Other'),
]

class Airport(models.Model):
    iata = models.CharField(max_length=3)  
    icao = models.CharField(max_length=4)
    name = models.CharField(max_length=500)
    
    @property
    def output(self):
        return f"{self.iata}/{self.icao} - {self.name}"
    
class TrainStation(models.Model):
    name = models.CharField(max_length=500)

class Survey(models.Model):
    title = models.CharField(max_length=200)
    opening = models.DateField(default = datetime.date(2024,1,1))
    deadline = models.DateField(default = datetime.date(2099,12,31))
 
    def __str__(self):
        return self.title
    
    @property 
    def status(self):
        days_remaining = (self.deadline-datetime.datetime.now().date()).days
        duration = (self.deadline-self.opening).days
        if days_remaining < 0 or days_remaining > duration:
            return "Disabled"
        elif days_remaining == duration:
            return "Open"
        elif days_remaining == 10:
            return "Comfortable"
        elif days_remaining == 5:
            return "Nudge"
        elif days_remaining == 3:
            return "Notify"
        elif days_remaining == 1:
            return "Urge"
        elif days_remaining == 0:
            return "Alert"



class Entry(models.Model):
    house = models.CharField(choices=houses,max_length=200,default="None")
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cohort = models.CharField(max_length=10)
    transportation = models.CharField(choices=trans_choice,null=True, blank=True,max_length=20)
    start = models.CharField(max_length=1000)
    end = models.CharField(max_length=1000)
    identification = models.CharField(max_length=10)
    carbon_emissions = models.FloatField(default=-1)
    further_review = models.BooleanField(default=False)

    def to_str(self):
        return self.identification
    
    def set_start(self,INPUT):
        self.start=INPUT

class OperatorEntry(models.Model):
    file = models.FileField(upload_to="excel")

class OperatorReport(models.Model):
    Month_Text = models.CharField(max_length=3,default="Jan")
    Month = models.IntegerField(default=1)
    Year = models.IntegerField(default=2001)
    ALL_ELE = models.IntegerField(default=0)
    RES = models.IntegerField(default=0)
    ACA = models.IntegerField(default=0)
    SCI = models.IntegerField(default=0)
    THE = models.IntegerField(default=0)
    GYM = models.IntegerField(default=0)
    RESL = models.IntegerField(default=0)
    ACAL = models.IntegerField(default=0)
    SCIL = models.IntegerField(default=0)
    THEL = models.IntegerField(default=0)
    GYML = models.IntegerField(default=0)
    RESE = models.IntegerField(default=0)
    ACAE = models.IntegerField(default=0)
    SCIE = models.IntegerField(default=0)
    THEE = models.IntegerField(default=0)
    GYME = models.IntegerField(default=0)
    RESA = models.IntegerField(default=0)
    ACAA = models.IntegerField(default=0)
    SCIA = models.IntegerField(default=0)
    THEA = models.IntegerField(default=0)

    @property
    def ELE_SUM(self):
        return round(self.RES+self.ACA+self.SCI+self.THE+self.GYM,2)

    @property
    def L_SUM(self):
        return round(self.RESL+self.ACAL+self.SCIL+self.THEL+self.GYML,2)
    
    @property
    def E_SUM(self):
        return round(self.RESE+self.ACAE+self.SCIE+self.THEE+self.GYME,2)
    
    @property
    def A_SUM(self):
        return round(self.RESA+self.ACAA+self.SCIA+self.THEA,2)
    
    @property
    def ELE_P(self):
        return round(self.ELE_SUM/self.ALL_ELE * 100,2)
    
    @property
    def RES_ELE_P(self):
        return round(self.RES/self.ELE_SUM * 100,2)
    
    @property
    def ACA_ELE_P(self):
        return round(self.ACA/self.ELE_SUM * 100,2)
    
    @property
    def SCI_ELE_P(self):
        return round(self.SCI/self.ELE_SUM * 100,2)
    
    @property
    def THE_ELE_P(self):
        return round(self.THE/self.ELE_SUM * 100,2)
    
    @property
    def GYM_ELE_P(self):
        return round(self.GYM/self.ELE_SUM * 100,2)
    
    @property
    def RES_L_P(self):
        return round(self.RESL/self.L_SUM * 100,2)
    
    @property
    def ACA_L_P(self):
        return round(self.ACAL/self.L_SUM * 100,2)
    
    @property
    def SCI_L_P(self):
        return round(self.SCIL/self.L_SUM * 100,2)
    
    @property
    def THE_L_P(self):
        return round(self.THEL/self.L_SUM * 100,2)
    
    @property
    def GYM_L_P(self):
        return round(self.GYML/self.L_SUM * 100,2)
    
    @property
    def RES_E_P(self):
        return round(self.RESE/self.E_SUM * 100,2)
        
    @property
    def ACA_E_P(self):
        return round(self.ACAE/self.E_SUM * 100,2)
    
    @property
    def SCI_E_P(self):
        return round(self.SCIE/self.E_SUM * 100,2)
    
    @property
    def THE_E_P(self):
        return round(self.THEE/self.E_SUM * 100,2)
    
    @property
    def GYM_E_P(self):
        return round(self.GYME/self.E_SUM * 100,2)
    
    @property
    def RES_A_P(self):
        return round(self.RESA/self.A_SUM * 100,2)
    
    @property
    def ACA_A_P(self):
        return round(self.ACAA/self.A_SUM * 100,2)
    
    @property
    def SCI_A_P(self):
        return round(self.SCIA/self.A_SUM * 100,2)
    
    @property
    def THE_A_P(self):
        return round(self.THEA/self.A_SUM * 100,2)
    
    # @property
    # def HavePrevious(self):
    #     return True if (OperatorReport.objects.filter) else (False)
    




