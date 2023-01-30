import base64

import rsa

from config.config import dev_public_key, prod_public_key


def rsa_encrypt(message, env="dev"):
    """
    使用rsa 加密生成 x-guard-key。
    :param message:
    :param env:
    :return: 使用公钥对32位随机值aes key进行加密并转成base64的字符串
    """
    if env == "dev":
        pem_file = dev_public_key
    elif env == "prod":
        pem_file = prod_public_key
    else:
        pem_file = dev_public_key

    f = open(pem_file, 'rb')
    content = f.read()
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(content)
    crypto_text = rsa.encrypt(message, public_key)
    return base64.b64encode(crypto_text)
