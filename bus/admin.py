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

# class BusRouteTownAdmin(admin.ModelAdmin):
#     model = BusRouteTown
#     list_display = ('id','days','towns')

# admin.site.register(BusRouteTown, BusRouteTownAdmin)

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