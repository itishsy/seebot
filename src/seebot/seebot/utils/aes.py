from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

encoding = 'utf-8'
aes_key = '1a2C9b8gh5ltvt0m'
pad_style = 'pkcs7'


def encrypt(plaintext: str) -> str:
    # 将密钥编码为UTF-8格式的bytes
    key_bytes = aes_key.encode(encoding)
    # 创建AES对象
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    # 将明文编码为UTF-8格式的bytes
    plaintext_bytes = plaintext.encode(encoding)
    # 为编码后的明文添加padding
    plaintext_bytes_padded = pad(plaintext_bytes, AES.block_size, pad_style)
    # 执行加密
    ciphertext_bytes = cipher.encrypt(plaintext_bytes_padded)
    # 将加密后的bytes进行base64编码
    # 注意：不能用encodebytes！否则会每76个字符增加一个换行符，见：https://docs.python.org/zh-cn/3/library/base64.html
    ciphertext_base64_bytes = base64.b64encode(ciphertext_bytes)
    # 将base64编码过的bytes，解码为Python中使用的字符串类型（即unicode字符串）
    ciphertext = ciphertext_base64_bytes.decode(encoding)
    return ciphertext