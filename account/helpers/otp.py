from account.sms_templates.otp import COMMUTER_LOGIN_OTP_MESSAGE
from utils.sms_service import SMSService
from utils.apnibus_logger import apnibus_logger


def send_otp(user_obj, mobile_number, otp):
    """
    :param user_obj: Not required
    :param mobile_number: Using this mobile number to send otp
    :param otp: OTP to send
    :return: None
    """
    message = COMMUTER_LOGIN_OTP_MESSAGE.format(otp)
    apnibus_logger.info(message)
    resp = SMSService(mobile=mobile_number, message=message).send_sms(unicode=0)
    apnibus_logger.info(resp)
