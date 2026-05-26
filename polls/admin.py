from django.contrib import admin

# Register your models here.
class DateDecisionAdmin(admin.ModelAdmin):
    list_display = ('decision', 'voter_ip', 'timestamp')
    list_filter = ('decision', 'timestamp')