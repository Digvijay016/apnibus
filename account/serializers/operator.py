from rest_framework import serializers
from account.models.operators import Operator
from utils.serializers import DynamicFieldsModelSerializer
# from account.models.bus import Bus
# from operators.models import OperatorRemark


class OperatorSerializer(DynamicFieldsModelSerializer):
    # bank_accounts = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    # onboarded_bus_count = serializers.SerializerMethodField(read_only=True)
    # remarks = serializers.SerializerMethodField(read_only=True)
    # img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Operator
        fields = ('id', 'name', 'hindi_name', 'owner', 'email', 'mobile', 'town', 'address', 'gstin', 'aadhar_number',
                  'aadhar_front_photo', 'aadhar_back_photo', 'pan_number', 'pan_photo', 'bus_count', 'poc_name', 'poc_number', 'is_active', 'status',
                  'show_qr_code', 'show_ticket_msg', 'show_brand_name', 'show_mob_number', 'setup_fee', 'monthly_subscription_fee', 'pos_given_as')

    def get_email(self, obj):
        operator_email = obj.user.email
        return operator_email

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Modify the aadhar_front_photo URL format in the representation
        # print(representation['aadhar_front_photo'])
        # print(representation['aadhar_back_photo'])
        # print(representation['pan_photo'])
        if 'aadhar_front_photo' in representation and representation['aadhar_front_photo'] is not None:
            modified_url = representation['aadhar_front_photo'].replace("http://localhost:8000/media/",'').replace('%3A',':').replace('https:/','https://')
            # print(modified_url)
            representation['aadhar_front_photo'] = modified_url

        if 'aadhar_back_photo' in representation and representation['aadhar_back_photo'] is not None:
            modified_url = representation['aadhar_back_photo'].replace("http://localhost:8000/media/",'').replace('%3A',':').replace('https:/','https://')
            # print(modified_url)
            representation['aadhar_back_photo'] = modified_url
        
        if 'pan_photo' in representation and representation['pan_photo'] is not None:
            modified_url = representation['pan_photo'].replace("http://localhost:8000/media/",'').replace('%3A',':').replace('https:/','https://')
            # print(modified_url)
            representation['pan_photo'] = modified_url
        
        return representation

    # def get_bank_accounts(self, obj):
    #     bank_accounts = obj.bank_accounts.all()
    #     return OperatorBankAccountSerializer(bank_accounts, many=True).data

    # def get_onboarded_bus_count(self, obj):
    #     return Bus.objects.filter(operator=obj).count()

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
