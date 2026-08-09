import re

# Pola regex untuk deteksi nomor telepon (lihat penjelasan di atas)
phone_pattern = re.compile(
    r"(?:(?:\+|00)\s*(?:\d{1,3})[-.\s]?)?"
    r"(?:\(?\d{1,4}\)?[-.\s]?)*"
    r"\d{3,4}(?:[-.\s]?\d{3,4})*"
)

# Pengecualian awalan lokal (Indonesia)
INDO_LOCAL = re.compile(r'^(?:\+62|62|0)(\d+)$')

def normalize_phone(raw: str) -> str:
    # Hapus semua karakter kecuali + dan digit
    s = re.sub(r'[^\d+]', '', raw)
    # Ganti awalan "00" dengan "+"
    if s.startswith("00"):
        s = "+" + s[2:]
    # Jika ada + dan digit sesudahnya, ya sudah; jika tidak ada, tambah + di depan
    if not s.startswith("+"):
        # Cek jika nomor Indonesia (0 atau 62)
        m = INDO_LOCAL.match(s)
        if m:
            digits = m.group(1)
            # Jika sebelumnya '0' ( tanpa 62), ganti ke +62
            if s.startswith("0"):
                s = "+62" + digits
            else:
                # Memulai dengan '62' tanpa +, tambahkan +
                s = "+" + s
        else:
            s = "+" + s  # default tambah +
    # Batasi hanya 15 digit setelah +
    digits = re.sub(r'\D', '', s)
    if len(digits) > 15:
        digits = digits[:15]
    return "+" + digits

def detect_phone(text: str):
    results = []
    for m in phone_pattern.finditer(text):
        raw = m.group().strip()
        start, end = m.span()
        # Hitung digit saja
        digits = re.sub(r'\D', '', raw)
        # Abaikan jika digit < 8
        if len(digits) < 8:
            continue
        # Normalisasi
        normalized = normalize_phone(raw)
        results.append({
            "start": start,
            "end": end,
            "text": raw,
            "entity_type": "PHONE",
            "normalized": normalized,
            "confidence": 0.99
        })
    return results

def redact_phone(text: str):
    """Ganti teks nomor telepon dengan token, mempertahankan pemisah spasi."""
    def repl(m):
        raw = m.group()
        norm = normalize_phone(raw)
        token = f"[PHONE_{hash(norm) & 0xFFFF:04d}]"
        # Ganti angka dengan token, pertahankan panjang
        return token
    return phone_pattern.sub(repl, text)
