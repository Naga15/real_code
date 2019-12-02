from django.test import TestCase
from .models import CEPData, SLCase, Claim, Fault_Code
import uuid
from datetime import datetime
from datetime import date

class CEPTest(TestCase):

    def testFields(self):
        cep = CEPData()
        cep.ESN = 'It is a proof of membership in an ESN section and so indirectly of the ESN Network.'
        cep.Chassis = 'vehicle which is also known as Frame. It bears all the stresses on the vehicle in both static and dynamic conditions.'
        cep.save()
        record = CEPData.objects.get(pk=1)
        self.assertEqual(record, cep)

    def test_esn_on_save(self):
        cep = CEPData()
        cep.ESN = 'The ESNcard can be obtained exclusively from your ESN local section. '
        cep.Chassis = 'Find here online price details of companies selling Car Chassis.'
        cep.save()
        self.assertEqual(cep.ESN, 'The ESNcard can be obtained exclusively from your ESN local section. ')

    def test_chassis_on_save(self):
        cep = CEPData()
        cep.ESN = 'The ESNcard is also used as a discount card in many cities and countries around Europe. '
        cep.Chassis = 'Chassis is a collective term for all the parts of a vehicle except the body work.'
        cep.save()
        self.assertEqual(cep.Chassis, 'Chassis is a collective term for all the parts of a vehicle except the body work.')

class SLCaseTest(TestCase):

    def test_SLCaseFields(self):
        slcase = SLCase()
        slcase.SLID = '2'
        slcase.Disposition = 'Disposition'
        slcase.Message = 'Message 1'
        slcase.save()
        record = SLCase.objects.get(pk=1)
        self.assertEqual(record, slcase)

    def test_slcase_SLID_on_save(self):
        slcase = SLCase()
        slcase.SLID = '3'
        slcase.Disposition = 'Disposition 2'
        slcase.Message = 'Message 2'
        slcase.save()
        self.assertEqual(slcase.Disposition, 'Disposition 2')

    def test_plantdata_application_on_save(self):
        slcase = SLCase()
        slcase.SLID = '3'
        slcase.Disposition = 'Disposition 3'
        slcase.Message = 'Message 3'
        slcase.save()
        self.assertEqual(slcase.Message, 'Message 3')
        self.assertEqual(slcase.SLID, '3')

class ClaimTest(TestCase):

    def test_ClaimTestFields(self):
        claimtest = Claim()
        claimtest.Dealer_Story = 'This is dealer story'
        claimtest.Cost_Parts = 'Parts 1'
        claimtest.Cost_Total = 'Cost total 123456'
        claimtest.PR_Part_No = 'PR Part Number 1'
        claimtest.PR_Part_Desc = 'The codes were created by the Society of Automotive Engineers (SAE) to comply with OBD-II emissions regulations in the US.'
        claimtest.PR_Part_Amount = 'PR Amount 1'
        claimtest.save()
        record = Claim.objects.get(pk=1)
        self.assertEqual(record, claimtest)

    def test_ClaimTest_Cost_Parts(self):
        claimtest = Claim()
        claimtest.Dealer_Story = 'I receive a long talk describing how I should buy the replacement insurance.'
        claimtest.Cost_Parts = 'Parts-2'
        claimtest.Cost_Total = 'Cost total'
        claimtest.PR_Part_No = 'PR Part Number'
        claimtest.PR_Part_Desc = 'Something is wrong with our car but what? The vehicle seems to be running fine.'
        claimtest.PR_Part_Amount = 'PR Amount'
        claimtest.save()
        self.assertEqual(claimtest.Cost_Parts, 'Parts-2')

    def test_ClaimTest_PR_Part_Description(self):
        claimtest = Claim()
        claimtest.Dealer_Story = 'However, after this buying experience, I lost pretty much any respect and sympathy for the dealers.'
        claimtest.PR_Part_Desc = 'The trouble code, or diagnostic code, is an alphanumeric value that corresponds to a particular problem.'
        claimtest.save()
        self.assertEqual(claimtest.PR_Part_Desc, 'The trouble code, or diagnostic code, is an alphanumeric value that corresponds to a particular problem.')

    def test_ClaimTest_Dealer_Story(self):
        claimtest = Claim()
        claimtest.Dealer_Story = 'I enter a dealership, with the intention of exploring a car'
        claimtest.save()
        self.assertEqual(claimtest.Dealer_Story, 'I enter a dealership, with the intention of exploring a car')

    def test_ClaimTest_Cost_Parts_PR_Part_Amount(self):
        claimtest = Claim()
        claimtest.Dealer_Story = 'A question occurred to me about a car, and I decided to drop by a dealership to ask.'
        claimtest.Cost_Parts = 'Parts-3'
        claimtest.Cost_Total = 'Cost total 985'
        claimtest.PR_Part_No = 'PR Part Number 3'
        claimtest.PR_Part_Desc = 'PR Part Description3'
        claimtest.PR_Part_Amount = 'PR Amount 180,000'
        claimtest.save()
        self.assertEqual(claimtest.PR_Part_Amount, 'PR Amount 180,000')

class Fault_Code_Test(TestCase):

    def test_Fault_Code_Fields(self):
        fault_code = Fault_Code()
        fault_code.P_Code = 'P_Code1'
        fault_code.Title = 'We are driving down the road and all of a sudden the check engine light goes on'
        fault_code.Mileage = 'Test Mileage'
        fault_code.save()
        record = Fault_Code.objects.get(pk=1)
        self.assertEqual(record, fault_code)

    def test_Fault_Code_title(self):
        fault_code = Fault_Code()
        fault_code.P_Code = 'P_Code2'
        fault_code.Title = 'On Board Diagnostics (OBD-II) is an automotive term referring to a vehicle’s self-diagnostic and reporting capability.'
        fault_code.Mileage = 'Test Mileage 2'
        fault_code.publish = True
        fault_code.save()
        self.assertEqual(fault_code.Title, 'On Board Diagnostics (OBD-II) is an automotive term referring to a vehicle’s self-diagnostic and reporting capability.')

    def test_Fault_Code_Mileage(self):
        fault_code = Fault_Code()
        fault_code.P_Code = 'P_Code1'
        fault_code.Title = 'The trouble code, or diagnostic code, is an alphanumeric value that corresponds to a particular problem.'
        fault_code.Mileage = 'Test Mileage Testing'
        fault_code.save()
        self.assertEqual(fault_code.Mileage, 'Test Mileage Testing')

    def test_Fault_Code_P_Code(self):
        fault_code = Fault_Code()
        fault_code.P_Code = 'P_Code1'
        fault_code.Title = 'Diagnostic codes are divided into four categories: Powertrain (P), Body (B), Chassis © and Network Communications (U). '
        fault_code.Mileage = 'Test Mileage Testing'
        fault_code.save()
        self.assertEqual(fault_code.P_Code, 'P_Code1')
        self.assertEqual(fault_code.Mileage, 'Test Mileage Testing')
