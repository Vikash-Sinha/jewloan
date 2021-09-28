from django.db import models

class SerialNo(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class PrrodcutMaster(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class LoanInfo(models.Model):
    sr_no = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    product_id = models.ForeignKey(PrrodcutMaster, null=True, blank=True, on_delete=models.CASCADE, related_name="product")
    weight = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    loan_amount = models.FloatField(blank=True, null=True)
    rate_of_interest = models.FloatField(blank=True, null=True)
    exit_date = models.DateTimeField(blank=True, null=True)
    interest_per_day = models.FloatField(blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    added_by = models.IntegerField(null=True, default=1)
    updated_by = models.IntegerField(null=True, blank=True, default=None)

    def __int__(self):
        return self.id


class LoanDetail(models.Model):
     LoanID = models.ForeignKey(LoanInfo,null=True,blank=True, on_delete=models.CASCADE, related_name="loan")
     Notes = models.TextField(max_length=200, blank=True,null=True)
     TodayRate = models.FloatField(blank=True,null=True)
     UpdateRate = models.FloatField(blank=True,null=True)
     TodayDate = models.DateTimeField(auto_now_add=True)
     IsonRisk = models.CharField(max_length=100,blank=True,null=True,default=False)
     Active = models.BooleanField(default=False)
