from rest_framework import serializers
from account.models.operators import Operator
from account.settings.base import BASE_DIR, SERVER_URL
from bus.models.bus import Bus
from utils.serializers import DynamicFieldsModelSerializer


class OperatorSerializer(DynamicFieldsModelSerializer):
    bus_count = serializers.SerializerMethodField()

    class Meta:
        model = Operator
        fields = ('id', 'name', 'company_name', 'mobile', 'bus_count' ,'town', 'address', 'gstin', 'aadhar_number',
                  'aadhar_front_photo', 'aadhar_back_photo', 'pan_number', 'pan_photo', 'status',
                 'setup_fee', 'monthly_subscription_fee', 'pos_given_as')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Modify the aadhar_front_photo URL format in the representation
        # direc = 'http://'+str(UploadFiles.get_ec2_instance_ip('i-05d51c6ef2609f88f'))+':8000/media/'
        direc = 'http://localhost:8000/media/'
        if 'aadhar_front_photo' in representation and representation['aadhar_front_photo'] is not None:
            modified_url = representation['aadhar_front_photo'].replace(direc,'').replace('%3A',':').replace('https:/','https://')
            representation['aadhar_front_photo'] = modified_url

        if 'aadhar_back_photo' in representation and representation['aadhar_back_photo'] is not None:
            modified_url = representation['aadhar_back_photo'].replace(direc,'').replace('%3A',':').replace('https:/','https://')
            representation['aadhar_back_photo'] = modified_url
        
        if 'pan_photo' in representation and representation['pan_photo'] is not None:
            modified_url = representation['pan_photo'].replace(direc,'').replace('%3A',':').replace('https:/','https://')
            representation['pan_photo'] = modified_url
        
        return representation

    def get_bus_count(self, obj):
        return Bus.objects.filter(operator=obj).count()

    # def get_bank_accounts(self, obj):
    #     bank_accounts = obj.bank_accounts.all()
    #     return OperatorBankAccountSerializer(bank_accounts, many=True).data

    # def get_remarks(self, obj):
    #     # from operators.serializers import OperatorRemarkSerializer
    #
    #     qs = OperatorRemark.objects.filter(operator=obj)
    #     serializer_data = OperatorRemarkSerializer(qs, many=True).data
    #     return serializer_data


# class OperatorBankAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OperatorBankAccount
#         fields = ('id', 'account_holder_name', 'bank_name', 'account_number', 'ifsc', 'account_type')
