from django.contrib import admin
from .models import Problem, Contest

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name',)

admin.site.register(Problem)
