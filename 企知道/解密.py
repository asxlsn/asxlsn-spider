from Crypto.Cipher import AES
import base64
import json

# 密钥映射表（来自原始 JS 代码）
AES_KEYS = {
    1: "xc46VoB49X3PGYAg",
    2: "KE3pb84wxqLTZEG3",
    3: "18Lw0OEaBBUwHYNT",
    4: "jxxWWIzvkqEQcZrd",
    5: "40w42rjLEXxYhxRn",
    6: "K6hkD03WNW8N1fPM",
    7: "I8V3IwIhrwNbWxqz",
    8: "3JNNbxAP4zi5oSGA",
    9: "7pUuESQl8aRTFFKK",
    10: "KB4GAHN6M5soB3WV"
}


def aes_ecb_decrypt_base64(cipher_text: str, key_index: int) -> str:
    """
    解密 AES ECB 模式的 base64 密文。
    :param cipher_text: 加密后的 base64 字符串
    :param key_index: 使用的密钥编号（1-10）
    :return: 解密后的明文字符串
    """
    if key_index not in AES_KEYS:
        raise ValueError(f"无效的密钥编号：{key_index}")

    key = AES_KEYS[key_index].encode('utf-8')
    cipher_data = base64.b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(cipher_data)
    # 去除 PKCS7 padding
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode('utf-8')


cipher_text =""  # 你的密文
key_index = 9  # hasUse

plaintext = aes_ecb_decrypt_base64(cipher_text, key_index)
print("解密结果：", plaintext)

