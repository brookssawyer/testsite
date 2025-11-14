#!/usr/bin/env python3
"""
Generate a secure random SECRET_KEY for production deployment
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(32)
    print("\n" + "="*60)
    print("Generated SECRET_KEY for Railway deployment:")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("\nAdd this to your Railway environment variables as:")
    print(f"SECRET_KEY={secret_key}")
    print("="*60 + "\n")
