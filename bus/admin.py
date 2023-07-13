from django.contrib import admin
from bus.models.bus import Bus
from bus.models.bus_route import BusRoute
from bus.models.bus_route_town import BusRouteTown

"""
class BusAdmin(admin.ModelAdmin):
    model = Bus
    list_display = ('bus_number', 'get_operator', 'pos_serial_no',
                  'pos_dsn_number', 'gps_sim_image','category','brand','has_wifi','has_power_plug',
                  'is_sanitized','is_air_conditioned','operating_as','driver_name','driver_contact',
                  'conductor_name','conductor_contact','seat_type','layout_type','is_multi_axle',
                  'normal_seats_capacity','single_sleeper_capacity','sharing_sleeper_capacity',
                  'upper_single_sleeper_capacity','upper_sharing_sleeper_capacity','recliner_capacity',
                  'status','gps_status','commission','digital_commission','cash_commission',
                  'is_booking_allowed','is_qr_booking_allowed','is_pos_connected','printing_enabled',
                  'trips_access','print_bus_number','access_password','ticket_header','ticket_footer',
                  'subscription_pending','apply_concession','apply_bus_discount','apply_qr_discount',
                  'show_passenger_in_poc','online_app_booking_commission','qr_booking_commission')
    
    search_fields = ['bus_number','operator__name','is_sanitized','is_air_conditioned','operating_as']

    @admin.display(description='Operator')
    def get_operator(self, obj):
        return obj.operator.name

admin.site.register(Bus, BusAdmin)

class BusRouteAdmin(admin.ModelAdmin):
    model = BusRoute
    list_display = ('from_town', 'to_town','start_time', 'arrival_time')

admin.site.register(BusRoute, BusRouteAdmin)

class BusRouteTownAdmin(admin.ModelAdmin):
    model = BusRouteTown
    list_display = ('days','towns')

admin.site.register(BusRouteTown, BusRouteTownAdmin)
"""
