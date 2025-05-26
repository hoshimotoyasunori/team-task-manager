from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Owner, Company, Property, Case, Contract, User
from api.models import ConstructionType, Estimate, Schedule, BusinessAlliance, SurveyRecord, ReportRecord, EstimateItem, ContractItem
from datetime import date
from rest_framework.test import APIRequestFactory, force_authenticate
from api.serializers import ContractSerializer, UserSerializer
from api.views import IsHQUser, IsSalesUser, IsConstructionUser, IsSalesOrHQUser, IsSalesOrConstructionUser, IsHQOrConstructionUser, IsAuthenticatedReadOnly, CustomAuthToken
from rest_framework.request import Request

# Create your tests here.

class APISmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        # HQユーザーとSalesユーザーを両方作成
        self.hq_user = User.objects.create_user(username='hquser', password='hqpass', employee_number='1000', role='HQ')
        self.sales_user = User.objects.create_user(username='salesuser', password='salespass', employee_number='1001', role='Sales')
        self.hq_token, _ = Token.objects.get_or_create(user=self.hq_user)
        self.sales_token, _ = Token.objects.get_or_create(user=self.sales_user)
        # デフォルトはSalesユーザー
        self.user = self.sales_user
        self.token = self.sales_token.key

    def auth_get(self, url, use_hq=False):
        token = self.hq_token.key if use_hq else self.sales_token.key
        return self.client.get(url, HTTP_AUTHORIZATION=f'Token {token}')

    def auth_post(self, url, data, use_hq=False):
        token = self.hq_token.key if use_hq else self.sales_token.key
        return self.client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {token}')

    def auth_put(self, url, data, use_hq=False):
        token = self.hq_token.key if use_hq else self.sales_token.key
        return self.client.put(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {token}')

    def auth_delete(self, url, use_hq=False):
        token = self.hq_token.key if use_hq else self.sales_token.key
        return self.client.delete(url, HTTP_AUTHORIZATION=f'Token {token}')

    def test_owner_list(self):
        response = self.auth_get('/api/owners/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_create(self):
        data = {'name': 'テストオーナー', 'contact_info': {'tel': '000-0000-0000'}, 'address': '東京都', 'assigned_sales': self.user.id}
        response = self.auth_post('/api/owners/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Owner.objects.filter(name='テストオーナー').count(), 1)

    def test_owner_create_validation_error(self):
        data = {'contact_info': {'tel': '000-0000-0000'}}  # nameがない
        response = self.auth_post('/api/owners/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_update(self):
        owner = Owner.objects.create(name='旧名', contact_info={'tel': '1'}, address='A', assigned_sales=self.user)
        data = {'name': '新名', 'contact_info': {'tel': '2'}, 'address': 'B', 'assigned_sales': self.user.id}
        response = self.auth_put(f'/api/owners/{owner.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        owner.refresh_from_db()
        self.assertEqual(owner.name, '新名')

    def test_owner_delete(self):
        owner = Owner.objects.create(name='削除対象', contact_info={'tel': '1'}, address='A', assigned_sales=self.user)
        response = self.auth_delete(f'/api/owners/{owner.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Owner.objects.filter(id=owner.id).exists())

    def test_company_list(self):
        response = self.auth_get('/api/companies/', use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_create(self):
        data = {'name': 'テスト会社', 'contact_info': {'tel': '03-0000-0000'}, 'address': '東京都', 'contact_person_name': '担当者A'}
        response = self.auth_post('/api/companies/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.filter(name='テスト会社').count(), 1)

    def test_company_create_validation_error(self):
        data = {'contact_info': {'tel': '03-0000-0000'}}  # nameがない
        response = self.auth_post('/api/companies/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_company_update(self):
        company = Company.objects.create(name='旧会社', contact_info={'tel': '1'}, address='A', contact_person_name='担当者B')
        data = {'name': '新会社', 'contact_info': {'tel': '2'}, 'address': 'B', 'contact_person_name': '担当者C'}
        response = self.auth_put(f'/api/companies/{company.id}/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertEqual(company.name, '新会社')

    def test_company_delete(self):
        company = Company.objects.create(name='削除会社', contact_info={'tel': '1'}, address='A', contact_person_name='担当者D')
        response = self.auth_delete(f'/api/companies/{company.id}/', use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())

    def test_property_list(self):
        response = self.auth_get('/api/properties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_list(self):
        response = self.auth_get('/api/cases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_list(self):
        response = self.auth_get('/api/contracts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        response = self.auth_get('/api/users/', use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_property_create(self):
        company = Company.objects.create(name='管理会社', contact_info={'tel': '03-1111-2222'}, address='東京都', contact_person_name='担当者X')
        owner = Owner.objects.create(name='物件オーナー', contact_info={'tel': '090-1111-2222'}, address='東京都', assigned_sales=self.user)
        data = {
            'owner': owner.id,
            'company': company.id,
            'address': '東京都中央区A-1',
            'property_type': 'Apartment',
            'year_built': 2000
        }
        response = self.auth_post('/api/properties/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.filter(address='東京都中央区A-1').count(), 1)

    def test_property_create_validation_error(self):
        data = {'address': '東京都中央区A-2'}  # owner, property_typeがない
        response = self.auth_post('/api/properties/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_property_update(self):
        company = Company.objects.create(name='管理会社2', contact_info={'tel': '03-2222-3333'}, address='東京都', contact_person_name='担当者Y')
        owner = Owner.objects.create(name='物件オーナー2', contact_info={'tel': '090-2222-3333'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='旧住所', property_type='Apartment', year_built=1990)
        data = {
            'owner': owner.id,
            'company': company.id,
            'address': '新住所',
            'property_type': 'House',
            'year_built': 2020
        }
        response = self.auth_put(f'/api/properties/{prop.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prop.refresh_from_db()
        self.assertEqual(prop.address, '新住所')

    def test_property_delete(self):
        company = Company.objects.create(name='管理会社3', contact_info={'tel': '03-3333-4444'}, address='東京都', contact_person_name='担当者Z')
        owner = Owner.objects.create(name='物件オーナー3', contact_info={'tel': '090-3333-4444'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='削除物件', property_type='Apartment', year_built=2010)
        response = self.auth_delete(f'/api/properties/{prop.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Property.objects.filter(id=prop.id).exists())

    def test_case_create(self):
        company = Company.objects.create(name='管理会社C', contact_info={'tel': '03-4444-5555'}, address='東京都', contact_person_name='担当者C')
        owner = Owner.objects.create(name='案件オーナー', contact_info={'tel': '090-4444-5555'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='案件物件', property_type='Apartment', year_built=2015)
        ct = ConstructionType.objects.create(name='テスト工事種別')
        data = {
            'owner': owner.id,
            'property': prop.id,
            'assigned_sales': self.user.id,
            'case_type': 'New',
            'status': 'Appointment',
            'occurence_date': '2024-01-01',
            'expected_construction_types': [ct.id]
        }
        response = self.auth_post('/api/cases/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Case.objects.filter(owner=owner, property=prop).count(), 1)

    def test_case_create_validation_error(self):
        data = {'case_type': 'New'}  # owner, property, status, occurence_dateがない
        response = self.auth_post('/api/cases/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_case_update(self):
        company = Company.objects.create(name='管理会社D', contact_info={'tel': '03-5555-6666'}, address='東京都', contact_person_name='担当者D')
        owner = Owner.objects.create(name='案件オーナー2', contact_info={'tel': '090-5555-6666'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='案件物件2', property_type='Apartment', year_built=2018)
        ct = ConstructionType.objects.create(name='テスト工事種別2')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        data = {
            'owner': owner.id,
            'property': prop.id,
            'assigned_sales': self.user.id,
            'case_type': 'CS',
            'status': 'Surveyed',
            'occurence_date': '2024-02-01',
            'expected_construction_types': [ct.id]
        }
        response = self.auth_put(f'/api/cases/{case.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case.refresh_from_db()
        self.assertEqual(case.case_type, 'CS')

    def test_case_delete(self):
        company = Company.objects.create(name='管理会社E', contact_info={'tel': '03-6666-7777'}, address='東京都', contact_person_name='担当者E')
        owner = Owner.objects.create(name='案件オーナー3', contact_info={'tel': '090-6666-7777'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='案件物件3', property_type='Apartment', year_built=2020)
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        response = self.auth_delete(f'/api/cases/{case.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Case.objects.filter(id=case.id).exists())

    def test_contract_create_xxx(self):
        company = Company.objects.create(name='契約会社', contact_info={'tel': '03-7777-8888'}, address='東京都', contact_person_name='担当者F')
        owner = Owner.objects.create(name='契約オーナー', contact_info={'tel': '090-7777-8888'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='契約物件', property_type='Apartment', year_built=2017)
        ct = ConstructionType.objects.create(name='契約工事種別')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        estimate = Estimate.objects.create(case=case, total_amount=1000000, approval_status='Approved')
        data = {
            'case': case.id,
            'estimate': estimate.id,
            'contract_type': 'Order',
            'contract_date': '2024-06-01',
            'contract_amount': '1000000.00',
            'approval_status': 'Pending',
            'customer_confirmation_status': 'Required'
        }
        response = self.auth_post('/api/contracts/', data)
        if response.status_code != status.HTTP_201_CREATED:
            raise AssertionError(f"status={response.status_code}, data={repr(response.data)}, content={response.content}, content_decoded={response.content.decode(errors='replace')}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.filter(case=case).count(), 1)

    def test_contract_create_validation_error(self):
        data = {'contract_type': 'Order'}  # 必須項目不足
        response = self.auth_post('/api/contracts/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contract_update(self):
        company = Company.objects.create(name='契約会社2', contact_info={'tel': '03-8888-9999'}, address='東京都', contact_person_name='担当者G')
        owner = Owner.objects.create(name='契約オーナー2', contact_info={'tel': '090-8888-9999'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='契約物件2', property_type='Apartment', year_built=2018)
        ct = ConstructionType.objects.create(name='契約工事種別2')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        estimate = Estimate.objects.create(case=case, total_amount=2000000, approval_status='Approved')
        contract = Contract.objects.create(case=case, estimate=estimate, contract_type='Order', contract_date='2024-06-01', contract_amount=2000000, approval_status='Pending', customer_confirmation_status='Required')
        data = {
            'case': case.id,
            'estimate': estimate.id,
            'contract_type': 'Contract',
            'contract_date': '2024-07-01',
            'contract_amount': '3000000.00',
            'approval_status': 'Approved',
            'customer_confirmation_status': 'CompletedOK'
        }
        response = self.auth_put(f'/api/contracts/{contract.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contract.refresh_from_db()
        self.assertEqual(contract.contract_type, 'Contract')

    def test_contract_delete(self):
        company = Company.objects.create(name='契約会社3', contact_info={'tel': '03-9999-0000'}, address='東京都', contact_person_name='担当者H')
        owner = Owner.objects.create(name='契約オーナー3', contact_info={'tel': '090-9999-0000'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='契約物件3', property_type='Apartment', year_built=2019)
        ct = ConstructionType.objects.create(name='契約工事種別3')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        estimate = Estimate.objects.create(case=case, total_amount=3000000)
        contract = Contract.objects.create(case=case, estimate=estimate, contract_type='Order', contract_date='2024-06-01', contract_amount=3000000, approval_status='Pending', customer_confirmation_status='Required')
        response = self.auth_delete(f'/api/contracts/{contract.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contract.objects.filter(id=contract.id).exists())

    def test_estimate_create(self):
        company = Company.objects.create(name='見積会社', contact_info={'tel': '03-1111-2222'}, address='東京都', contact_person_name='担当者I')
        owner = Owner.objects.create(name='見積オーナー', contact_info={'tel': '090-1111-2222'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='見積物件', property_type='Apartment', year_built=2020)
        ct = ConstructionType.objects.create(name='見積工事種別')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        data = {
            'case': case.id,
            'total_amount': '500000.00',
            'approval_status': 'Pending'
        }
        response = self.auth_post('/api/estimates/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estimate.objects.filter(case=case).count(), 1)

    def test_estimate_create_validation_error(self):
        data = {'total_amount': '500000.00'}  # caseがない
        response = self.auth_post('/api/estimates/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_estimate_update(self):
        company = Company.objects.create(name='見積会社2', contact_info={'tel': '03-2222-3333'}, address='東京都', contact_person_name='担当者J')
        owner = Owner.objects.create(name='見積オーナー2', contact_info={'tel': '090-2222-3333'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='見積物件2', property_type='Apartment', year_built=2021)
        ct = ConstructionType.objects.create(name='見積工事種別2')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        estimate = Estimate.objects.create(case=case, total_amount=800000)
        data = {
            'case': case.id,
            'total_amount': '900000.00',
            'approval_status': 'Approved'
        }
        response = self.auth_put(f'/api/estimates/{estimate.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        estimate.refresh_from_db()
        self.assertEqual(str(estimate.total_amount), '900000.00')

    def test_estimate_delete(self):
        company = Company.objects.create(name='見積会社3', contact_info={'tel': '03-3333-4444'}, address='東京都', contact_person_name='担当者K')
        owner = Owner.objects.create(name='見積オーナー3', contact_info={'tel': '090-3333-4444'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='見積物件3', property_type='Apartment', year_built=2022)
        ct = ConstructionType.objects.create(name='見積工事種別3')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        estimate = Estimate.objects.create(case=case, total_amount=1000000)
        response = self.auth_delete(f'/api/estimates/{estimate.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Estimate.objects.filter(id=estimate.id).exists())

    def test_schedule_create(self):
        company = Company.objects.create(name='スケジュール会社', contact_info={'tel': '03-4444-5555'}, address='東京都', contact_person_name='担当者L')
        owner = Owner.objects.create(name='スケジュールオーナー', contact_info={'tel': '090-4444-5555'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='スケジュール物件', property_type='Apartment', year_built=2023)
        ct = ConstructionType.objects.create(name='スケジュール工事種別')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        data = {
            'case': case.id,
            'assigned_to': self.user.id,
            'schedule_date': '2024-07-01',
            'start_time': '10:00:00',
            'end_time': '12:00:00',
            'type': 'Appointment',
            'location': '現地',
            'details': '現地調査アポイント'
        }
        response = self.auth_post('/api/schedules/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.filter(case=case).count(), 1)

    def test_schedule_create_validation_error(self):
        data = {'schedule_date': '2024-07-01'}  # 必須項目不足
        response = self.auth_post('/api/schedules/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_schedule_update(self):
        company = Company.objects.create(name='スケジュール会社2', contact_info={'tel': '03-5555-6666'}, address='東京都', contact_person_name='担当者M')
        owner = Owner.objects.create(name='スケジュールオーナー2', contact_info={'tel': '090-5555-6666'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='スケジュール物件2', property_type='Apartment', year_built=2024)
        ct = ConstructionType.objects.create(name='スケジュール工事種別2')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        schedule = Schedule.objects.create(case=case, assigned_to=self.user, schedule_date='2024-07-01', start_time='10:00:00', end_time='12:00:00', type='Appointment', location='現地', details='旧アポイント')
        data = {
            'case': case.id,
            'assigned_to': self.user.id,
            'schedule_date': '2024-07-02',
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'type': 'Construction',
            'location': '現地',
            'details': '施工予定'
        }
        response = self.auth_put(f'/api/schedules/{schedule.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule.refresh_from_db()
        self.assertEqual(schedule.type, 'Construction')

    def test_schedule_delete(self):
        company = Company.objects.create(name='スケジュール会社3', contact_info={'tel': '03-6666-7777'}, address='東京都', contact_person_name='担当者N')
        owner = Owner.objects.create(name='スケジュールオーナー3', contact_info={'tel': '090-6666-7777'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='スケジュール物件3', property_type='Apartment', year_built=2025)
        ct = ConstructionType.objects.create(name='スケジュール工事種別3')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        schedule = Schedule.objects.create(case=case, assigned_to=self.user, schedule_date='2024-07-01', start_time='10:00:00', end_time='12:00:00', type='Appointment', location='現地', details='削除アポイント')
        response = self.auth_delete(f'/api/schedules/{schedule.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Schedule.objects.filter(id=schedule.id).exists())

    def test_businessalliance_create(self):
        company = Company.objects.create(name='提携会社', contact_info={'tel': '03-8888-1111'}, address='東京都', contact_person_name='担当者O')
        data = {
            'company': company.id,
            'start_date': '2024-01-01',
            'referral_commission_rate': '5.0',
            'contract_info': '契約書A'
        }
        response = self.auth_post('/api/business-alliances/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessAlliance.objects.filter(company=company).count(), 1)

    def test_businessalliance_create_validation_error(self):
        data = {'referral_commission_rate': '5.0'}  # company, start_dateがない
        response = self.auth_post('/api/business-alliances/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_businessalliance_update(self):
        company = Company.objects.create(name='提携会社2', contact_info={'tel': '03-9999-2222'}, address='東京都', contact_person_name='担当者P')
        alliance = BusinessAlliance.objects.create(company=company, start_date='2024-01-01', referral_commission_rate=5.0, contract_info='契約書A')
        data = {
            'company': company.id,
            'start_date': '2024-02-01',
            'referral_commission_rate': '7.5',
            'contract_info': '契約書B'
        }
        response = self.auth_put(f'/api/business-alliances/{alliance.id}/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alliance.refresh_from_db()
        self.assertEqual(str(alliance.referral_commission_rate), '7.50')

    def test_businessalliance_delete(self):
        company = Company.objects.create(name='提携会社3', contact_info={'tel': '03-0000-3333'}, address='東京都', contact_person_name='担当者Q')
        alliance = BusinessAlliance.objects.create(company=company, start_date='2024-01-01', referral_commission_rate=5.0, contract_info='契約書A')
        response = self.auth_delete(f'/api/business-alliances/{alliance.id}/', use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BusinessAlliance.objects.filter(id=alliance.id).exists())

    def test_surveyrecord_create(self):
        company = Company.objects.create(name='調査会社', contact_info={'tel': '03-5555-1111'}, address='東京都', contact_person_name='担当者R')
        owner = Owner.objects.create(name='調査オーナー', contact_info={'tel': '090-5555-1111'}, address='東京都', assigned_sales=self.sales_user)
        prop = Property.objects.create(owner=owner, company=company, address='調査物件', property_type='Apartment', year_built=2022)
        ct = ConstructionType.objects.create(name='調査工事種別')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        data = {
            'case': case.id,
            'survey_date': '2024-07-01',
            'assigned_to': self.sales_user.id,
            'summary': '現地調査実施',
            'details': '特に問題なし',
            'attachment_paths': ['photo1.jpg', 'photo2.jpg']
        }
        response = self.auth_post('/api/surveyrecords/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyRecord.objects.filter(case=case).count(), 1)

    def test_surveyrecord_create_validation_error(self):
        data = {'summary': '現地調査実施'}  # 必須項目不足
        response = self.auth_post('/api/surveyrecords/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_surveyrecord_update(self):
        company = Company.objects.create(name='調査会社2', contact_info={'tel': '03-6666-2222'}, address='東京都', contact_person_name='担当者S')
        owner = Owner.objects.create(name='調査オーナー2', contact_info={'tel': '090-6666-2222'}, address='東京都', assigned_sales=self.sales_user)
        prop = Property.objects.create(owner=owner, company=company, address='調査物件2', property_type='Apartment', year_built=2023)
        ct = ConstructionType.objects.create(name='調査工事種別2')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        record = SurveyRecord.objects.create(case=case, survey_date='2024-07-01', assigned_to=self.sales_user, summary='旧調査', details='旧詳細', attachment_paths=['old.jpg'])
        data = {
            'case': case.id,
            'survey_date': '2024-07-02',
            'assigned_to': self.sales_user.id,
            'summary': '新調査',
            'details': '新しい詳細',
            'attachment_paths': ['new.jpg']
        }
        response = self.auth_put(f'/api/surveyrecords/{record.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.summary, '新調査')

    def test_surveyrecord_delete(self):
        company = Company.objects.create(name='調査会社3', contact_info={'tel': '03-7777-3333'}, address='東京都', contact_person_name='担当者T')
        owner = Owner.objects.create(name='調査オーナー3', contact_info={'tel': '090-7777-3333'}, address='東京都', assigned_sales=self.sales_user)
        prop = Property.objects.create(owner=owner, company=company, address='調査物件3', property_type='Apartment', year_built=2024)
        ct = ConstructionType.objects.create(name='調査工事種別3')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        record = SurveyRecord.objects.create(case=case, survey_date='2024-07-01', assigned_to=self.sales_user, summary='削除調査', details='削除詳細', attachment_paths=['del.jpg'])
        response = self.auth_delete(f'/api/surveyrecords/{record.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SurveyRecord.objects.filter(id=record.id).exists())

    def test_reportrecord_create(self):
        company = Company.objects.create(name='報告会社', contact_info={'tel': '03-8888-1111'}, address='東京都', contact_person_name='担当者U')
        owner = Owner.objects.create(name='報告オーナー', contact_info={'tel': '090-8888-1111'}, address='東京都', assigned_sales=self.sales_user)
        prop = Property.objects.create(owner=owner, company=company, address='報告物件', property_type='Apartment', year_built=2022)
        ct = ConstructionType.objects.create(name='報告工事種別')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        data = {
            'case': case.id,
            'report_date': '2024-07-01',
            'assigned_to': self.sales_user.id,
            'negotiation_content': '商談内容A',
            'result': 'Won'
        }
        response = self.auth_post('/api/reportrecords/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReportRecord.objects.filter(case=case).count(), 1)

    def test_reportrecord_create_validation_error(self):
        data = {'negotiation_content': '商談内容A'}  # 必須項目不足
        response = self.auth_post('/api/reportrecords/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reportrecord_update(self):
        company = Company.objects.create(name='報告会社2', contact_info={'tel': '03-9999-2222'}, address='東京都', contact_person_name='担当者V')
        owner = Owner.objects.create(name='報告オーナー2', contact_info={'tel': '090-9999-2222'}, address='東京都', assigned_sales=self.sales_user)
        prop = Property.objects.create(owner=owner, company=company, address='報告物件2', property_type='Apartment', year_built=2023)
        ct = ConstructionType.objects.create(name='報告工事種別2')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        record = ReportRecord.objects.create(case=case, report_date='2024-07-01', assigned_to=self.sales_user, negotiation_content='旧商談', result='Ongoing')
        data = {
            'case': case.id,
            'report_date': '2024-07-02',
            'assigned_to': self.sales_user.id,
            'negotiation_content': '新商談',
            'result': 'Lost'
        }
        response = self.auth_put(f'/api/reportrecords/{record.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.result, 'Lost')

    def test_reportrecord_delete(self):
        company = Company.objects.create(name='報告会社3', contact_info={'tel': '03-0000-3333'}, address='東京都', contact_person_name='担当者W')
        owner = Owner.objects.create(name='報告オーナー3', contact_info={'tel': '090-0000-3333'}, address='東京都', assigned_sales=self.sales_user)
        prop = Property.objects.create(owner=owner, company=company, address='報告物件3', property_type='Apartment', year_built=2024)
        ct = ConstructionType.objects.create(name='報告工事種別3')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        record = ReportRecord.objects.create(case=case, report_date='2024-07-01', assigned_to=self.sales_user, negotiation_content='削除商談', result='Ongoing')
        response = self.auth_delete(f'/api/reportrecords/{record.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ReportRecord.objects.filter(id=record.id).exists())

    def test_user_create(self):
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'employee_number': '2000',
            'role': 'Sales',
            'status': 'Active',
            'is_first_login': True
        }
        response = self.auth_post('/api/users/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_user_create_validation_error(self):
        data = {'username': 'nouser'}  # 必須項目不足
        response = self.auth_post('/api/users/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update(self):
        user = User.objects.create_user(username='updateuser', password='updatepass', employee_number='2001', role='Sales')
        data = {
            'username': 'updateduser',
            'employee_number': '2001',
            'role': 'HQ',
            'status': 'Inactive',
            'is_first_login': False
        }
        response = self.auth_put(f'/api/users/{user.id}/', data, use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.role, 'HQ')

    def test_user_delete(self):
        user = User.objects.create_user(username='deluser', password='delpass', employee_number='2002', role='Sales')
        response = self.auth_delete(f'/api/users/{user.id}/', use_hq=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_user_permission_error(self):
        # Salesユーザーでユーザー作成は403になる
        data = {
            'username': 'forbiddenuser',
            'password': 'forbidpass',
            'employee_number': '2003',
            'role': 'Sales',
            'status': 'Active',
            'is_first_login': True
        }
        response = self.auth_post('/api/users/', data, use_hq=False)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_create_with_unapproved_estimate(self):
        company = Company.objects.create(name='契約会社X', contact_info={'tel': '03-7777-8888'}, address='東京都', contact_person_name='担当者F')
        owner = Owner.objects.create(name='契約オーナーX', contact_info={'tel': '090-7777-8888'}, address='東京都', assigned_sales=self.user)
        prop = Property.objects.create(owner=owner, company=company, address='契約物件X', property_type='Apartment', year_built=2017)
        ct = ConstructionType.objects.create(name='契約工事種別X')
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        case.expected_construction_types.set([ct])
        # 未承認の見積書
        estimate = Estimate.objects.create(case=case, total_amount=1000000, approval_status='Pending')
        data = {
            'case': case.id,
            'estimate': estimate.id,
            'contract_type': 'Order',
            'contract_date': '2024-06-01',
            'contract_amount': '1000000.00',
            'approval_status': 'Pending',
            'customer_confirmation_status': 'Required'
        }
        response = self.auth_post('/api/contracts/', data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('見積書が承認済みでないと契約書を作成できません', response.content.decode())

class ModelStrTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='struser', password='strpass', employee_number='9999', role='HQ')
        self.user_no_empnum = User.objects.create_user(username='noemp', password='strpass', employee_number='', role='HQ')
        self.company = Company.objects.create(name='str会社', contact_info={'tel': '03-0000-0000'}, address='東京都', contact_person_name='担当者')
        self.owner = Owner.objects.create(name='strオーナー', contact_info={'tel': '090-0000-0000'}, address='東京都', assigned_sales=self.user)
        self.prop = Property.objects.create(owner=self.owner, company=self.company, address='str物件', property_type='Apartment', year_built=2020)
        self.ct = ConstructionType.objects.create(name='str工事種別')
        self.case = Case.objects.create(owner=self.owner, property=self.prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        self.case.expected_construction_types.set([self.ct])
        self.estimate = Estimate.objects.create(case=self.case, total_amount=1000, approval_status='Approved')
        self.estimate_item = EstimateItem.objects.create(estimate=self.estimate, item_name='テスト明細', quantity=2, unit_price=100, subtotal=200)
        self.contract = Contract.objects.create(case=self.case, estimate=self.estimate, contract_type='Order', contract_date='2024-06-01', contract_amount=1000, approval_status='Pending', customer_confirmation_status='Required')
        self.contract_item = ContractItem.objects.create(contract=self.contract, item_name='契約明細', quantity=1, unit_price=1000, subtotal=1000)
        self.schedule = Schedule.objects.create(case=self.case, assigned_to=self.user, schedule_date='2024-07-01', start_time='10:00:00', end_time='12:00:00', type='Appointment', location='現地', details='str詳細')
        self.survey = SurveyRecord.objects.create(case=self.case, survey_date='2024-07-01', assigned_to=self.user, summary='検索概要', details='検索詳細', attachment_paths=['a.jpg'])
        self.report = ReportRecord.objects.create(case=self.case, report_date='2024-07-01', assigned_to=self.user, negotiation_content='検索商談', result='Won')
        self.alliance = BusinessAlliance.objects.create(company=self.company, start_date='2024-01-01', referral_commission_rate=5.0, contract_info='str契約')

    def test_user_str(self):
        self.assertEqual(str(self.user), '9999')
    def test_user_str_no_employee_number(self):
        self.assertEqual(str(self.user_no_empnum), 'noemp')
    def test_owner_str(self):
        self.assertEqual(str(self.owner), 'strオーナー')
    def test_company_str(self):
        self.assertEqual(str(self.company), 'str会社')
    def test_property_str(self):
        self.assertEqual(str(self.prop), 'str物件')
    def test_constructiontype_str(self):
        self.assertEqual(str(self.ct), 'str工事種別')
    def test_case_str(self):
        s = str(self.case)
        self.assertIn('Case', s)
        self.assertIn('New', s)
    def test_estimate_str(self):
        self.assertTrue(str(self.estimate))
    def test_estimateitem_str(self):
        self.assertIn('Item', str(self.estimate_item))
        self.assertIn('Estimate', str(self.estimate_item))
    def test_contract_str(self):
        self.assertTrue(str(self.contract))
    def test_contractitem_str(self):
        self.assertIn('Item', str(self.contract_item))
        self.assertIn('Contract', str(self.contract_item))
    def test_schedule_str(self):
        self.assertTrue(str(self.schedule))
    def test_surveyrecord_str(self):
        self.assertTrue(str(self.survey))
    def test_reportrecord_str(self):
        self.assertTrue(str(self.report))
    def test_businessalliance_str(self):
        self.assertTrue(str(self.alliance))

class ApproveActionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.hq_user = User.objects.create_user(username='hqapprove', password='hqpass', employee_number='3000', role='HQ')
        self.sales_user = User.objects.create_user(username='salesapprove', password='salespass', employee_number='3001', role='Sales')
        self.hq_token, _ = Token.objects.get_or_create(user=self.hq_user)
        self.sales_token, _ = Token.objects.get_or_create(user=self.sales_user)
        self.company = Company.objects.create(name='承認会社', contact_info={'tel': '03-0000-0000'}, address='東京都', contact_person_name='担当者')
        self.owner = Owner.objects.create(name='承認オーナー', contact_info={'tel': '090-0000-0000'}, address='東京都', assigned_sales=self.sales_user)
        self.prop = Property.objects.create(owner=self.owner, company=self.company, address='承認物件', property_type='Apartment', year_built=2020)
        self.ct = ConstructionType.objects.create(name='承認工事種別')
        self.case = Case.objects.create(owner=self.owner, property=self.prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        self.case.expected_construction_types.set([self.ct])
        self.estimate = Estimate.objects.create(case=self.case, total_amount=1000, approval_status='Approved', approver=self.hq_user, approval_date=date.today())
        self.contract = Contract.objects.create(case=self.case, estimate=self.estimate, contract_type='Order', contract_date='2024-06-01', contract_amount=1000, approval_status='Approved', approver=self.hq_user, approval_date=date.today(), customer_confirmation_status='Required')

    def test_estimate_approve_already_approved(self):
        url = f'/api/estimates/{self.estimate.id}/approve/'
        response = self.client.post(url, HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('既に承認済み', response.content.decode())

    def test_contract_approve_already_approved(self):
        url = f'/api/contracts/{self.contract.id}/approve/'
        response = self.client.post(url, HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('既に承認済み', response.content.decode())

class SerializerEdgeCaseTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='seruser', password='serpass', employee_number='8888', role='HQ')
        self.company = Company.objects.create(name='ser会社', contact_info={'tel': '03-0000-0000'}, address='東京都', contact_person_name='担当者')
        self.owner = Owner.objects.create(name='serオーナー', contact_info={'tel': '090-0000-0000'}, address='東京都', assigned_sales=self.user)
        self.prop = Property.objects.create(owner=self.owner, company=self.company, address='ser物件', property_type='Apartment', year_built=2020)
        self.ct = ConstructionType.objects.create(name='ser工事種別')
        self.case = Case.objects.create(owner=self.owner, property=self.prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        self.case.expected_construction_types.set([self.ct])
        self.estimate = Estimate.objects.create(case=self.case, total_amount=1000, approval_status='Approved')
        self.contract = Contract.objects.create(case=self.case, estimate=self.estimate, contract_type='Order', contract_date='2024-06-01', contract_amount=1000, approval_status='Pending', customer_confirmation_status='Required')

    def test_contract_serializer_estimate_none(self):
        data = {
            'case': self.case.id,
            'estimate': None,
            'contract_type': 'Order',
            'contract_date': '2024-06-01',
            'contract_amount': '1000.00',
            'approval_status': 'Pending',
            'customer_confirmation_status': 'Required'
        }
        serializer = ContractSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('契約書作成には関連する見積書が必要です。', str(serializer.errors))

    def test_user_serializer_update_with_password(self):
        user = User.objects.create_user(username='updatepw', password='oldpass', employee_number='7777', role='Sales')
        data = {
            'username': 'updatepw',
            'employee_number': '7777',
            'role': 'Sales',
            'status': 'Active',
            'is_first_login': False,
            'password': 'newpass123'
        }
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password('newpass123'))

class PermissionEdgeCaseTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.hq = User.objects.create_user(username='hq', password='pass', employee_number='1', role='HQ')
        self.sales = User.objects.create_user(username='sales', password='pass', employee_number='2', role='Sales')
        self.cons = User.objects.create_user(username='cons', password='pass', employee_number='3', role='Construction')
        self.anon = None

    def _get_req(self, user, method='GET'):
        req = self.factory.generic(method, '/')
        force_authenticate(req, user=user)
        return Request(req)

    def test_is_hq_user(self):
        req = self._get_req(self.hq)
        self.assertTrue(IsHQUser().has_permission(req, None))
        req = self._get_req(self.sales)
        self.assertFalse(IsHQUser().has_permission(req, None))

    def test_is_sales_user(self):
        req = self._get_req(self.sales)
        self.assertTrue(IsSalesUser().has_permission(req, None))
        req = self._get_req(self.hq)
        self.assertFalse(IsSalesUser().has_permission(req, None))

    def test_is_construction_user(self):
        req = self._get_req(self.cons)
        self.assertTrue(IsConstructionUser().has_permission(req, None))
        req = self._get_req(self.hq)
        self.assertFalse(IsConstructionUser().has_permission(req, None))

    def test_is_sales_or_hq_user(self):
        req = self._get_req(self.sales)
        self.assertTrue(IsSalesOrHQUser().has_permission(req, None))
        req = self._get_req(self.hq)
        self.assertTrue(IsSalesOrHQUser().has_permission(req, None))
        req = self._get_req(self.cons)
        self.assertFalse(IsSalesOrHQUser().has_permission(req, None))

    def test_is_sales_or_construction_user(self):
        req = self._get_req(self.sales)
        self.assertTrue(IsSalesOrConstructionUser().has_permission(req, None))
        req = self._get_req(self.cons)
        self.assertTrue(IsSalesOrConstructionUser().has_permission(req, None))
        req = self._get_req(self.hq)
        self.assertFalse(IsSalesOrConstructionUser().has_permission(req, None))

    def test_is_hq_or_construction_user(self):
        req = self._get_req(self.hq)
        self.assertTrue(IsHQOrConstructionUser().has_permission(req, None))
        req = self._get_req(self.cons)
        self.assertTrue(IsHQOrConstructionUser().has_permission(req, None))
        req = self._get_req(self.sales)
        self.assertFalse(IsHQOrConstructionUser().has_permission(req, None))

    def test_is_authenticated_read_only(self):
        req = self._get_req(self.hq, method='GET')
        self.assertTrue(IsAuthenticatedReadOnly().has_permission(req, None))
        req = self._get_req(self.hq, method='POST')
        self.assertFalse(IsAuthenticatedReadOnly().has_permission(req, None))
        req.user.is_superuser = True
        self.assertTrue(IsAuthenticatedReadOnly().has_permission(req, None))

class ViewSetPermissionEdgeCaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.hq = User.objects.create_user(username='hq2', password='pass', employee_number='11', role='HQ')
        self.sales = User.objects.create_user(username='sales2', password='pass', employee_number='12', role='Sales')
        self.cons = User.objects.create_user(username='cons2', password='pass', employee_number='13', role='Construction')
        self.hq_token, _ = Token.objects.get_or_create(user=self.hq)
        self.sales_token, _ = Token.objects.get_or_create(user=self.sales)
        self.cons_token, _ = Token.objects.get_or_create(user=self.cons)
        self.company = Company.objects.create(name='権限会社', contact_info={'tel': '03-0000-0000'}, address='東京都', contact_person_name='担当者')

    def test_company_create_forbidden_for_sales(self):
        data = {'name': 'NG会社', 'contact_info': {'tel': '03-0000-0000'}, 'address': '東京都', 'contact_person_name': '担当者'}
        response = self.client.post('/api/companies/', data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {self.sales_token.key}')
        self.assertEqual(response.status_code, 403)

    def test_property_create_forbidden_for_hq(self):
        # HQはPropertyのcreate権限なし
        owner = Owner.objects.create(name='権限オーナー', contact_info={'tel': '090-0000-0000'}, address='東京都', assigned_sales=self.sales)
        data = {'owner': owner.id, 'company': self.company.id, 'address': '東京都', 'property_type': 'Apartment', 'year_built': 2020}
        response = self.client.post('/api/properties/', data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(response.status_code, 403)

    def test_schedule_create_forbidden_for_hq(self):
        # HQはScheduleのcreate権限なし
        owner = Owner.objects.create(name='権限オーナー2', contact_info={'tel': '090-0000-0000'}, address='東京都', assigned_sales=self.sales)
        prop = Property.objects.create(owner=owner, company=self.company, address='東京都', property_type='Apartment', year_built=2020)
        case = Case.objects.create(owner=owner, property=prop, assigned_sales=self.sales, case_type='New', status='Appointment', occurence_date='2024-01-01')
        data = {'case': case.id, 'assigned_to': self.sales.id, 'schedule_date': '2024-07-01', 'start_time': '10:00:00', 'end_time': '12:00:00', 'type': 'Appointment', 'location': '現地', 'details': '詳細'}
        response = self.client.post('/api/schedules/', data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(response.status_code, 403)

class ViewSearchFilterOrderingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='searchuser', password='searchpass', employee_number='100', role='Sales')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.company = Company.objects.create(name='検索会社', contact_info={'tel': '03-0000-0000'}, address='東京都', contact_person_name='担当者')
        self.owner = Owner.objects.create(name='検索オーナー', contact_info={'tel': '090-0000-0000'}, address='東京都', assigned_sales=self.user)
        self.prop = Property.objects.create(owner=self.owner, company=self.company, address='検索物件', property_type='Apartment', year_built=2020)
        self.ct = ConstructionType.objects.create(name='検索工事種別')
        self.case = Case.objects.create(owner=self.owner, property=self.prop, assigned_sales=self.user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        self.case.expected_construction_types.set([self.ct])
        self.schedule = Schedule.objects.create(case=self.case, assigned_to=self.user, schedule_date='2024-07-01', start_time='10:00:00', end_time='12:00:00', type='Appointment', location='現地', details='検索詳細')
        self.survey = SurveyRecord.objects.create(case=self.case, survey_date='2024-07-01', assigned_to=self.user, summary='検索概要', details='検索詳細', attachment_paths=['a.jpg'])
        self.report = ReportRecord.objects.create(case=self.case, report_date='2024-07-01', assigned_to=self.user, negotiation_content='検索商談', result='Won')

    def auth_get(self, url, params=None):
        return self.client.get(url, params or {}, HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_schedule_search(self):
        response = self.auth_get('/api/schedules/', {'search': '検索詳細'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('検索詳細', response.content.decode())

    def test_schedule_filter(self):
        response = self.auth_get('/api/schedules/', {'schedule_date': '2024-07-01'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('2024-07-01', response.content.decode())

    def test_schedule_ordering(self):
        response = self.auth_get('/api/schedules/', {'ordering': '-schedule_date'})
        self.assertEqual(response.status_code, 200)

    def test_surveyrecord_filter(self):
        response = self.auth_get('/api/surveyrecords/', {'survey_date': '2024-07-01'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('2024-07-01', response.content.decode())

    def test_reportrecord_filter(self):
        response = self.auth_get('/api/reportrecords/', {'report_date': '2024-07-01'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('2024-07-01', response.content.decode())

    def test_surveyrecord_search_summary(self):
        response = self.auth_get('/api/surveyrecords/', {'search': '検索概要'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('検索概要', response.content.decode())

    def test_reportrecord_search_negotiation_content(self):
        response = self.auth_get('/api/reportrecords/', {'search': '検索商談'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('検索商談', response.content.decode())

class CustomAuthTokenTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='authtest', password='authpass', employee_number='200', role='Sales')

    def test_auth_token_success(self):
        view = CustomAuthToken.as_view()
        data = {'username': 'authtest', 'password': 'authpass'}
        request = self.factory.post('/api/token/', data)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_auth_token_fail(self):
        view = CustomAuthToken.as_view()
        data = {'username': 'authtest', 'password': 'wrongpass'}
        request = self.factory.post('/api/token/', data)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', str(response.data))

class NewFeatureTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.hq_user = User.objects.create_user(username='hq2', password='hqpass2', employee_number='2000', role='HQ')
        self.sales_user = User.objects.create_user(username='sales2', password='salespass2', employee_number='2001', role='Sales')
        self.hq_token, _ = Token.objects.get_or_create(user=self.hq_user)
        self.sales_token, _ = Token.objects.get_or_create(user=self.sales_user)
        self.owner = Owner.objects.create(name='履歴オーナー', contact_info={'tel': '1'}, address='A', assigned_sales=self.sales_user)
        self.company = Company.objects.create(name='履歴会社', contact_info={'tel': '2'}, address='B', contact_person_name='担当')
        self.prop = Property.objects.create(owner=self.owner, company=self.company, address='履歴物件', property_type='Apartment', year_built=2020)
        self.case = Case.objects.create(owner=self.owner, property=self.prop, assigned_sales=self.sales_user, case_type='New', status='Appointment', occurence_date='2024-01-01')
        self.estimate = Estimate.objects.create(case=self.case, total_amount=1000)
        self.contract = Contract.objects.create(case=self.case, estimate=self.estimate, contract_type='Order', contract_date='2024-01-02', contract_amount=1000)

    def auth_get(self, url, use_hq=False):
        token = self.hq_token.key if use_hq else self.sales_token.key
        return self.client.get(url, HTTP_AUTHORIZATION=f'Token {token}')

    def auth_post(self, url, data, use_hq=False):
        token = self.hq_token.key if use_hq else self.sales_token.key
        return self.client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {token}')

    def test_estimate_history_and_rollback(self):
        # 見積書を更新して履歴を作る
        url = f'/api/estimates/{self.estimate.id}/'
        data = {'case': self.case.id, 'total_amount': 2000}
        self.auth_put = lambda url, data, use_hq=False: self.client.put(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        resp = self.auth_put(url, data, use_hq=True)
        self.assertEqual(resp.status_code, 200)
        # 履歴一覧取得
        resp = self.auth_get(f'/api/estimates/{self.estimate.id}/histories/', use_hq=True)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()), 1)
        # ロールバック
        history_id = resp.json()[0]['id']
        resp = self.client.post(f'/api/estimates/{self.estimate.id}/histories/{history_id}/rollback/', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('estimate', resp.json())

    def test_contract_history_and_rollback(self):
        # 契約書を更新して履歴を作る
        url = f'/api/contracts/{self.contract.id}/'
        data = {'case': self.case.id, 'estimate': self.estimate.id, 'contract_type': 'Order', 'contract_date': '2024-01-03', 'contract_amount': 3000}
        self.auth_put = lambda url, data, use_hq=False: self.client.put(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        resp = self.auth_put(url, data, use_hq=True)
        self.assertEqual(resp.status_code, 200)
        # 履歴一覧取得
        resp = self.auth_get(f'/api/contracts/{self.contract.id}/histories/', use_hq=True)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()), 1)
        # ロールバック
        history_id = resp.json()[0]['id']
        resp = self.client.post(f'/api/contracts/{self.contract.id}/histories/{history_id}/rollback/', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('contract', resp.json())

    def test_asbestos_survey_crud(self):
        # 作成
        data = {'case': self.case.id, 'survey_date': '2024-07-01', 'inspector': self.hq_user.id, 'result': 'OK'}
        resp = self.auth_post('/api/asbestos-surveys/', data, use_hq=True)
        self.assertEqual(resp.status_code, 201)
        survey_id = resp.json()['id']
        # 取得
        resp = self.auth_get(f'/api/asbestos-surveys/{survey_id}/', use_hq=True)
        self.assertEqual(resp.status_code, 200)
        # 更新
        data['result'] = 'NG'
        resp = self.client.put(f'/api/asbestos-surveys/{survey_id}/', data, content_type='application/json', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(resp.status_code, 200)
        # 削除
        resp = self.client.delete(f'/api/asbestos-surveys/{survey_id}/', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(resp.status_code, 204)

    def test_revenue_cost_crud_and_filter(self):
        # 作成
        data = {'case': self.case.id, 'revenue': 10000, 'cost': 5000}
        resp = self.auth_post('/api/revenue-costs/', data, use_hq=True)
        self.assertEqual(resp.status_code, 201)
        rc_id = resp.json()['id']
        # 取得
        resp = self.auth_get(f'/api/revenue-costs/{rc_id}/', use_hq=True)
        self.assertEqual(resp.status_code, 200)
        # 検索
        resp = self.auth_get(f'/api/revenue-costs/?revenue__gte=5000', use_hq=True)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()), 1)
        # 削除
        resp = self.client.delete(f'/api/revenue-costs/{rc_id}/', HTTP_AUTHORIZATION=f'Token {self.hq_token.key}')
        self.assertEqual(resp.status_code, 204)
