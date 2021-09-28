from django.contrib import admin

from .models import *

class PrrodcutMasterAdmin(admin.ModelAdmin):
    list_per_page = 1000
    show_full_result_count = False
    list_display = [f.name for f in PrrodcutMaster._meta.fields]

admin.site.register(PrrodcutMaster, PrrodcutMasterAdmin)

class LoanInfoAdmin(admin.ModelAdmin):
    list_per_page = 1000
    show_full_result_count = False
    list_display = [f.name for f in LoanInfo._meta.fields]


admin.site.register(LoanInfo,LoanInfoAdmin)

class LoanDetailAdmin(admin.ModelAdmin):
    list_per_page = 1000
    show_full_result_count = False
    list_display = [f.name for f in LoanDetail._meta.fields]

admin.site.register(LoanDetail, LoanDetailAdmin)

class SerialNoAdmin(admin.ModelAdmin):
    list_per_page = 1000
    show_full_result_count = False
    list_display = [f.name for f in SerialNo._meta.fields]

admin.site.register(SerialNo, SerialNoAdmin)