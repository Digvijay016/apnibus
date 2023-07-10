from django.contrib import admin
from bus.models.bus import Bus
from bus.models.bus_route import BusRoute
from bus.models.bus_route_town import BusRouteTown


class BusAdmin(admin.ModelAdmin):
    model = Bus
    list_display = ('bus_number', 'get_operator','pos_dsn_number')
    search_fields = []

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
