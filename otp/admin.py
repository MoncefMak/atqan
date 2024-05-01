from django.contrib import admin
from .models import Otp

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'is_active', 'created_at')
    search_fields = ('user__email', 'otp_code')
    list_filter = ('is_active',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)