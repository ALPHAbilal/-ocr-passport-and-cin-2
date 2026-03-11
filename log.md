============================================================
TEST 3 — REAL OCR — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M
Inference time: 8.10s
Tokens — prompt: 1206, completion: 112
Raw output (first 500 chars):
<think>

</think>

{"last_name_fr": "CHAFI", "first_name_fr": "BILAL", "last_name_ar": "شافي", "first_name_ar": "بلال", "birth_date": "22.01.2001", "birth_place_fr": "RABAT", "birth_place_ar": "الرباط", "card_number": "AS13538", "expiry_date": "19.03.2029", "gender": "M"}

Extracted:
{
  "last_name_fr": "CHAFI",
  "first_name_fr": "BILAL",
  "last_name_ar": "شافي",
  "first_name_ar": "بلال",
  "birth_date": "22.01.2001",
  "birth_place_fr": "RABAT",
  "birth_place_ar": "الرباط",
  "card_number": "AS13538",
  "expiry_date": "19.03.2029",
  "gender": "M"
}

SCORECARD — Real OCR:
------------------------------------------------------------
  OK   last_name_fr: 'CHAFI'
  OK   first_name_fr: 'BILAL'
  OK   last_name_ar: 'شافي'
  OK   first_name_ar: 'بلال'
  OK   birth_date: '22.01.2001'
  OK   birth_place_fr: 'RABAT'
  OK   birth_place_ar: 'الرباط'
  OK   card_number: 'AS13538'
  OK   expiry_date: '19.03.2029'
  OK   gender: 'M'

Score: 10/10 fields correct | Time: 8.1s


------------------
============================================================
STRESS 1 — Compound name + Casablanca — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M
Inference time: 9.53s
Tokens — prompt: 1186, completion: 122
Raw output (first 500 chars):
<think>

</think>

{"last_name_fr": "ABDERRAHMANE", "first_name_fr": "EL BAKAOUI", "last_name_ar": "عبد الرحمن", "first_name_ar": "البكاوي", "birth_date": "15.06.1985", "birth_place_fr": "CASABLANCA", "birth_place_ar": "الدار البيضاء", "card_number": "BK987654", "expiry_date": "01.07.2030", "gender": "M"}

Extracted:
{
  "last_name_fr": "ABDERRAHMANE",
  "first_name_fr": "EL BAKAOUI",
  "last_name_ar": "عبد الرحمن",
  "first_name_ar": "البكاوي",
  "birth_date": "15.06.1985",
  "birth_place_fr": "CASABLANCA",
  "birth_place_ar": "الدار البيضاء",
  "card_number": "BK987654",
  "expiry_date": "01.07.2030",
  "gender": "M"
}

  MISS last_name_fr: expected 'EL BAKAOUI' got 'ABDERRAHMANE'
  MISS first_name_fr: expected 'ABDERRAHMANE' got 'EL BAKAOUI'
  MISS last_name_ar: expected 'البكاوي' got 'عبد الرحمن'
  MISS first_name_ar: expected 'عبد الرحمن' got 'البكاوي'
  OK   birth_date: '15.06.1985'
  OK   birth_place_fr: 'CASABLANCA'
  OK   birth_place_ar: 'الدار البيضاء'
  OK   card_number: 'BK987654'
  OK   expiry_date: '01.07.2030'
  OK   gender: 'M'

Score: 6/10 | Time: 9.53s

============================================================
STRESS 2 — Female + compound first name + Oujda — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M
Inference time: 10.61s
Tokens — prompt: 1244, completion: 117
Raw output (first 500 chars):
<think>

</think>

{"last_name_fr": "FATIMA", "first_name_fr": "BENNISSI", "last_name_ar": "الزهراء", "first_name_ar": "فاطمة", "birth_date": "03.11.1992", "birth_place_fr": "OUJDA", "birth_place_ar": "الواجدة", "card_number": "CD554433", "expiry_date": "10.12.2028", "gender": "F"}

Extracted:
{
  "last_name_fr": "FATIMA",
  "first_name_fr": "BENNISSI",
  "last_name_ar": "الزهراء",
  "first_name_ar": "فاطمة",
  "birth_date": "03.11.1992",
  "birth_place_fr": "OUJDA",
  "birth_place_ar": "الواجدة",
  "card_number": "CD554433",
  "expiry_date": "10.12.2028",
  "gender": "F"
}

  MISS last_name_fr: expected 'BENNISSI' got 'FATIMA'
  MISS first_name_fr: expected 'FATIMA' got 'BENNISSI'
  MISS last_name_ar: expected 'بنيسى' got 'الزهراء'
  OK   first_name_ar: 'فاطمة'
  OK   birth_date: '03.11.1992'
  OK   birth_place_fr: 'OUJDA'
  MISS birth_place_ar: expected 'وجدة' got 'الواجدة'
  OK   card_number: 'CD554433'
  OK   expiry_date: '10.12.2028'
  OK   gender: 'F'

Score: 6/10 | Time: 10.61s

============================================================
STRESS 3 — Minimal detections, missing fields — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M
Inference time: 5.85s
Tokens — prompt: 947, completion: 101
Raw output (first 500 chars):
<think>

</think>

{"last_name_fr": "ALAOUI", "first_name_fr": "MOHAMMED", "last_name_ar": "محمد", "first_name_ar": "محمد", "birth_date": "22.08.1970", "birth_place_fr": "FES", "birth_place_ar": "الفيسب", "card_number": "EE112233", "expiry_date": "null", "gender": "M"}

Extracted:
{
  "last_name_fr": "ALAOUI",
  "first_name_fr": "MOHAMMED",
  "last_name_ar": "محمد",
  "first_name_ar": "محمد",
  "birth_date": "22.08.1970",
  "birth_place_fr": "FES",
  "birth_place_ar": "الفيسب",
  "card_number": "EE112233",
  "expiry_date": "null",
  "gender": "M"
}

  OK   last_name_fr: 'ALAOUI'
  OK   first_name_fr: 'MOHAMMED'
  MISS last_name_ar: expected 'None' got 'محمد'
  OK   first_name_ar: 'محمد'
  OK   birth_date: '22.08.1970'
  OK   birth_place_fr: 'FES'
  MISS birth_place_ar: expected 'فاس' got 'الفيسب'
  OK   card_number: 'EE112233'
  MISS expiry_date: expected 'None' got 'null'
  OK   gender: 'M'

Score: 7/10 | Time: 5.85s
-----------------------------


SCORECARD — Qwen3-8B Q4_K_M — Sample 1 (clean OCR):
------------------------------------------------------------
  OK  last_name_fr: 'CHAFI'
  OK  first_name_fr: 'BILAL'
  MISS last_name_ar: expected 'الشافعي' got 'شافي'
  OK  first_name_ar: 'بلال'
  OK  birth_date: '22.01.2007'
  OK  birth_place_fr: 'RABAT'
  OK  birth_place_ar: 'الرباط'
  OK  card_number: 'AB123456'
  OK  expiry_date: '19.03.2029'
  OK  gender: 'M'

Score: 9/10 fields correct | Time: 12.8s

--------------
============================================================
FEW-SHOT TEST — Qwen3-8B Q4_K_M — Sample 2 (noisy)
============================================================
Model: Qwen3-8B Q4_K_M
Inference time: 8.14s
Tokens — prompt: 641, completion: 106
Raw output (first 500 chars):
<think>

</think>

{"last_name_fr": "CHAF1", "first_name_fr": "B1LAL", "last_name_ar": null, "first_name_ar": null, "birth_date": "22.O1.20O7", "birth_place_fr": "RABA7", "birth_place_ar": null, "card_number": "A8123456", "expiry_date": "19.03.2029", "gender": null}

Few-shot extracted:
{
  "last_name_fr": "CHAF1",
  "first_name_fr": "B1LAL",
  "last_name_ar": null,
  "first_name_ar": null,
  "birth_date": "22.O1.20O7",
  "birth_place_fr": "RABA7",
  "birth_place_ar": null,
  "card_number": "A8123456",
  "expiry_date": "19.03.2029",
  "gender": null
}

============================================================
Compare with zero-shot on same input:
{
  "last_name_fr": "CHAFI",
  "first_name_fr": "BILAL",
  "last_name_ar": "شافي",
  "first_name_ar": "بلال",
  "birth_date": "22.01.2007",
  "birth_place_fr": "RABAT",
  "birth_place_ar": "الرباط",
  "card_number": "A8123456",
  "expiry_date": "19.03.2029",
  "gender": "M"
}
-----------------------