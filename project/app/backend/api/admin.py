from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # CustomUserを使用する場合
from .models import (
    User, Owner, Company, BusinessAlliance, Property, Case,
    ConstructionType, Estimate, EstimateItem, Contract, ContractItem,
    SurveyRecord, ReportRecord, Schedule, AsbestosSurvey, RevenueCost, EstimateHistory, ContractHistory, AuditLog
)

# Register your models here.

# Custom Userモデルを登録する場合
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'employee_number', 'email', 'role', 'status', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee_number', 'role', 'status', 'is_first_login')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('employee_number', 'role', 'status', 'is_first_login')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Owner)
admin.site.register(Company)
admin.site.register(BusinessAlliance)
admin.site.register(Property)
admin.site.register(Case)
admin.site.register(ConstructionType)
admin.site.register(Estimate)
admin.site.register(EstimateItem)
admin.site.register(Contract)
admin.site.register(ContractItem)
admin.site.register(SurveyRecord)
admin.site.register(ReportRecord)
admin.site.register(Schedule)

@admin.register(AsbestosSurvey)
class AsbestosSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'contract', 'survey_date', 'inspector', 'result', 'created_at')
    search_fields = ('result',)
    list_filter = ('survey_date', 'inspector', 'result', 'created_at')

@admin.register(RevenueCost)
class RevenueCostAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'contract', 'revenue', 'cost', 'commission', 'created_at')
    search_fields = ('note',)
    list_filter = ('created_at', 'case', 'contract')

@admin.register(EstimateHistory)
class EstimateHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'estimate', 'version', 'changed_by', 'changed_at')
    search_fields = ('estimate__id',)
    list_filter = ('changed_by', 'changed_at')

@admin.register(ContractHistory)
class ContractHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'version', 'changed_by', 'changed_at')
    search_fields = ('contract__id',)
    list_filter = ('changed_by', 'changed_at')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'model', 'object_id', 'created_at')
    search_fields = ('user__username', 'model', 'object_id', 'detail')
    list_filter = ('action', 'model', 'created_at')
