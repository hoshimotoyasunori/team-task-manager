from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OwnerViewSet, CompanyViewSet, PropertyViewSet, BusinessAllianceViewSet, CaseViewSet, EstimateViewSet, ContractViewSet, ScheduleViewSet, UserViewSet, CustomAuthToken, SurveyRecordViewSet, ReportRecordViewSet, AsbestosSurveyViewSet, RevenueCostViewSet, AuditLogViewSet, ConstructionTypeViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'owners', OwnerViewSet, basename='owner')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'business-alliances', BusinessAllianceViewSet, basename='businessalliance')
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'estimates', EstimateViewSet, basename='estimate')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'users', UserViewSet, basename='user')
router.register(r'surveyrecords', SurveyRecordViewSet, basename='surveyrecord')
router.register(r'reportrecords', ReportRecordViewSet, basename='reportrecord')
router.register(r'asbestos-surveys', AsbestosSurveyViewSet, basename='asbestossurvey')
router.register(r'revenue-costs', RevenueCostViewSet, basename='revenuecost')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')
router.register(r'constructiontypes', ConstructionTypeViewSet, basename='constructiontype')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api-login'),
    path('token/', CustomAuthToken.as_view(), name='api-token'),
    path('', include(router.urls)),
] 