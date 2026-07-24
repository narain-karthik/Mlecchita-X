import unittest
from mlecchita_x import (
    encrypt, decrypt, encrypt_text, decrypt_text, generate_key,
    AuthenticationError
)
from mlecchita_x.primitives import sbox, position_permutation

class CipherTests(unittest.TestCase):
    def test_round_trip_bytes(self):
        key = generate_key()
        cases = [b"", b"a", b"hello", bytes(range(256)), b"x" * 4096]
        for data in cases:
            self.assertEqual(decrypt(encrypt(data, key), key), data)

    def test_unicode(self):
        key = generate_key()
        text = "Vanakkam தமிழ் — Mlecchita-X"
        self.assertEqual(decrypt_text(encrypt_text(text, key), key), text)

    def test_wrong_key_rejected(self):
        blob = encrypt(b"secret", generate_key())
        with self.assertRaises(AuthenticationError):
            decrypt(blob, generate_key())

    def test_tampering_rejected(self):
        key = generate_key()
        blob = bytearray(encrypt(b"secret message", key))
        blob[30] ^= 1
        with self.assertRaises(AuthenticationError):
            decrypt(bytes(blob), key)

    def test_fresh_nonce_changes_ciphertext(self):
        key = generate_key()
        a = encrypt(b"same plaintext", key)
        b = encrypt(b"same plaintext", key)
        self.assertNotEqual(a, b)

    def test_sbox_is_permutation(self):
        key = generate_key()
        nonce = bytes(16)
        table, inverse = sbox(key, nonce, 0)
        self.assertEqual(sorted(table), list(range(256)))
        for i, v in enumerate(table):
            self.assertEqual(inverse[v], i)

    def test_position_permutation(self):
        key = generate_key()
        nonce = bytes(16)
        table, inverse = position_permutation(key, nonce, 0, 100)
        self.assertEqual(sorted(table), list(range(100)))
        for old, new in enumerate(inverse):
            self.assertEqual(table[new], old)

if __name__ == "__main__":
    unittest.main()
