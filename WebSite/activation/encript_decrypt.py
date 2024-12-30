import json
from cryptography.fernet import Fernet

  


def encrypt_data(data,KEY = b'UX9tkZTaHTU0GqnBT6vnI4mi3Ja3XQRUMrHqjzmXm4I='):
    """Chiffre les données (dictionnaire)."""
    cipher = Fernet(KEY)
    json_data = json.dumps(data)  # Convertir le dictionnaire en chaîne JSON
    encrypted_data = cipher.encrypt(json_data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data,KEY = b'UX9tkZTaHTU0GqnBT6vnI4mi3Ja3XQRUMrHqjzmXm4I='):
    """Déchiffre les données (dictionnaire)."""
    cipher = Fernet(KEY)
    decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
    return json.loads(decrypted_data)  # Convertir la chaîne JSON en dictionnaire