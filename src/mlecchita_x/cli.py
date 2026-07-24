import argparse
from pathlib import Path

from . import encrypt, decrypt, encrypt_text, decrypt_text
from .keys import generate_key, save_key, load_key

def main():
    parser = argparse.ArgumentParser(description="Mlecchita-X experimental research cipher")
    sub = parser.add_subparsers(dest="command", required=True)

    keygen = sub.add_parser("keygen", help="Generate a 256-bit secret key")
    keygen.add_argument("-o", "--output", required=True)

    enc_text = sub.add_parser("encrypt-text", help="Encrypt UTF-8 text")
    enc_text.add_argument("--key", required=True)
    enc_text.add_argument("text")

    dec_text = sub.add_parser("decrypt-text", help="Decrypt an MX02 text token")
    dec_text.add_argument("--key", required=True)
    dec_text.add_argument("token")

    enc_file = sub.add_parser("encrypt-file", help="Encrypt a file")
    enc_file.add_argument("--key", required=True)
    enc_file.add_argument("input")
    enc_file.add_argument("output")

    dec_file = sub.add_parser("decrypt-file", help="Decrypt a file")
    dec_file.add_argument("--key", required=True)
    dec_file.add_argument("input")
    dec_file.add_argument("output")

    args = parser.parse_args()

    if args.command == "keygen":
        save_key(args.output, generate_key())
        print(f"Key saved to {args.output}")
        return

    key = load_key(args.key)

    if args.command == "encrypt-text":
        print(encrypt_text(args.text, key))
    elif args.command == "decrypt-text":
        print(decrypt_text(args.token, key))
    elif args.command == "encrypt-file":
        Path(args.output).write_bytes(encrypt(Path(args.input).read_bytes(), key))
        print(f"Encrypted file saved to {args.output}")
    elif args.command == "decrypt-file":
        Path(args.output).write_bytes(decrypt(Path(args.input).read_bytes(), key))
        print(f"Decrypted file saved to {args.output}")

if __name__ == "__main__":
    main()
