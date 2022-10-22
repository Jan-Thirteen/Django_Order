from django.conf import settings
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig


# 生成支付alipay对象，以供调用
def alipay_obj():
    alipay = AliPay(
        appid=settings.ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=open(settings.ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=open(settings.ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=settings.ALIPAY_SETTING.get('SIGN_TYPE'),  # RSA 或者 RSA2
        debug=settings.ALIPAY_SETTING.get('ALIPAY_DEBUG'),  # 默认 False
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间
    )
    return alipay