import time

from scanner.dexscreener import get_tokens

print("=" * 50)
print("💎 GemRadar AI Auto Scanner")
print("=" * 50)

SCAN_INTERVAL = 60  # detik

while True:
    print("\n🔍 Memulai scan DexScreener...")

    try:
        get_tokens()
        print("✅ Scan selesai")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    print(f"⏳ Menunggu {SCAN_INTERVAL} detik...\n")
    time.sleep(SCAN_INTERVAL)