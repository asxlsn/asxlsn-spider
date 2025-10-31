import binascii
from gmssl import sm2


def sm2_encrypt(data: str, public_key: str, cipher_mode: int = 0) -> str:
    """
    模拟 JS SM2Utils.encs(key, data, cipherMode)
    cipher_mode:
        0 -> C1C3C2 (JS 使用)
        1 -> C1C2C3 (gmssl 默认)
    返回加密结果: '04' + HEX 字符串（大写）
    """

    # 如果公钥以 04 开头，去掉（JS传的是 X+Y）
    if public_key.startswith('04'):
        public_key = public_key[2:]

    # 检查长度合法
    if len(public_key) != 128:
        raise ValueError("公钥必须是128个十六进制字符（即 X64 + Y64）")

    full_public_key = '04' + public_key
    data_bytes = data.encode('utf-8')

    # 创建SM2对象
    sm2_crypt = sm2.CryptSM2(public_key=full_public_key, private_key='')

    # 加密（gmssl默认是C1C2C3）
    encrypted_bytes = sm2_crypt.encrypt(data_bytes)
    encrypted_hex = binascii.b2a_hex(encrypted_bytes).decode().upper()

    # 如果 JS 使用 cipherMode=0 → 转为 C1C3C2
    if cipher_mode == 0:
        c1 = encrypted_hex[:130]
        c3 = encrypted_hex[-64:]
        c2 = encrypted_hex[130:-64]
        encrypted_hex = c1 + c3 + c2

    return '04' + encrypted_hex


# 来自页面的公钥
public_key_example = "04CF18973EA8F51C60B5595D728BE3342B802E9275B34BCFC2B69E39099F5E624049C492FFF7FB1DCD9C999F29D26AC7121F438DE0F959AF49F8A92C9F3C11D4BB"

# 明文密码
password = "111111"

# JS 页面明确使用 cipherMode = 0
encrypted = sm2_encrypt(password, public_key_example, cipher_mode=0)

print("模拟 JS 加密结果:", encrypted)
