from django.contrib import admin
from .models import PersonalRegistrado
from .models import LiveData
from .models import Historial
from .models import NoRegistrados
from .models import deviceID

# Register your models here.


class PersonalRegistradoAdmin(admin.ModelAdmin):
    readonly_fields = ("f_alta", )


admin.site.register(PersonalRegistrado, PersonalRegistradoAdmin)
admin.site.register(LiveData)
admin.site.register(Historial)
admin.site.register(NoRegistrados)
admin.site.register(deviceID)
