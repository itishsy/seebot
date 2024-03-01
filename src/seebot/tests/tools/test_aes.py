from cryptography.fernet import Fernet
import base64

# 生成随机的128位密钥（32字节）
key = b'Sixteen byte key' * 4  # 这里将会自动转换为bytes类型
cipher_suite = Fernet(base64.urlsafe_b64encode(key))

# 明文数据
plaintext = 'Hello World!'

# AES加密
encrypted_data = cipher_suite.encrypt(plaintext.encode())
print("加密结果：", encrypted_data)