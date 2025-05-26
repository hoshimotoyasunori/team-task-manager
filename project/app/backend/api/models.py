from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

# ロールとステータスの choices を定義
# データエンティティのroleの例: 営業担当者, 本部担当者, 施工担当者
ROLE_CHOICES = [
    ('Sales', '営業担当者'),
    ('HQ', '本部担当者'),
    ('Construction', '施工担当者'),
]

# データエンティティのUserのstatusの例: Active, Inactive
STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
]

# AbstractUserを継承してUserモデルを定義
class User(AbstractUser):
    # username, password, email, first_name, last_nameなどはAbstractUserから継承
    # user_idは通常DjangoのAbstractUserのidフィールド(Integer PK)を使用
    # もしUUIDを使用したい場合は、以下の行のコメントを外し、上記のidフィールドは使用しない
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee_number = models.CharField(max_length=255, unique=True, verbose_name="社員番号") # ログインIDとして使用
    # password_hash は AbstractUser がhandling
    # AbstractUserにはfirst_nameとlast_nameがあるので、それらをuser_nameとして使用するか検討
    # もし単一のuser_nameフィールドが必要なら追加
    # user_name = models.CharField(max_length=255, verbose_name="氏名")

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="役割")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active', verbose_name="アカウント状態")
    # created_at, updated_at は通常自動で設定されるフィールドを使用 (auto_now_add=True, auto_now=True)
    # is_first_loginはデータエンティティにあるため追加
    is_first_login = models.BooleanField(default=True, verbose_name="初回ログインフラグ")

    # AbstractUserのusernameフィールドをemployee_numberで置き換える場合は以下を追記
    # USERNAME_FIELD = 'employee_number'
    # REQUIRED_FIELDS = ['email'] # 必要に応じて他の必須フィールドを追加

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def __str__(self):
        # 表示名をemployee_numberまたはusernameにするなど調整
        return self.employee_number or self.username

# オーナー エンティティ
class Owner(models.Model):
    # owner_id は Django のデフォルトの PK (id) を使用します
    name = models.CharField(max_length=255, verbose_name="オーナー名")
    contact_info = models.JSONField(null=True, blank=True, verbose_name="連絡先情報") # JSON/String は JSONField が便利
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="住所")
    # 担当営業 (user_id - FK) は User モデルへの ForeignKey
    # User モデルは既に定義済みなので参照できます
    assigned_sales = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # ユーザーが削除されてもオーナー情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='owners', # User モデルから関連Ownerを取得するための名前
        verbose_name="担当営業"
    )
    # 登録日、更新日は auto_now_add=True, auto_now=True を使用
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "オーナー"
        verbose_name_plural = "オーナー"

    def __str__(self):
        return self.name

# 不動産会社/管理会社 エンティティ
class Company(models.Model):
    # company_id は Django のデフォルトの PK (id) を使用します
    name = models.CharField(max_length=255, verbose_name="会社名")
    contact_info = models.JSONField(null=True, blank=True, verbose_name="連絡先情報")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="住所")
    contact_person_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="担当者名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "不動産会社/管理会社"
        verbose_name_plural = "不動産会社/管理会社"

    def __str__(self):
        return self.name

# 物件 エンティティ
class Property(models.Model):
    # property_id は Django のデフォルトの PK (id) を使用します
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE, # オーナーが削除されたら物件も削除 (必要に応じて変更)
        related_name='properties',
        verbose_name="オーナー"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL, # 会社が削除されても物件情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='managed_properties',
        verbose_name="管理会社"
    )
    address = models.CharField(max_length=255, verbose_name="住所")
    # 物件種別の choices を定義 (必要に応じて)
    PROPERTY_TYPE_CHOICES = [
        ('Apartment', '集合住宅'),
        ('House', '戸建て'),
        # 他の種別を追加
    ]
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, verbose_name="物件種別")
    year_built = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="築年数")
    last_inspection_date = models.DateField(null=True, blank=True, verbose_name="最終点検/工事日") # 日付型が適切
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "物件"
        verbose_name_plural = "物件"

    def __str__(self):
        return self.address # または他の識別しやすい情報

# ... other models will be added here ...

# 工事種別 エンティティ
class ConstructionType(models.Model):
    # construction_type_id は Django のデフォルトの PK (id) を使用します
    name = models.CharField(max_length=255, verbose_name="工事種別名")
    description = models.TextField(null=True, blank=True, verbose_name="説明")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "工事種別"
        verbose_name_plural = "工事種別"

    def __str__(self):
        return self.name

# 案件 エンティティ
class Case(models.Model):
    # case_id は Django のデフォルトの PK (id) を使用します
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE, # オーナーが削除されたら案件も削除 (必要に応じて変更)
        related_name='cases',
        verbose_name="オーナー"
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE, # 物件が削除されたら案件も削除 (必要に応じて変更)
        related_name='cases',
        verbose_name="物件"
    )
    assigned_sales = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # 担当営業が削除されても案件情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='assigned_cases',
        verbose_name="担当営業"
    )
    # case_type の choices を定義 (必要に応じて)
    CASE_TYPE_CHOICES = [
        ('New', '新規'),
        ('CS', 'CS'),
        # 他の種別を追加
    ]
    case_type = models.CharField(max_length=50, choices=CASE_TYPE_CHOICES, verbose_name="案件種別")
    # status の choices を定義 (必要に応じて)
    CASE_STATUS_CHOICES = [
        ('Appointment', 'アポ取得済'),
        ('Surveyed', '調査/点検済'),
        ('Negotiating', '商談中'),
        ('Contracted', '契約済'),
        ('InProgress', '施工中'),
        ('Completed', '完了'),
        ('Cancelled', '中止'),
        # 他のステータスを追加
    ]
    status = models.CharField(max_length=50, choices=CASE_STATUS_CHOICES, default='Appointment', verbose_name="案件ステータス")
    occurence_date = models.DateField(verbose_name="発生日") # 日付型が適切
    # 想定工事種別 (construction_type_id - FK, 複数紐付けの可能性あり) は ManyToManyField
    expected_construction_types = models.ManyToManyField(
        ConstructionType,
        related_name='cases',
        verbose_name="想定工事種別"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "案件"
        verbose_name_plural = "案件"

    def __str__(self):
        return f"Case {self.id} ({self.case_type} - {self.status})" # または他の識別しやすい情報

# 見積書 エンティティ
class Estimate(models.Model):
    # estimate_id は Django のデフォルトの PK (id) を使用します
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE, # 案件が削除されたら見積書も削除 (必要に応じて変更)
        related_name='estimates',
        verbose_name="案件"
    )
    created_date = models.DateField(auto_now_add=True, verbose_name="作成日") # 作成日時は自動設定
    valid_until = models.DateField(null=True, blank=True, verbose_name="有効期限")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="合計金額") # 金額なのでDecimalField
    # 承認ステータスの choices を定義 (必要に応じて)
    APPROVAL_STATUS_CHOICES = [
        ('Pending', '未承認'),
        ('Approved', '承認済'),
        ('Rejected', '却下'),
    ]
    approval_status = models.CharField(max_length=50, choices=APPROVAL_STATUS_CHOICES, default='Pending', verbose_name="承認ステータス")
    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # 承認者が削除されても見積書情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='approved_estimates',
        verbose_name="承認者"
    )
    approval_date = models.DateField(null=True, blank=True, verbose_name="承認日")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日") # 登録日時、更新日時は自動設定
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "見積書"
        verbose_name_plural = "見積書"

    def __str__(self):
        return f"Estimate for Case {self.case.id} ({self.created_date})"

# 見積明細 エンティティ
class EstimateItem(models.Model):
    # estimate_item_id は Django のデフォルトの PK (id) を使用します
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE, # 見積書が削除されたら明細も削除
        related_name='items',
        verbose_name="見積書"
    )
    item_name = models.CharField(max_length=255, verbose_name="項目名")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="小計")

    class Meta:
        verbose_name = "見積明細"
        verbose_name_plural = "見積明細"

    def __str__(self):
        return f"Item {self.item_name} for Estimate {self.estimate.id}"

# 契約書 エンティティ
class Contract(models.Model):
    # contract_id は Django のデフォルトの PK (id) を使用します
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE, # 案件が削除されたら契約書も削除 (必要に応じて変更)
        related_name='contracts',
        verbose_name="案件"
    )
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.SET_NULL, # 見積書が削除されても契約書情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='contracts',
        verbose_name="関連見積書"
    )
    # contract_type の choices を定義 (必要に応じて)
    CONTRACT_TYPE_CHOICES = [
        ('Order', '注文書'),
        ('Contract', '契約書'),
        ('CompletionConfirmation', '契約兼完了確認書'),
    ]
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES, verbose_name="契約書種別")
    contract_date = models.DateField(verbose_name="契約日")
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="契約金額")
    desired_construction_date = models.DateField(null=True, blank=True, verbose_name="施工希望日")
    payment_terms = models.TextField(null=True, blank=True, verbose_name="支払い条件")
    owner_sign_date = models.DateField(null=True, blank=True, verbose_name="オーナー記入日")
    # 承認ステータス (本部チェック) の choices を定義 (必要に応じて)
    APPROVAL_STATUS_CHOICES = [
        ('Pending', '未承認'),
        ('Approved', '承認済'),
        ('Rejected', '却下'),
    ]
    approval_status = models.CharField(max_length=50, choices=APPROVAL_STATUS_CHOICES, default='Pending', verbose_name="承認ステータス (本部チェック)")
    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # 承認者が削除されても契約書情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='approved_contracts',
        verbose_name="承認者"
    )
    approval_date = models.DateField(null=True, blank=True, verbose_name="承認日")
    # お客様確認ステータスの choices を定義 (必要に応じて)
    CUSTOMER_CONFIRMATION_CHOICES = [
        ('Required', '要'),
        ('NotRequired', '不要'),
        ('NotImplemented', '未実施'),
        ('CompletedOK', '実施済OK'),
        ('CompletedNG', '実施済NG'),
    ]
    customer_confirmation_status = models.CharField(max_length=50, choices=CUSTOMER_CONFIRMATION_CHOICES, default='Required', verbose_name="お客様確認ステータス")
    customer_confirmation_date = models.DateField(null=True, blank=True, verbose_name="お客様確認日")
    customer_confirmation_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # お客様確認担当者が削除されても契約書情報は残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='confirmed_contracts',
        verbose_name="お客様確認担当者"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "契約書"
        verbose_name_plural = "契約書"

    def __str__(self):
        return f"Contract for Case {self.case.id} ({self.contract_type})"

# 契約明細 エンティティ
class ContractItem(models.Model):
    # contract_item_id は Django のデフォルトの PK (id) を使用します
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE, # 契約書が削除されたら明細も削除
        related_name='items',
        verbose_name="契約書"
    )
    item_name = models.CharField(max_length=255, verbose_name="項目名")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="小計")
    # 見積明細からの引用情報は、必要に応じて ForeignKey で EstimateItem と紐付けるか、
    # このモデル内に情報を duplication するか検討が必要ですが、ここではシンプルに属性として定義
    # related_estimate_item = models.ForeignKey(
    #     EstimateItem,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='contract_items',
    #     verbose_name="関連見積明細"
    # )

    class Meta:
        verbose_name = "契約明細"
        verbose_name_plural = "契約明細"

    def __str__(self):
        return f"Item {self.item_name} for Contract {self.contract.id}"

# 調査/点検記録 エンティティ
class SurveyRecord(models.Model):
    # survey_id は Django のデフォルトの PK (id) を使用します
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE, # 案件が削除されたら記録も削除
        related_name='survey_records',
        verbose_name="案件"
    )
    survey_date = models.DateField(verbose_name="調査/点検日")
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # 担当者が削除されても記録情報は残す
        null=True,
        blank=True,
        related_name='survey_records',
        verbose_name="担当者"
    )
    summary = models.TextField(verbose_name="概要")
    details = models.TextField(verbose_name="結果詳細")
    attachment_paths = models.JSONField(null=True, blank=True, verbose_name="添付資料パス") # ファイルパスはJSONFieldで複数保持可能に
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "調査/点検記録"
        verbose_name_plural = "調査/点検記録"

    def __str__(self):
        return f"Survey Record for Case {self.case.id} on {self.survey_date}"

# 報告/商談記録 エンティティ
class ReportRecord(models.Model):
    # report_id は Django のデフォルトの PK (id) を使用します
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE, # 案件が削除されたら記録も削除
        related_name='report_records',
        verbose_name="案件"
    )
    report_date = models.DateField(verbose_name="報告/商談日")
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # 担当者が削除されても記録情報は残す
        null=True,
        blank=True,
        related_name='report_records',
        verbose_name="担当者"
    )
    negotiation_content = models.TextField(verbose_name="商談内容")
    # 結果の choices を定義 (必要に応じて)
    RESULT_CHOICES = [
        ('Won', '受注'),
        ('Lost', '失注'),
        ('Ongoing', '継続'),
        # 他の結果を追加
    ]
    result = models.CharField(max_length=50, choices=RESULT_CHOICES, verbose_name="結果")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "報告/商談記録"
        verbose_name_plural = "報告/商談記録"

    def __str__(self):
        return f"Report Record for Case {self.case.id} on {self.report_date}"

# スケジュール エンティティ
class Schedule(models.Model):
    # schedule_id は Django のデフォルトの PK (id) を使用します
    case = models.ForeignKey(
        Case,
        on_delete=models.SET_NULL, # 案件が削除されてもスケジュールは残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='schedules',
        verbose_name="関連案件"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # 担当者が削除されてもスケジュールは残す (必要に応じて変更)
        null=True,
        blank=True,
        related_name='schedules',
        verbose_name="担当者"
    )
    schedule_date = models.DateField(verbose_name="スケジュール日")
    start_time = models.TimeField(verbose_name="開始時間") # 時間型が適切
    end_time = models.TimeField(null=True, blank=True, verbose_name="終了時間") # 終了時間は任意
    # type の choices を定義 (必要に応じて)
    SCHEDULE_TYPE_CHOICES = [
        ('Appointment', 'アポイント'),
        ('Construction', '施工'),
        # 他の種別を追加
    ]
    type = models.CharField(max_length=50, choices=SCHEDULE_TYPE_CHOICES, verbose_name="種別")
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name="場所")
    details = models.TextField(null=True, blank=True, verbose_name="詳細")
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="タイトル")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "スケジュール"
        verbose_name_plural = "スケジュール"

    def __str__(self):
        return f"Schedule on {self.schedule_date} ({self.type})"

# 業務提携 エンティティ
class BusinessAlliance(models.Model):
    # alliance_id は Django のデフォルトの PK (id) を使用します
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, # 会社が削除されたら業務提携も削除 (必要に応じて変更)
        related_name='business_alliances',
        verbose_name="提携会社"
    )
    start_date = models.DateField(verbose_name="開始日")
    referral_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="紹介手数料率") # 例: 10.00%
    contract_info = models.TextField(null=True, blank=True, verbose_name="契約書情報") # 関連する契約書へのリンクや情報保持
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "業務提携"
        verbose_name_plural = "業務提携"

    def __str__(self):
        return f"Business Alliance with {self.company.name} (since {self.start_date})"

# 見積書履歴 エンティティ
class EstimateHistory(models.Model):
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        related_name='histories',
        verbose_name="元見積書"
    )
    version = models.PositiveIntegerField(verbose_name="バージョン番号")
    data = models.JSONField(verbose_name="見積書データスナップショット")
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estimate_histories',
        verbose_name="変更者"
    )
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="変更日時")

    class Meta:
        verbose_name = "見積書履歴"
        verbose_name_plural = "見積書履歴"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.estimate.id} v{self.version} ({self.changed_at})"

# 契約書履歴 エンティティ
class ContractHistory(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='histories',
        verbose_name="元契約書"
    )
    version = models.PositiveIntegerField(verbose_name="バージョン番号")
    data = models.JSONField(verbose_name="契約書データスナップショット")
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contract_histories',
        verbose_name="変更者"
    )
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="変更日時")

    class Meta:
        verbose_name = "契約書履歴"
        verbose_name_plural = "契約書履歴"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.contract.id} v{self.version} ({self.changed_at})"

# 石綿調査書類 エンティティ
class AsbestosSurvey(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='asbestos_surveys',
        verbose_name="関連案件"
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asbestos_surveys',
        verbose_name="関連契約書"
    )
    survey_date = models.DateField(verbose_name="調査日")
    inspector = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asbestos_surveys',
        verbose_name="調査担当者"
    )
    result = models.CharField(max_length=255, verbose_name="調査結果")
    attachments = models.JSONField(null=True, blank=True, verbose_name="添付ファイルパス")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "石綿調査書類"
        verbose_name_plural = "石綿調査書類"
        ordering = ["-survey_date", "-created_at"]

    def __str__(self):
        return f"AsbestosSurvey for Case {self.case.id} on {self.survey_date}"

# 売上・原価管理 エンティティ
class RevenueCost(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='revenue_costs',
        verbose_name="関連案件"
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='revenue_costs',
        verbose_name="関連契約書"
    )
    revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="売上金額")
    cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="原価金額")
    commission = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="紹介手数料")
    note = models.TextField(null=True, blank=True, verbose_name="備考")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")

    class Meta:
        verbose_name = "売上・原価管理"
        verbose_name_plural = "売上・原価管理"
        ordering = ["-created_at"]

    def __str__(self):
        return f"RevenueCost for Case {self.case.id} (revenue: {self.revenue})"

# 監査ログ エンティティ
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="操作ユーザー")
    action = models.CharField(max_length=50, verbose_name="操作種別")
    model = models.CharField(max_length=100, verbose_name="対象モデル")
    object_id = models.CharField(max_length=100, verbose_name="対象ID")
    detail = models.TextField(null=True, blank=True, verbose_name="詳細")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="操作日時")

    class Meta:
        verbose_name = "監査ログ"
        verbose_name_plural = "監査ログ"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at} {self.user} {self.action} {self.model}({self.object_id})"
