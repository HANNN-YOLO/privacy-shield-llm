# # versi lama
# from presidio_analyzer import RecognizerResult

# from app.utils.text import clean_entity

# ADDRESS_KEYWORDS = [
#     "street ",
#     "road",
#     "avenue",
#     "district",
#     "city",
#     "jalan",
#     "jl ",
#     "jl .",
#     "jl.",
#     "no",
#     "rt",
#     "rw",
#     "kelurahan",
#     "kecamatan",
#     "kota",
#     "province",
# ]


# def detect_address(
#     text: str,
#     results: list[RecognizerResult],
# ) -> list[RecognizerResult]:
#     addresses = []

#     for entity in results:
#         # Hanya proses LOCATION
#         if entity.entity_type != "LOCATION":
#             continue

#         # Ambil konteks sebelum entity
#         before = text[max(0, entity.start - 40):entity.start].lower()

#         # Ambil konteks sesudah entity
#         after = text[entity.end:min(len(text), entity.end + 40)].lower()

        
#         value, start, end = clean_entity(
#             text,
#             entity.start,
#             entity.end,
#         )

#         # context = before + " " + after
#         context = before + " " + value.lower() + " " + after

#         # Cek apakah ada keyword alamat
#         if not any(keyword in context for keyword in ADDRESS_KEYWORDS):
#             continue


#         addresses.append(
#             RecognizerResult(
#                 entity_type="ADDRESS",
#                 start=start,
#                 end=end,
#                 score=entity.score,
#             )
#         )

#     return addresses

# versi upgrade dari nlp + regex
import re
from presidio_analyzer import RecognizerResult
from app.utils.text import clean_entity

# Kata kunci untuk mengecek konteks alamat (internasional & Indonesia)
ADDRESS_KEYWORDS = [
    "street", "road", "avenue", "district", "city",  # kata kunci Inggris
    "jalan", "jl", "kelurahan", "kecamatan", "kota", # kata kunci Indonesia
    "rt", "rw", "no"  # RT/RW dan No.
]

def detect_address(text: str, results: list[RecognizerResult]) -> list[RecognizerResult]:
    addresses = []
    detected_spans = []  # daftar rentang yang sudah ditambahkan

    # 1. Deteksi menggunakan NLP (Presidio) berdasarkan konteks
    for entity in results:
        if entity.entity_type != "LOCATION":
            continue

        # Ambil teks sekitar (40 karakter) untuk konteks sebelum dan sesudah
        before = text[max(0, entity.start - 40):entity.start].lower()
        after = text[entity.end:entity.end + 40].lower()

        # Hapus whitespace ekstra dan tanda baca di akhir (clean_entity)
        value, start, end = clean_entity(text, entity.start, entity.end)

        context = before + " " + value.lower() + " " + after
        # Jika konteks mengandung salah satu kata kunci alamat, terima sebagai alamat
        if any(keyword in context for keyword in ADDRESS_KEYWORDS):
            addresses.append(
                RecognizerResult(entity_type="ADDRESS", start=start, end=end, score=entity.score)
            )
            detected_spans.append((start, end))

    # 2. Deteksi tambahan dengan regex untuk pola 'Jl.' (nama jalan)
    pattern_jalan = re.compile(r"\b(?:Jalan|Jl\.?|Jln)\s+[A-Z][\w\s]*?(?:\s+No\.?\s*\d+)?\b", re.IGNORECASE)
    for match in pattern_jalan.finditer(text):
        span = (match.start(), match.end())
        # Cek apakah span ini sudah tercakup
        if not any(span[0] >= s and span[1] <= e for s, e in detected_spans):
            _, start, end = clean_entity(text, span[0], span[1])
            addresses.append(
                RecognizerResult(entity_type="ADDRESS", start=start, end=end, score=0.85)
            )
            detected_spans.append((start, end))

    # 3. Deteksi tambahan dengan regex untuk pola RT/RW
    pattern_rt_rw = re.compile(r"\bRT\.?\s*\d{1,3}\s*/\s*RW\.?\s*\d{1,3}\b", re.IGNORECASE)
    for match in pattern_rt_rw.finditer(text):
        span = (match.start(), match.end())
        if not any(span[0] >= s and span[1] <= e for s, e in detected_spans):
            _, start, end = clean_entity(text, span[0], span[1])
            addresses.append(
                RecognizerResult(entity_type="ADDRESS", start=start, end=end, score=0.85)
            )
            detected_spans.append((start, end))

    return addresses


# # version expand charakter
# from presidio_analyzer import RecognizerResult
# from app.utils.text import clean_entity

# ADDRESS_KEYWORDS = [
#     "street",
#     "road",
#     "avenue",
#     "district",
#     "city",
#     "jalan",
#     "jl",
#     "no",
#     "rt",
#     "rw",
#     "kelurahan",
#     "kecamatan",
#     "kota",
#     "province"
# ]


# # ============================================================
# # Mengecek apakah entity berada dalam konteks alamat
# # ============================================================

# def is_address_context(text: str, entity: RecognizerResult):

#     before = text[max(0, entity.start - 40):entity.start].lower()
#     after = text[entity.end:min(len(text), entity.end + 60)].lower()

#     value = text[entity.start:entity.end].lower()

#     context = before + value + after

#     return any(
#         keyword in context
#         for keyword in ADDRESS_KEYWORDS
#     )


# # ============================================================
# # Membuat Full Address
# # ============================================================

# def build_full_address(text, entity):

#     start = entity.start
#     end = entity.end

#     # -------------------------------------------------------
#     # Expand ke kiri
#     # -------------------------------------------------------

#     while start > 0:

#         c = text[start - 1]

#         if c.isalnum() or c in ".-/,# ":
#             start -= 1
#             continue

#         break

#     # -------------------------------------------------------
#     # Expand ke kanan
#     # -------------------------------------------------------

#     while end < len(text):

#         c = text[end]

#         if c.isalnum() or c in ".-/,# ":
#             end += 1
#             continue

#         break

#     value = text[start:end].strip()

#     return clean_entity(
#         value,
#         0,
#         len(value)
#     )[0], start, end


# # ============================================================
# # Fallback
# # ============================================================

# def detect_single_address(text, entity):

#     value, start, end = clean_entity(
#         text,
#         entity.start,
#         entity.end
#     )

#     return RecognizerResult(
#         entity_type="ADDRESS",
#         start=start,
#         end=end,
#         score=entity.score
#     )


# # ============================================================
# # MAIN
# # ============================================================

# def detect_address(
#     text: str,
#     results: list[RecognizerResult]
# ):

#     addresses = []

#     used_span = []

#     for entity in results:

#         if entity.entity_type != "LOCATION":
#             continue

#         if not is_address_context(text, entity):
#             continue

#         # ====================================================
#         # PRIORITAS 1
#         # Full Address
#         # ====================================================

#         value, start, end = build_full_address(
#             text,
#             entity
#         )

#         overlap = False

#         for s, e in used_span:

#             if not (end <= s or start >= e):
#                 overlap = True
#                 break

#         if not overlap:

#             addresses.append(

#                 RecognizerResult(
#                     entity_type="ADDRESS",
#                     start=start,
#                     end=end,
#                     score=entity.score
#                 )

#             )

#             used_span.append((start, end))

#             continue

#         # ====================================================
#         # PRIORITAS 2
#         # Single Address
#         # ====================================================

#         addresses.append(

#             detect_single_address(
#                 text,
#                 entity
#             )

#         )

#     return addresses

# # version 3
# from presidio_analyzer import RecognizerResult
# from app.utils.text import clean_entity


# # ============================================================
# # ADDRESS KEYWORDS
# # ============================================================

# ADDRESS_KEYWORDS = [
#     "street",
#     "road",
#     "avenue",
#     "district",
#     "city",
#     "jalan",
#     "jl",
#     "no",
#     "rt",
#     "rw",
#     "kelurahan",
#     "kecamatan",
#     "kota",
#     "province"
# ]


# # ============================================================
# # Mengecek apakah LOCATION berada pada konteks alamat
# # ============================================================

# def is_address_context(
#     text: str,
#     entity: RecognizerResult
# ) -> bool:

#     before = text[
#         max(0, entity.start - 40):entity.start
#     ].lower()

#     value = text[
#         entity.start:entity.end
#     ].lower()

#     after = text[
#         entity.end:min(len(text), entity.end + 60)
#     ].lower()

#     context = before + value + after

#     return any(
#         keyword in context
#         for keyword in ADDRESS_KEYWORDS
#     )


# # ============================================================
# # Mencari batas kiri alamat
# # ============================================================

# def find_left_boundary(
#     text: str,
#     start: int
# ) -> int:

#     while start > 0:
#         character = text[start - 1]
#         if (
#             character.isalnum()
#             or character in ".-/,# "
#         ):
#             start -= 1
#             continue
#         break
#     return start


# # ============================================================
# # Mencari batas kanan alamat
# # ============================================================

# def find_right_boundary(
#     text: str,
#     end: int
# ) -> int:

#     while end < len(text):
#         character = text[end]
#         if (
#             character.isalnum()
#             or character in ".-/,# "
#         ):
#             end += 1
#             continue
#         break
#     return end

# # ============================================================
# # Expand LOCATION menjadi span alamat lengkap
# # ============================================================

# def expand_address_span(
#     text: str,
#     entity: RecognizerResult
# ):

#     start = find_left_boundary(
#         text,
#         entity.start
#     )

#     end = find_right_boundary(
#         text,
#         entity.end
#     )

#     value = text[start:end].strip()
#     return value, start, end

# # # normal
# # # ============================================================
# # # Mengambil komponen-komponen alamat
# # # ============================================================

# # def collect_address_components(
# #     address: str
# # ):
# #     components = []
# #     for part in address.split(","):
# #         part = part.strip()
# #         if part:
# #             components.append(part)
# #     return components

# # # v6
# # # ============================================================
# # # Mengambil komponen-komponen alamat
# # # ============================================================

# # def collect_address_components(
# #     address: str
# # ):

# #     # ---------------------------------------
# #     # Pecah berdasarkan koma
# #     # ---------------------------------------

# #     raw_components = address.split(",")

# #     components = []

# #     # ---------------------------------------
# #     # Penanda parser
# #     # ---------------------------------------

# #     address_started = False

# #     # ---------------------------------------
# #     # Kata yang biasanya muncul
# #     # setelah alamat selesai
# #     # ---------------------------------------

# #     SENTENCE_STARTERS = [

# #         "the ",
# #         "patient ",
# #         "his ",
# #         "her ",
# #         "doctor ",
# #         "dr ",
# #         "please ",
# #         "for ",
# #         "during ",
# #         "after ",
# #         "before ",
# #         "however ",
# #         "therefore "

# #     ]

# #     # ---------------------------------------
# #     # Loop setiap bagian
# #     # ---------------------------------------

# #     for part in raw_components:

# #         part = part.strip()

# #         if not part:
# #             continue

# #         lower = part.lower()

# #         # ===================================
# #         # Menentukan awal alamat
# #         # ===================================

# #         if not address_started:

# #             if any(
# #                 keyword in lower
# #                 for keyword in ADDRESS_KEYWORDS
# #             ):

# #                 address_started = True

# #             elif any(
# #                 char.isdigit()
# #                 for char in part
# #             ):

# #                 address_started = True

# #             else:
# #                 continue

# #         # ===================================
# #         # Stop jika sudah masuk
# #         # kalimat biasa
# #         # ===================================

# #         if any(
# #             lower.startswith(word)
# #             for word in SENTENCE_STARTERS
# #         ):
# #             break

# #         # ===================================
# #         # Stop pada titik
# #         # ===================================

# #         if "." in part:

# #             sentence = part.split(".")[0].strip()

# #             if sentence:

# #                 components.append(sentence)

# #             break

# #         # ===================================
# #         # Simpan komponen
# #         # ===================================

# #         components.append(part)

# #     # ---------------------------------------
# #     # Gabungkan kembali
# #     # ---------------------------------------

# #     cleaned_address = ", ".join(
# #         components
# #     )

# #     return {

# #         "components": components,

# #         "address": cleaned_address,

# #         "count": len(components)

# #     }

# # v7
# # ============================================================
# # Parser Address Components
# # ============================================================

# def collect_address_components(
#     text: str,
#     value: str,
#     start: int
# ):

#     raw_parts = value.split(",")

#     components = []

#     current_position = start

#     new_start = None
#     new_end = None

#     address_started = False

#     SENTENCE_STARTERS = [

#         "the ",
#         "patient ",
#         "his ",
#         "her ",
#         "doctor ",
#         "dr ",
#         "please ",
#         "for ",
#         "during ",
#         "after ",
#         "before ",
#         "however ",
#         "therefore "

#     ]

#     for part in raw_parts:

#         clean = part.strip()

#         if not clean:
#             current_position += len(part) + 1
#             continue

#         lower = clean.lower()

#         # ----------------------------------
#         # Menentukan awal alamat
#         # ----------------------------------

#         if not address_started:

#             if (
#                 any(
#                     keyword in lower
#                     for keyword in ADDRESS_KEYWORDS
#                 )
#                 or
#                 any(
#                     c.isdigit()
#                     for c in clean
#                 )
#             ):

#                 address_started = True

#                 offset = part.find(clean)

#                 new_start = current_position + offset

#             else:

#                 current_position += len(part) + 1
#                 continue

#         # ----------------------------------
#         # Stop jika mulai kalimat baru
#         # ----------------------------------

#         if any(
#             lower.startswith(word)
#             for word in SENTENCE_STARTERS
#         ):
#             break

#         # ----------------------------------
#         # Stop di titik
#         # ----------------------------------

#         if "." in clean:

#             clean = clean.split(".")[0].strip()

#             if clean:
#                 components.append(clean)

#             break

#         components.append(clean)

#         current_position += len(part) + 1

#     cleaned_address = ", ".join(components)

#     if new_start is None:
#         new_start = start

#     new_end = new_start + len(cleaned_address)

#     return {

#         "address": cleaned_address,
#         "components": components,
#         "start": new_start,
#         "end": new_end

#     }

# # # normal
# # # ============================================================
# # # Validasi apakah hasil expand layak dianggap alamat
# # # ============================================================

# # def validate_address(
# #     address: str
# # ) -> bool:

# #     components = collect_address_components(
# #         address
# #     )

# #     score = 0
# #     address_lower = address.lower()

# #     # ---------------------------------------
# #     # Ada keyword alamat
# #     # ---------------------------------------

# #     if any(
# #         keyword in address_lower
# #         for keyword in ADDRESS_KEYWORDS
# #     ):
# #         score += 1

# #     # ---------------------------------------
# #     # Memiliki minimal dua komponen
# #     # ---------------------------------------

# #     if len(components) >= 2:
# #         score += 1

# #     # ---------------------------------------
# #     # Mengandung angka
# #     # ---------------------------------------

# #     if any(
# #         c.isdigit()
# #         for c in address
# #     ):
# #         score += 1
# #     return score >= 2

# # # v6
# # def validate_address(
# #     address: str
# # ) -> bool:

# #     data = collect_address_components(
# #         address
# #     )

# #     components = data["components"]
# #     cleaned_address = data["address"]

# #     score = 0

# #     address_lower = cleaned_address.lower()

# #     # ---------------------------------------
# #     # Ada keyword alamat
# #     # ---------------------------------------

# #     if any(
# #         keyword in address_lower
# #         for keyword in ADDRESS_KEYWORDS
# #     ):
# #         score += 1

# #     # ---------------------------------------
# #     # Memiliki minimal dua komponen
# #     # ---------------------------------------

# #     if len(components) >= 2:
# #         score += 1

# #     # ---------------------------------------
# #     # Mengandung angka
# #     # ---------------------------------------

# #     if any(
# #         c.isdigit()
# #         for c in cleaned_address
# #     ):
# #         score += 1

# #     return score >= 2

# # v7
# # ============================================================
# # Validasi hasil parser alamat
# # ============================================================

# def validate_address(
#     address_info: dict
# ) -> bool:

#     address = address_info["address"]

#     components = address_info["components"]

#     score = 0

#     address_lower = address.lower()

#     # ---------------------------------------
#     # Keyword alamat
#     # ---------------------------------------

#     if any(

#         keyword in address_lower

#         for keyword in ADDRESS_KEYWORDS

#     ):

#         score += 1

#     # ---------------------------------------
#     # Minimal dua komponen
#     # ---------------------------------------

#     if len(components) >= 2:

#         score += 1

#     # ---------------------------------------
#     # Ada angka
#     # ---------------------------------------

#     if any(

#         c.isdigit()

#         for c in address

#     ):

#         score += 1

#     return score >= 2


# # ============================================================
# # Merge Overlapping Address
# # ============================================================

# def merge_overlapping_addresses(
#     addresses: list[RecognizerResult],
#     candidate: RecognizerResult
# ) -> bool:

#     for address in addresses:
#         overlap = not (
#             candidate.end <= address.start
#             or
#             candidate.start >= address.end
#         )
#         if overlap:
#             return False
#     addresses.append(candidate)
#     return True

# # ============================================================
# # Fallback Single Address
# # ============================================================

# def fallback_single_address(
#     text: str,
#     entity: RecognizerResult
# ):

#     value, start, end = clean_entity(
#         text,
#         entity.start,
#         entity.end
#     )

#     return RecognizerResult(
#         entity_type="ADDRESS",
#         start=start,
#         end=end,
#         score=entity.score
#     )

# # ============================================================
# # Detect Single Address
# # ============================================================

# def detect_single_address(
#     text: str,
#     entity: RecognizerResult
# ):

#     value, start, end = clean_entity(
#         text,
#         entity.start,
#         entity.end
#     )

#     if not value:
#         return None

#     return RecognizerResult(
#         entity_type="ADDRESS",
#         start=start,
#         end=end,
#         score=entity.score
#     )




# # ============================================================
# # Membuat object RecognizerResult
# # ============================================================

# def create_recognizer_result(
#     start: int,
#     end: int,
#     score: float
# ):

#     return RecognizerResult(
#         entity_type="ADDRESS",
#         start=start,
#         end=end,
#         score=score
#     )


# # ============================================================
# # Debug Output
# # ============================================================

# def debug_address(
#     text: str,
#     value: str,
#     start: int,
#     end: int,
#     mode: str
# ):

#     print("=" * 70)
#     print("ADDRESS DETECTED")
#     print("MODE      :", mode)
#     print("VALUE     :", repr(value))
#     print("START     :", start)
#     print("END       :", end)
#     print("TEXT      :", repr(text[start:end]))
#     print("=" * 70)

# # # normal + bermasalah
# # # ============================================================
# # # Main Detector
# # # ============================================================

# # def detect_address(
# #     text: str,
# #     results: list[RecognizerResult]
# # ):

# #     addresses = []

# #     # --------------------------------------------------------
# #     # Loop seluruh entity dari Presidio
# #     # --------------------------------------------------------

# #     for entity in results:

# #         # --------------------------------------------
# #         # Hanya LOCATION
# #         # --------------------------------------------

# #         if entity.entity_type != "LOCATION":
# #             continue

# #         # --------------------------------------------
# #         # Pastikan memang konteks alamat
# #         # --------------------------------------------

# #         if not is_address_context(text, entity):
# #             continue

# #         # --------------------------------------------
# #         # Expand menjadi alamat lengkap
# #         # --------------------------------------------

# #         # normal + masalah
# #         # value, start, end = expand_address_span(
# #         #     text,
# #         #     entity
# #         # )

# #         # # --------------------------------------------
# #         # # Pisahkan komponen alamat
# #         # # --------------------------------------------
# #         # # # normal
# #         # # components = collect_address_components(
# #         # #     value
# #         # # )

# #         # component_data = collect_address_components(
# #         #     value
# #         # )

# #         # components = component_data["components"]

# #         # cleaned_address = component_data["address"]

# #         # # --------------------------------------------
# #         # # Validasi hasil expand
# #         # # --------------------------------------------

# #         # # normal
# #         # # if validate_address(value):

# #         # # v6
# #         # if validate_address(cleaned_address):

# #         #     candidate = create_recognizer_result(
# #         #         start,
# #         #         end,
# #         #         entity.score
# #         #     )

# #         #     if merge_overlapping_addresses(
# #         #         addresses,
# #         #         candidate
# #         #     ):

# #         #         # # normal
# #         #         # debug_address(
# #         #         #     text,
# #         #         #     components,
# #         #         #     start,
# #         #         #     end,
# #         #         #     "FULL ADDRESS"
# #         #         # )

# #         #         # v6
# #         #         debug_address(
# #         #             text,
# #         #             cleaned_address,
# #         #             start,
# #         #             end,
# #         #             "FULL ADDRESS"
# #         #         )

# #         #         continue

# #         # v7
# #         value, start, end = expand_address_span(
# #             text,
# #             entity
# #         )

# #         address_info = collect_address_components(
# #             text,
# #             value,
# #             start
# #         )

# #         if validate_address(address_info):

# #             candidate = create_recognizer_result(

# #                 address_info["start"],
# #                 address_info["end"],
# #                 entity.score

# #             )

# #             if merge_overlapping_addresses(
# #                 addresses,
# #                 candidate
# #             ):

# #                 debug_address(

# #                     text,

# #                     address_info["address"],

# #                     address_info["start"],

# #                     address_info["end"],

# #                     "FULL ADDRESS"

# #                 )

# #                 continue

# #         # --------------------------------------------
# #         # Jika Full Address gagal
# #         # gunakan Single Address
# #         # --------------------------------------------

# #         fallback = detect_single_address(
# #             text,
# #             entity
# #         )

# #         if fallback is not None:

# #             debug_address(
# #                 text,
# #                 text[fallback.start:fallback.end],
# #                 fallback.start,
# #                 fallback.end,
# #                 "SINGLE ADDRESS"
# #             )

# #             merge_overlapping_addresses(
# #                 addresses,
# #                 fallback
# #             )

# #     return addresses

# # v4
# # ============================================================
# # Main Detector
# # ============================================================

# def detect_address(
#     text: str,
#     results: list[RecognizerResult]
# ):

#     addresses = []

#     # --------------------------------------------
#     # Menandai sampai index mana
#     # alamat sebelumnya sudah diproses
#     # --------------------------------------------

#     processed_until = -1

#     # --------------------------------------------
#     # Loop seluruh entity
#     # --------------------------------------------

#     for entity in results:

#         # --------------------------------------------
#         # Hanya LOCATION
#         # --------------------------------------------

#         if entity.entity_type != "LOCATION":
#             continue

#         # --------------------------------------------
#         # LOCATION ini sudah masuk
#         # alamat sebelumnya
#         # --------------------------------------------

#         if entity.start < processed_until:
#             continue

#         # --------------------------------------------
#         # Harus benar-benar konteks alamat
#         # --------------------------------------------

#         if not is_address_context(
#             text,
#             entity
#         ):
#             continue

#         # --------------------------------------------
#         # Expand span
#         # --------------------------------------------

#         value, start, end = expand_address_span(
#             text,
#             entity
#         )

#         # --------------------------------------------
#         # Parser alamat
#         # --------------------------------------------

#         address_info = collect_address_components(
#             text,
#             value,
#             start
#         )

#         # --------------------------------------------
#         # Validasi
#         # --------------------------------------------

#         if validate_address(address_info):

#             candidate = create_recognizer_result(

#                 address_info["start"],
#                 address_info["end"],
#                 entity.score

#             )

#             # ----------------------------------------
#             # Merge overlap
#             # ----------------------------------------

#             if merge_overlapping_addresses(
#                 addresses,
#                 candidate
#             ):

#                 debug_address(

#                     text,

#                     address_info["address"],

#                     address_info["start"],

#                     address_info["end"],

#                     "FULL ADDRESS"

#                 )

#                 # ------------------------------------
#                 # LOCATION berikutnya
#                 # di dalam span ini
#                 # tidak diproses lagi
#                 # ------------------------------------

#                 processed_until = candidate.end

#                 continue

#         # --------------------------------------------
#         # Fallback
#         # --------------------------------------------

#         fallback = detect_single_address(
#             text,
#             entity
#         )

#         if fallback is not None:

#             if merge_overlapping_addresses(
#                 addresses,
#                 fallback
#             ):

#                 debug_address(

#                     text,

#                     text[fallback.start:fallback.end],

#                     fallback.start,

#                     fallback.end,

#                     "SINGLE ADDRESS"

#                 )

#                 processed_until = fallback.end

#     return addresses