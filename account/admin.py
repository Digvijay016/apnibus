from django.contrib import admin
from .models import Operator
from rest_framework import filters
from .models import Operator

class OperatorAdmin(admin.ModelAdmin):
    model = Operator
    list_display = ('name', 'company_name', 'mobile','town', 'address', 'status',
                 'setup_fee', 'monthly_subscription_fee', 'pos_given_as','rejection_reason')
    list_filter = ['status']
    # filter_backends = [filters.SearchFilter]
    search_fields = ['name','company_name','mobile']


admin.site.register(Operator, OperatorAdmin)
