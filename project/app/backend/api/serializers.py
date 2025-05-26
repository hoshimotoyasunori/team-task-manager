from rest_framework import serializers
from .models import Owner, Company, Property, BusinessAlliance, Case, Estimate, Contract, Schedule, User, SurveyRecord, ReportRecord, EstimateHistory, ContractHistory, AsbestosSurvey, RevenueCost, AuditLog, ConstructionType

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class BusinessAllianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAlliance
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

    def validate(self, data):
        # ロールバック時など、バリデーションをスキップしたい場合
        if self.context.get('skip_validation', False):
            return data
        estimate = data.get('estimate')
        if estimate is None:
            raise serializers.ValidationError("契約書作成には関連する見積書が必要です。")
        if estimate.approval_status != 'Approved':
            raise serializers.ValidationError("見積書が承認済みでないと契約書を作成できません。")
        return data

class ScheduleSerializer(serializers.ModelSerializer):
    # titleフィールドはモデル追加により自動的に含まれます
    class Meta:
        model = Schedule
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class SurveyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyRecord
        fields = '__all__'

class ReportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRecord
        fields = '__all__'

class EstimateHistorySerializer(serializers.ModelSerializer):
    diff_summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EstimateHistory
        fields = '__all__'
        extra_fields = ['diff_summary']

    def get_diff_summary(self, obj):
        # 直前の履歴を取得
        prev = obj.estimate.histories.filter(changed_at__lt=obj.changed_at).order_by('-changed_at').first()
        if not prev:
            return '初回作成'
        # 差分抽出（主要フィールドのみ例示）
        diffs = []
        fields = ['total_amount', 'approval_status', 'approval_date', 'valid_until']
        for f in fields:
            prev_val = prev.data.get(f)
            curr_val = obj.data.get(f)
            if prev_val != curr_val:
                diffs.append(f"{f}: {prev_val} → {curr_val}")
        return ' / '.join(diffs) if diffs else '主な変更なし'

class ContractHistorySerializer(serializers.ModelSerializer):
    diff_summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContractHistory
        fields = '__all__'
        extra_fields = ['diff_summary']

    def get_diff_summary(self, obj):
        prev = obj.contract.histories.filter(changed_at__lt=obj.changed_at).order_by('-changed_at').first()
        if not prev:
            return '初回作成'
        diffs = []
        fields = ['contract_amount', 'approval_status', 'approval_date', 'contract_type', 'customer_confirmation_status']
        for f in fields:
            prev_val = prev.data.get(f)
            curr_val = obj.data.get(f)
            if prev_val != curr_val:
                diffs.append(f"{f}: {prev_val} → {curr_val}")
        return ' / '.join(diffs) if diffs else '主な変更なし'

class AsbestosSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = AsbestosSurvey
        fields = '__all__'

class RevenueCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueCost
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class ConstructionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionType
        fields = '__all__' 