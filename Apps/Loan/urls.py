from .import views
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # path('loan_list', LoanList.as_view(), name="loan_list"),
    path('report', login_required(Report.as_view()), name="report"),
    path('', login_required(LoanList.as_view()), name="loan_list"),
    path('add_loan', login_required(AddLoan.as_view()), name="add_loan"),
    path('serial_add', login_required(Serial.as_view()), name="serial_add"),
    path('update/<int:id>', login_required(updateLoan), name='update'),
    path('view/<int:id>', login_required(viewLoan), name='view'),
    path('Notes-add/<int:id>',login_required(addNotes),name='Notes_add'),
    path('update-is-on-risk/<int:id>',login_required(riskUpdate),name='update_is_on_risk'),
    path('view/del/<int:id>', login_required(delLoan), name='del'),
    path('exit_ac/del/<int:id>', login_required(exitLoan), name='exit_ac'),



]