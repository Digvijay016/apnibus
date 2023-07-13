from django.contrib import admin
from .models import Operator

class OperatorAdmin(admin.ModelAdmin):
    model = Operator
    list_display = ('name', 'company_name', 'mobile','town', 'address', 'status',
                 'setup_fee', 'monthly_subscription_fee', 'pos_given_as','rejection_reason')


admin.site.register(Operator, OperatorAdmin)
