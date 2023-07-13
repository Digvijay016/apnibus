"""
import json
import logging
from django.contrib import admin
from bus.models.bus import Bus
from bus.models.bus_route import BusRoute
from bus.models.bus_route_town import BusRouteTown
from django.db.models import JSONField
from django.forms import widgets

logger = logging.getLogger(__name__)

class BusAdmin(admin.ModelAdmin):
    model = Bus
    list_display = ('bus_number', 'get_operator' ,'pos_dsn_number')
    search_fields = ['bus_number','operator__name']

    @admin.display(description='Operator')
    def get_operator(self, obj):
        return obj.operator.name

admin.site.register(Bus, BusAdmin)

class BusRouteAdmin(admin.ModelAdmin):
    model = BusRoute
    list_display = ('from_town', 'to_town','start_time', 'arrival_time')

admin.site.register(BusRoute, BusRouteAdmin)

class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('}')]
            self.attrs['rows'] = min(max(len(row_lengths) + 3, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 3, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


class JsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

admin.site.register(BusRouteTown, JsonAdmin)

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
