from django.contrib import admin

from polls.models import DateDecision

@admin.register(DateDecision)
class DateDecisionAdmin(admin.ModelAdmin):
    list_display = ('decision', 'voter_ip', 'timestamp')
    list_filter = ('decision', 'timestamp')