from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, filters
from .models import Owner, Company, Property, BusinessAlliance, Case, Estimate, Contract, Schedule, User, SurveyRecord, ReportRecord, EstimateHistory, ContractHistory, AsbestosSurvey, RevenueCost, AuditLog, ConstructionType
from .serializers import OwnerSerializer, CompanySerializer, PropertySerializer, BusinessAllianceSerializer, CaseSerializer, EstimateSerializer, ContractSerializer, ScheduleSerializer, UserSerializer, SurveyRecordSerializer, ReportRecordSerializer, EstimateHistorySerializer, ContractHistorySerializer, AsbestosSurveySerializer, RevenueCostSerializer, AuditLogSerializer, ConstructionTypeSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Custom Permission Classes
class IsHQUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'HQ'

class IsSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Sales'

class IsConstructionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Construction'

class IsSalesOrHQUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'Sales' or request.user.role == 'HQ')

class IsSalesOrConstructionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'Sales' or request.user.role == 'Construction')

class IsHQOrConstructionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'HQ' or request.user.role == 'Construction')

class IsAuthenticatedReadOnly(permissions.BasePermission):
    """Authenticated users can read, unauthenticated users cannot."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Write permissions are only allowed to the superuser.
        return request.user and request.user.is_superuser

# Create your views here.

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    filterset_fields = ['name', 'address', 'assigned_sales', 'created_at', 'updated_at']
    ordering_fields = ['name', 'created_at', 'updated_at']

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'contact_person_name']
    filterset_fields = ['name', 'address', 'contact_person_name', 'created_at', 'updated_at']
    ordering_fields = ['name', 'created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsHQUser()]
        return super().get_permissions()

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address']
    filterset_fields = ['owner', 'company', 'property_type', 'year_built', 'last_inspection_date', 'created_at', 'updated_at']
    ordering_fields = ['address', 'year_built', 'last_inspection_date', 'created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSalesUser()]
        return super().get_permissions()

class BusinessAllianceViewSet(viewsets.ModelViewSet):
    queryset = BusinessAlliance.objects.all()
    serializer_class = BusinessAllianceSerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company__name']
    filterset_fields = ['company', 'start_date', 'referral_commission_rate', 'created_at', 'updated_at']
    ordering_fields = ['start_date', 'referral_commission_rate', 'created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsHQUser()]
        return super().get_permissions()

def log_audit(user, action, instance, detail=None):
    from .models import AuditLog
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        model=instance.__class__.__name__,
        object_id=str(getattr(instance, 'id', '')),
        detail=detail or ''
    )

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['property__address', 'owner__name']
    filterset_fields = [
        'case_type', 'status', 'assigned_sales', 'property', 'owner',
        'occurence_date', 'created_at', 'updated_at',
    ]
    ordering_fields = ['occurence_date', 'created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSalesOrHQUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'update', instance)

    def perform_destroy(self, instance):
        log_audit(self.request.user, 'delete', instance)
        instance.delete()

class EstimateViewSet(viewsets.ModelViewSet):
    queryset = Estimate.objects.all()
    serializer_class = EstimateSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['case__property__address']
    filterset_fields = [
        'case', 'approval_status', 'approver', 'created_date', 'approval_date', 'valid_until',
        'created_at', 'updated_at',
    ]
    ordering_fields = ['created_date', 'approval_date', 'created_at', 'updated_at', 'total_amount']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # 承認アクションの権限は@actionで定義済み
            return [IsSalesOrHQUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = self.get_object()
        # バージョン番号は履歴数+1
        version = instance.histories.count() + 1
        EstimateHistory.objects.create(
            estimate=instance,
            version=version,
            data=EstimateSerializer(instance).data,
            changed_by=self.request.user if self.request.user.is_authenticated else None
        )
        log_audit(self.request.user, 'update', instance)
        serializer.save()

    def perform_destroy(self, instance):
        version = instance.histories.count() + 1
        EstimateHistory.objects.create(
            estimate=instance,
            version=version,
            data=EstimateSerializer(instance).data,
            changed_by=self.request.user if self.request.user.is_authenticated else None
        )
        log_audit(self.request.user, 'delete', instance)
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsHQUser])
    def approve(self, request, pk=None):
        estimate = self.get_object()
        if estimate.approval_status == 'Approved':
            return Response({'detail': 'この見積書は既に承認済みです。', 'approval_status': estimate.approval_status}, status=status.HTTP_400_BAD_REQUEST)

        estimate.approval_status = 'Approved'
        estimate.approver = request.user
        estimate.approval_date = timezone.now().date()
        estimate.save()
        serializer = self.get_serializer(estimate)
        log_audit(request.user, 'approve', estimate)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsSalesOrHQUser])
    def histories(self, request, pk=None):
        estimate = self.get_object()
        histories = estimate.histories.all()
        serializer = EstimateHistorySerializer(histories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='histories/(?P<history_id>[^/.]+)/rollback', permission_classes=[IsHQUser])
    def rollback_history(self, request, pk=None, history_id=None):
        estimate = self.get_object()
        history = get_object_or_404(EstimateHistory, pk=history_id, estimate=estimate)
        serializer = EstimateSerializer(estimate, data=history.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'estimate': serializer.data})

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['case__property__address']
    filterset_fields = [
        'case', 'approval_status', 'approver', 'contract_type', 'contract_date', 'approval_date',
        'customer_confirmation_status', 'created_at', 'updated_at',
    ]
    ordering_fields = ['contract_date', 'approval_date', 'created_at', 'updated_at', 'contract_amount']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
             # 承認アクションの権限は@actionで定義済み
            return [IsSalesOrHQUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = self.get_object()
        version = instance.histories.count() + 1
        ContractHistory.objects.create(
            contract=instance,
            version=version,
            data=ContractSerializer(instance).data,
            changed_by=self.request.user if self.request.user.is_authenticated else None
        )
        log_audit(self.request.user, 'update', instance)
        serializer.save()

    def perform_destroy(self, instance):
        version = instance.histories.count() + 1
        ContractHistory.objects.create(
            contract=instance,
            version=version,
            data=ContractSerializer(instance).data,
            changed_by=self.request.user if self.request.user.is_authenticated else None
        )
        log_audit(self.request.user, 'delete', instance)
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsHQUser])
    def approve(self, request, pk=None):
        contract = self.get_object()
        if contract.approval_status == 'Approved':
            return Response({'detail': 'この契約書は既に承認済みです。', 'approval_status': contract.approval_status}, status=status.HTTP_400_BAD_REQUEST)

        contract.approval_status = 'Approved'
        contract.approver = request.user
        contract.approval_date = timezone.now().date()
        contract.save()
        serializer = self.get_serializer(contract)
        log_audit(request.user, 'approve', contract)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsSalesOrHQUser])
    def histories(self, request, pk=None):
        contract = self.get_object()
        histories = contract.histories.all()
        serializer = ContractHistorySerializer(histories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='histories/(?P<history_id>[^/.]+)/rollback', permission_classes=[IsHQUser])
    def rollback_history(self, request, pk=None, history_id=None):
        contract = self.get_object()
        history = get_object_or_404(ContractHistory, pk=history_id, contract=contract)
        serializer = ContractSerializer(contract, data=history.data, partial=True, context={'skip_validation': True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'contract': serializer.data})

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'details']
    filterset_fields = ['schedule_date', 'location', 'type', 'assigned_to', 'case', 'created_at', 'updated_at']
    ordering_fields = ['schedule_date', 'start_time', 'end_time', 'created_at', 'updated_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSalesOrConstructionUser()]
        return super().get_permissions()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee_number', 'first_name', 'last_name']
    filterset_fields = ['role', 'status', 'is_first_login', 'created_at', 'updated_at']
    ordering_fields = ['employee_number', 'created_at', 'updated_at']

class SurveyRecordViewSet(viewsets.ModelViewSet):
    queryset = SurveyRecord.objects.all()
    serializer_class = SurveyRecordSerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['summary', 'details']
    filterset_fields = ['survey_date', 'case', 'assigned_to', 'created_at', 'updated_at']
    ordering_fields = ['survey_date', 'created_at', 'updated_at']

class ReportRecordViewSet(viewsets.ModelViewSet):
    queryset = ReportRecord.objects.all()
    serializer_class = ReportRecordSerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['negotiation_content', 'result']
    filterset_fields = ['report_date', 'case', 'assigned_to', 'result', 'created_at', 'updated_at']
    ordering_fields = ['report_date', 'created_at', 'updated_at']

class AsbestosSurveyViewSet(viewsets.ModelViewSet):
    queryset = AsbestosSurvey.objects.all()
    serializer_class = AsbestosSurveySerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['result']
    filterset_fields = ['case', 'contract', 'survey_date', 'inspector', 'created_at', 'updated_at']
    ordering_fields = ['survey_date', 'created_at', 'updated_at']

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'update', instance)

    def perform_destroy(self, instance):
        log_audit(self.request.user, 'delete', instance)
        instance.delete()

class RevenueCostViewSet(viewsets.ModelViewSet):
    queryset = RevenueCost.objects.all()
    serializer_class = RevenueCostSerializer
    permission_classes = [IsSalesOrHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['note']
    filterset_fields = [
        'case', 'case__assigned_sales', 'case__case_type', 'contract',
        'created_at', 'updated_at',
        'revenue', 'cost', 'commission',
    ]
    ordering_fields = ['created_at', 'updated_at', 'revenue', 'cost', 'commission']

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'update', instance)

    def perform_destroy(self, instance):
        log_audit(self.request.user, 'delete', instance)
        instance.delete()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        username = data.get('username')
        # employee_numberでもusernameでもログインできるようにする
        User = get_user_model()
        try:
            user_obj = User.objects.get(employee_number=username)
            data['username'] = user_obj.username
        except User.DoesNotExist:
            pass  # 通常のusername認証にフォールバック
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'role': user.role,
            'employee_number': user.employee_number,
        })

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsHQUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'model', 'object_id', 'detail']
    filterset_fields = ['action', 'model', 'user', 'created_at']
    ordering_fields = ['created_at']

class ConstructionTypeViewSet(viewsets.ModelViewSet):
    queryset = ConstructionType.objects.all()
    serializer_class = ConstructionTypeSerializer
    permission_classes = [IsAuthenticatedReadOnly]
