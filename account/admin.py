from django.contrib import admin
from .models import Operator, UserAuthenticationOTP, User
from rest_framework import filters


class OperatorAdmin(admin.ModelAdmin):
    model = Operator
    list_display = ('name', 'company_name', 'mobile','town', 'address', 'status',
                 'setup_fee', 'monthly_subscription_fee', 'pos_given_as','rejection_reason')
    list_filter = ['status']
    # filter_backends = [filters.SearchFilter]
    search_fields = ['name','company_name','mobile']


admin.site.register(Operator, OperatorAdmin)
admin.site.register(UserAuthenticationOTP)
admin.site.register(User)
