otal: 122.1s

GPT-OSS-20B
110.1s
Last Name
CHAFI
Last Name (AR)
شافي
First Name
BILAL
First Name (AR)
بلال
Birth Date
2001-01-22
Birth Place
RABAT
Birth Place (AR)
الرياة
Card Number
AS13538
Expiry Date
2029-03-19
Gender
M

Prompt
▼
System
Extract fields from Moroccan CNIE card OCR.
Think in 2-3 short lines max, then output the JSON.
{"last_name_fr":"","last_name_ar":"","first_name_fr":"","first_name_ar":"","birth_date":"","birth_place_fr":"","birth_place_ar":"","card_number":"","expiry_date":"","gender":""}
- strip "a " prefix from birth_place_fr
- OCR may garble text. If FR and AR refer to the same value, use the clearer one to correct the other.
- null if missing
User
المعربية
المملكة
ROYAUME DU MAROC
للتعريف
البطاقة الوطنية
CARTE NATIONALE D'IDENTITE
بلال
BILAL
شافي
CHAFI
Né le
22.01.2001
مزداد بتانيخ
الرياة
a RABAT
Valable jusqu'au
19.03.2029
صالحة الى غاية
AS13538
M
المدير العام للإمن الوطنى
Thy
عبد اللطيّف حموشي

Raw Output
▼
<|channel|>analysis<|message|>We need to extract fields. The OCR text includes:

Arabic: "المعربية" maybe "المعربية" but likely "المعربية" is part of "المعربية" maybe "المعربية" but actual name? The card shows "بلال" and "BILAL" as last name? Actually "بلال" is first name? Wait: The card shows:

Arabic: "بلال" (BILAL) and "شافي" (CHAFI). So likely last name is "شافي" (CHAFI) and first name is "بلال" (BILAL). The French side shows "BILAL" and "CHAFI" as well. So last_name_fr = "CHAFI", last_name_ar = "شافي". first_name_fr = "BILAL", first_name_ar = "بلال".

Birth date: "22.01.2001" (22 Jan 2001). So birth_date = "2001-01-22" maybe format? They didn't specify format. Use "2001-01-22" or "22.01.2001"? Probably "2001-01-22" is better. But we can output "2001-01-22".

Birth place: French: "a RABAT" but we need strip "a " prefix. So "RABAT". Arabic: "الرياة" maybe "الرياة" but likely "الرياة" is "الرياة" maybe "الرياة" but actual place is "الرياة" maybe "الرياة" but we can use "الرياة". But we can correct using French: "RABAT". So birth_place_fr = "RABAT", birth_place_ar = "الرياة" or maybe "الرياة" but we can correct to "الرياة" but maybe "الرياة" is "الرياة". But we can use "الرياة" as Arabic. But we can also correct to "الرياة" but maybe "الرياة" is "الرياة". Let's keep as "الرياة".

Card number: "AS13538" maybe "AS13538". So card_number = "AS13538".

Expiry date: "19.03.2029" (19 March 2029). So expiry_date = "2029-03-19".

Gender: "M" indicates male. So gender = "M".

Now produce JSON.<|end|><|start|>assistant<|channel|>final<|message|>{"last_name_fr":"CHAFI","last_name_ar":"شافي","first_name_fr":"BILAL","first_name_ar":"بلال","birth_date":"2001-01-22","birth_place_fr":"RABAT","birth_place_ar":"الرياة","card_number":"AS13538","expiry_date":"2029-03-19","gender":"M"}

Raw OCR Detections (23)
▼
المعربية
93%
المملكة
93%
ROYAUME DU MAROC
100%
للتعريف
96%
البطاقة الوطنية
97%
CARTE NATIONALE D'IDENTITE
99%
بلال
95%
BILAL
100%
شافي
99%
CHAFI
100%
Né le
87%
22.01.2001
92%
مزداد بتانيخ
88%
الرياة
71%
a RABAT
90%
Valable jusqu'au
100%
19.03.2029
100%
صالحة الى غاية
97%
AS13538
100%
M
100%
المدير العام للإمن الوطنى
97%
Thy
53%
عبد اللطيّف حموشي
91%