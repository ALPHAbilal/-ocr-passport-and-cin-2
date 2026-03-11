============================================================
TEST 3 — REAL OCR — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M | Time: 10.01s | Tokens: 822→123
Raw: <think>

</think>

{
  "last_name_ar": "بلال",
  "last_name_fr": "BILAL",
  "first_name_ar": "شافي",
  "first_name_fr": "CHAFI",
  "birth_date": "22.01.2001",
  "birth_place_fr": "RABAT",
  "birth_place_ar": "رباط",
  "expiry_date": "19.03.2029",
  "card_number": "AS13538",
  "gender": "M"
}

Extracted:
{
  "last_name_ar": "بلال",
  "last_name_fr": "BILAL",
  "first_name_ar": "شافي",
  "first_name_fr": "CHAFI",
  "birth_date": "22.01.2001",
  "birth_place_fr": "RABAT",
  "birth_place_ar": "رباط",
  "expiry_date": "19.03.2029",
  "card_number": "AS13538",
  "gender": "M"
}

SCORECARD — Real OCR:
------------------------------------------------------------
  MISS last_name_fr: expected 'CHAFI' got 'BILAL'
  MISS first_name_fr: expected 'BILAL' got 'CHAFI'
  MISS last_name_ar: expected 'شافي' got 'بلال'
  MISS first_name_ar: expected 'بلال' got 'شافي'
  OK   birth_date: '22.01.2001'
  OK   birth_place_fr: 'RABAT'
  MISS birth_place_ar: expected 'الرباط' got 'رباط'
  OK   card_number: 'AS13538'
  OK   expiry_date: '19.03.2029'
  OK   gender: 'M'


--------------------------
============================================================
STRESS 1 — Compound name + Casablanca — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M | Time: 9.74s | Tokens: 802→134
Raw: <think>

</think>

{
  "last_name_ar": "عبد الرحمن",
  "last_name_fr": "ABDERRAHMANE",
  "first_name_ar": "البكاوي",
  "first_name_fr": "EL BAKAOUI",
  "birth_date": "15.06.1985",
  "birth_place_fr": "CASABLANCA",
  "birth_place_ar": "الدار البيضاء",
  "expiry_date": "01.07.2030",
  "card_number": "BK987654",
  "gender": "M"
}

Extracted:
{
  "last_name_ar": "عبد الرحمن",
  "last_name_fr": "ABDERRAHMANE",
  "first_name_ar": "البكاوي",
  "first_name_fr": "EL BAKAOUI",
  "birth_date": "15.06.1985",
  "birth_place_fr": "CASABLANCA",
  "birth_place_ar": "الدار البيضاء",
  "expiry_date": "01.07.2030",
  "card_number": "BK987654",
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

Score: 6/10 | Time: 9.74s

============================================================
STRESS 2 — Female + compound first name + Oujda — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M | Time: 9.57s | Tokens: 860→128
Raw: <think>

</think>

{
  "last_name_ar": "فاطمة",
  "last_name_fr": "FATIMA",
  "first_name_ar": "الزهراء",
  "first_name_fr": "EZZAHRA",
  "birth_date": "03.11.1992",
  "birth_place_fr": "OUJDA",
  "birth_place_ar": "أوجدا",
  "expiry_date": "10.12.2028",
  "card_number": "CD554433",
  "gender": "F"
}

Extracted:
{
  "last_name_ar": "فاطمة",
  "last_name_fr": "FATIMA",
  "first_name_ar": "الزهراء",
  "first_name_fr": "EZZAHRA",
  "birth_date": "03.11.1992",
  "birth_place_fr": "OUJDA",
  "birth_place_ar": "أوجدا",
  "expiry_date": "10.12.2028",
  "card_number": "CD554433",
  "gender": "F"
}

  MISS last_name_fr: expected 'BENNISSI' got 'FATIMA'
  MISS first_name_fr: expected 'FATIMA' got 'EZZAHRA'
  MISS last_name_ar: expected 'بنيسى' got 'فاطمة'
  MISS first_name_ar: expected 'فاطمة' got 'الزهراء'
  OK   birth_date: '03.11.1992'
  OK   birth_place_fr: 'OUJDA'
  MISS birth_place_ar: expected 'وجدة' got 'أوجدا'
  OK   card_number: 'CD554433'
  OK   expiry_date: '10.12.2028'
  OK   gender: 'F'

Score: 5/10 | Time: 9.57s

============================================================
STRESS 3 — Minimal detections, missing fields — Qwen3-8B Q4_K_M
============================================================
Model: Qwen3-8B Q4_K_M | Time: 6.37s | Tokens: 563→113
Raw: <think>

</think>

{
  "last_name_ar": "محمد",
  "last_name_fr": "MOHAMMED",
  "first_name_ar": "ALAOUI",
  "first_name_fr": "ALAOUI",
  "birth_date": "22.08.1970",
  "birth_place_fr": "FES",
  "birth_place_ar": "فيس",
  "expiry_date": null,
  "card_number": "EE112233",
  "gender": "M"
}

Extracted:
{
  "last_name_ar": "محمد",
  "last_name_fr": "MOHAMMED",
  "first_name_ar": "ALAOUI",
  "first_name_fr": "ALAOUI",
  "birth_date": "22.08.1970",
  "birth_place_fr": "FES",
  "birth_place_ar": "فيس",
  "expiry_date": null,
  "card_number": "EE112233",
  "gender": "M"
}

  MISS last_name_fr: expected 'ALAOUI' got 'MOHAMMED'
  MISS first_name_fr: expected 'MOHAMMED' got 'ALAOUI'
  MISS last_name_ar: expected 'None' got 'محمد'
  MISS first_name_ar: expected 'محمد' got 'ALAOUI'
  OK   birth_date: '22.08.1970'
  OK   birth_place_fr: 'FES'
  MISS birth_place_ar: expected 'فاس' got 'فيس'
  OK   card_number: 'EE112233'
  OK   expiry_date: 'None'
  OK   gender: 'M'

Score: 5/10 | Time: 6.37s



SCORECARD — Qwen3-8B Q4_K_M — Sample 1 (clean OCR):
------------------------------------------------------------
  OK  last_name_fr: 'CHAFI'
  OK  first_name_fr: 'BILAL'
  OK  last_name_ar: 'الشافعي'
  OK  first_name_ar: 'بلال'
  OK  birth_date: '22.01.2007'
  OK  birth_place_fr: 'RABAT'
  MISS birth_place_ar: expected 'الرباط' got 'رباط'
  OK  card_number: 'AB123456'
  OK  expiry_date: '19.03.2029'
  OK  gender: 'M'

Score: 9/10 fields correct | Time: 13.52s


============================================================
FEW-SHOT TEST — Qwen3-8B Q4_K_M — Sample 2 (noisy)
============================================================
Model: Qwen3-8B Q4_K_M | Time: 9.19s | Tokens: 635→108
Raw: <think>

</think>

{"last_name_fr": "CHAF1", "first_name_fr": "B1LAL", "last_name_ar": null, "first_name_ar": "اجا", "birth_date": "22.O1.20O7", "birth_place_fr": "RABA7", "birth_place_ar": null, "card_number": "A8123456", "expiry_date": "19.03.2029", "gender": null}

Few-shot extracted:
{
  "last_name_fr": "CHAF1",
  "first_name_fr": "B1LAL",
  "last_name_ar": null,
  "first_name_ar": "اجا",
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
  "last_name_ar": "الملكة",
  "last_name_fr": "ROYAUME",
  "first_name_ar": "لوح",
  "first_name_fr": "CHAF1",
  "birth_date": "22.01.2007",
  "birth_place_fr": "RABA7",
  "birth_place_ar": "رباط",
  "expiry_date": "19.03.2029",
  "card_number": "A8123456",
  "gender": null
}