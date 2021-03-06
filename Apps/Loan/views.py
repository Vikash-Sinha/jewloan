from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.http import JsonResponse
# import datetime
from datetime import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#   *** input date format yyyy-mm-dd
def str_to_date(dates):
    dates = dates.split('-')
    year = dates[0]
    month = dates[1]
    dates = dates[2]
    new_date = datetime(int(year),int(month),int(dates))
    return new_date


def riskUpdate(request,id):
    # import pdb
    # pdb.set_trace()
    wt = request.POST.get('wt')
    tr = request.POST.get('tr')
    tAmt = request.POST.get('today_approve_amount')
    pAmt = request.POST.get('past_approve_amount')
    loan_detail_obj = LoanDetail.objects.get(id=id)
    today_value_till_date = 0
    if loan_detail_obj.UpdateRate:
        today_value_till_date = float(loan_detail_obj.LoanID.weight) * float(loan_detail_obj.UpdateRate)
    ed1 = LoanInfo.objects.get(id=loan_detail_obj.LoanID)
    # Grand Amount Calculation
    si, grand = grandAmountCal(ed1)
    risk = ""
    # if float(tAmt) < float(pAmt):
    # if float(tAmt) < float(pAmt) or grand > today_value_till_date:
    if grand > today_value_till_date and today_value_till_date is not 0:
        loan_detail_obj.IsonRisk = True
        loan_detail_obj.UpdateRate=tr
        risk = "In Risk Now"
    else:
        loan_detail_obj.IsonRisk = False
        risk = "Not In Risk"
    loan_detail_obj.save()
    data = {
        'tr': tr,
        'wt': wt,
        'tAmt': tAmt,
        'pAmt': pAmt,
        'risk': risk
    }
    return JsonResponse(data)

def grandAmountCal(loan_info_obj):
    amt = loan_info_obj.loan_amount
    rt = loan_info_obj.rate_of_interest
    aprove_date = loan_info_obj.added_date.date()
    today = date.today()
    if loan_info_obj.exit_date:
        today = loan_info_obj.exit_date.date()
    day = today - aprove_date
    day = day.days
    si = amt * day * (rt / 30)
    si = si / 100
    if day < 30:
        si = (amt * rt) / 100

    grand = amt + si
    grand = round(grand,3)
    si= round(si,3)
    return si ,grand




class Serial(View):
    template_name = "Loan/add_serial_no.html"
    def get(self,request):

        return render(request,self.template_name)
    def post(self,request):
        name=request.POST.get('name')
        if name!='':
            obj=SerialNo()
            obj.name=name
            obj.save()
        return redirect('add_loan')



 # Loan View Page
def viewLoan(request,id):
    template_name = "Loan/view_loan.html"
    currentDate = datetime.now()
    currentDate = currentDate.strftime("%x")
    ed = LoanDetail.objects.get(id=id)
    ed1 = LoanInfo.objects.get(id=ed.LoanID)
    notes = LoanDetail.objects.all().order_by('TodayDate').reverse()
    paginator = Paginator(notes, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Grand Amount Calculation
    amt=ed1.loan_amount
    si, grand = grandAmountCal(ed1)
    context= {
        'loanD': ed,
        'loanI': ed1,
        'loanA': amt,
        'notes': page_obj,
        'currentDate': currentDate,
        'total_interest': si,
        'grand': grand
    }
    return render(request, template_name,context)


def addNotes(request, id):
    if request.POST.get('Notes') is not None:
        nts = LoanDetail()
        nts.Notes = request.POST.get('Notes')
        nts.save()
    return redirect('/view/{}'.format(id))



def updateLoan(request, id):
    items = PrrodcutMaster.objects.all()
    if request.method == 'POST':
        ed = LoanDetail.objects.get(id=id)
        ed1 = LoanInfo.objects.get(id=ed.LoanID)
        if (ed is not None and ed1 is not None):
            ed.name = request.POST.get('name')
            ed1.LoanID = request.POST.get('name')
            ed1.weight = request.POST.get('weight')
            ed1.rate_of_interest = request.POST.get('rate_of_interest')
            ed1.interest_per_day = request.POST.get('interest_per_day')
            ed.Notes = request.POST.get('Notes')
            ed.TodayRate = request.POST.get('TodayRate')
            ed.save()
            ed1.save()
        return redirect('/')
    else:
        template_name = "Loan/update_loan.html"
        ed = LoanDetail.objects.get(id=id)
        ed1 = LoanInfo.objects.get(id=ed.LoanID)
        return render(request, template_name, {'loanD': ed, 'loanI': ed1, 'items': items})


def delLoan(request, id):
    try:
        ids = LoanDetail.objects.get(id=id)
        ids.Active=False
        ids.save()

    except:
        pass
    return redirect('/')


def exitLoan(request,id):
    ids = LoanDetail.objects.get(id=id)
    time = datetime.now()
    loan_info=LoanInfo.objects.get(id=ids.LoanID)
    loan_info.exit_date = time
    loan_info.save()

    return redirect('/')



class Report(View):
    template_name = "Loan/report.html"

    def amount_send(self,loan_info):
        amount_send = 0
        interest = 0
        for i in loan_info:
            if i.loan.filter(Active=True).exists():
                si, grand = grandAmountCal(i)
                interest += si
                amount_send += i.loan_amount

        return amount_send , interest

    def amount_recive(self,loan_info):
        amount_receive = 0
        for i in loan_info:
            if i.loan.filter(Active=True).exists():
                if i.exit_date:
                    si, grand = grandAmountCal(i)
                    amount_receive += grand
        return amount_receive

    def get(self,request):
        to_date = request.GET.get('to')
        froms = request.GET.get('froms')
        loan_info_recive = LoanInfo.objects.all()
        loan_info_send = LoanInfo.objects.all()
        if froms and froms !='':
            from_date = str_to_date(froms)
            from_date_time = datetime.strptime(str(from_date.date()) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            loan_info_send = loan_info_send.filter(added_date__date__gte=from_date_time)
            loan_info_recive = loan_info_recive.filter(exit_date__date__gte=from_date_time)
        if to_date and to_date !='':
            to_dates = str_to_date(to_date)
            to_date_time = datetime.strptime(str(to_dates.date()) + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            loan_info_send = loan_info_send.filter(added_date__date__lte=to_date_time)
            loan_info_recive = loan_info_recive.filter(exit_date__date__lte=to_date_time)


        profit = 0
        loss = 0
        amount_receive = self.amount_recive(loan_info_recive)
        amount_send ,interest = self.amount_send(loan_info_send)
        # for i in loan_info:
        #     if i.loan.filter(Active=True).exists():
        #         if i.exit_date:
        #             si, grand = grandAmountCal(i)
        #             amount_receive += grand
        #         else:
        #             si, grand = grandAmountCal(i)
        #             interest += si
        #
        #         amount_send += i.loan_amount

        amount_receive = round(amount_receive,3)
        amount_send = round(amount_send,3)
        interest = round(interest,3)
        if amount_receive > amount_send:
            profit = amount_receive-amount_send
            profit = round(profit,3)
        else:
            loss = amount_send-amount_receive
            loss = round(loss,3)
        context = {
            'amount_send':amount_send,
            'amount_receive':amount_receive,
            'profit':profit,
            'interest':interest,
            'loss':loss,
            'froms':froms,
            'to_date':to_date,
        }

        return render(request,self.template_name,context)
    def post(self,request):
        pass


class LoanList(View):
    template_name = "home/home.html"

    def get(self, request):
        sn = SerialNo.objects.all()
        name=request.GET.get('name')
        sns=request.GET.get('sno')
        Sname=request.GET.get('Sname')
        risk=request.GET.get('risk')
        to = request.GET.get('to')
        froms= request.GET.get('froms')
        frm = LoanDetail.objects.all().order_by('LoanID').reverse()
        if name and name != '':
            frm = frm.filter(LoanID__name=name)
        if sns and sns != '':
            frm = frm.filter(LoanID__sr_no__startswith=sns)
        if Sname and Sname != '':
            frm = frm.filter(LoanID__sr_no=Sname)
        if risk and risk != '':
            frm = frm.filter(IsonRisk=risk)
        if to and to != '':
            frm = frm.filter(LoanID__added_date__date__lte = to)
        if froms and froms != '':
            frm = frm.filter(LoanID__added_date__date__gte=froms)
        item=PrrodcutMaster.objects.all()
        # param = request.get_full_path()
        # params = param.replace('/?', '')
        paginator = Paginator(frm, 50)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # calculation of Total Loan In safe or In risk ---
        loan=LoanDetail.objects.filter(Active=True)
        total_loan=0
        loan_safe=0
        loan_risk=0
        for i in loan:
            if i.IsonRisk=='True':
                loan_risk+=1
            else:
                loan_safe+=1

        total_loan=loan_safe+loan_risk
        loan_total=[total_loan,loan_risk,loan_safe]
        return render(request, self.template_name, {'loanF': page_obj,'items':item,'Sno':sn,'loan_total':loan_total,
                                                    'filter_serial_no':sns, 'filter_risk':risk,
                                                    'name':name, 'sns':sns, 'risk': risk,'froms':froms,'to':to})


    def post(selfself,request):
        today_rate=request.POST.get('TodayRate')
        product=request.POST.get('product_Name')
        loan_detail=LoanDetail.objects.all()

        for i in loan_detail:
            try:
                # import pdb
                # pdb.set_trace()
                amount = i.LoanID.amount
                today_value_til_date = 0
                present_amount = float(today_rate) * float(i.LoanID.weight)
                product_type = str(i.LoanID.product_id)
                i.UpdateRate = today_rate
                today_value_til_date = float(i.LoanID.weight) * float(i.UpdateRate)
                ed1 = LoanInfo.objects.get(id=i.LoanID)
                si, grand = grandAmountCal(ed1)
                if grand > today_value_til_date and product_type == product and today_value_til_date != 0:
                # if amount > present_amount and product_type==product:
                    i.IsonRisk=True
                    i.save()
                elif product_type==product:
                    i.IsonRisk=False
                    i.save()
            except:
                pass
        return redirect('/')


class AddLoan(View):
    template_name = "Loan/add_new_loan.html"
    form_class = LoanInfoForm
    form_c = LoanDetailForm

    def get(self, request):
        form = self.form_class
        items = PrrodcutMaster.objects.all()
        sn = SerialNo.objects.all()

        return render(request, self.template_name, {'form': form, 'items': items, 'Sno': sn})

    def post(self, request):
        forms = self.form_c(request.POST, request.FILES)
        form = self.form_class(request.POST, request.FILES)
        # serial No insertion method
        fSn = request.POST.get('sno')
        DSno = LoanInfo.objects.values_list('sr_no', flat=True)

        sn = []
        for i in DSno:
            # i=str(i)
            try:
                num = int(i[len(fSn):])
                if i[:len(fSn)] == fSn:
                    sn.append(i)
            except:
                continue



        if (len(sn) == 0):
            fSn = fSn + '0001'
        else:
            sn = max(sn)
            sn = sn[len(fSn):]
            sn = int(sn)
            if (sn < 9):
                sn += 1
                fSn = fSn + '000' + str(sn)
            elif (sn < 99):
                sn = sn + 1
                fSn = fSn + '00' + str(sn)
            elif (sn < 999):
                sn = sn + 1
                fSn = fSn + '0' + str(sn)
            else:
                fSn = fSn + str(sn)

        total_weight = request.POST.get('weight')
        total_rate = request.POST.get('TodayRate')
        pd_id = request.POST.get('product_Name')
        approve_per = request.POST.get('approve_per')
        itm = PrrodcutMaster.objects.get(name=pd_id)
        total_amount = float(total_weight) * float(total_rate)
        act_loan_amt = total_amount*float(approve_per)/100
        act_loan_amt=round(float(act_loan_amt),3)

        approve_per = request.POST.get('loan')
        approve_per = round(float(approve_per),3)

        risk=False
        if act_loan_amt<approve_per:
            risk=True

        total_amount = round(total_amount,3)

        # Date code
        dates = datetime.now()
        if request.POST.get('dat'):
            dates = request.POST.get('dat')

         # Interest per day Calculations
        int_rate = request.POST.get('rate_of_interest')
        interest_per_day = approve_per * float(int_rate)/(100*30)
        interest_per_day=round(interest_per_day,3)

        if form.is_valid() and forms.is_valid():
            add_product = form.save()
            add_p = forms.save()
            add_product.sr_no = fSn
            add_product.product_id = itm
            add_product.added_date = dates
            add_product.interest_per_day = interest_per_day
            add_p.LoanID = add_product
            add_p.Active = True
            add_p.IsonRisk = risk
            add_product.amount = total_amount
            add_product.loan_amount = approve_per
            add_product.save()
            add_p.save()
        return redirect('/')
