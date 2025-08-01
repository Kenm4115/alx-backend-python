from .models import Message, Notification, MessageHistory
from django.contrib import admin

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('old_content', 'edited_at')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'edited')
    inlines = [MessageHistoryInline]


admin.site.register(Message, MessageAdmin)
admin.site.register(Notification)
