Mistral-Nemo-12B (ID-assign)
66.5s
Last Name
BILAL
Last Name (AR)
بلال
First Name
CHAFI
First Name (AR)
شافي
Birth Date
22.01.2001
Birth Place
RABAT
Birth Place (AR)
الرباط
Card Number
AS13538
Expiry Date
19.03.2029
Gender
M

Prompt
▼
System
Vous êtes un extracteur JSON pour carte nationale d'identité marocaine (CNIE).

Tâche : À partir des lignes OCR numérotées, indiquez pour chaque champ UN SEUL numéro de ligne (entier).

Contraintes :
- [LABEL] = étiquette fixe. Ne jamais utiliser comme valeur.
- Les champs _ar DOIVENT pointer vers une ligne [AR].
- Les champs _fr DOIVENT pointer vers une ligne [FR].
- Aucun doublon : chaque numéro de ligne est utilisé AU PLUS UNE FOIS.
- Si le champ est absent ou illisible, mettez null.
- Renvoyez UNIQUEMENT l'objet JSON, sans texte avant ou après.

Comment identifier les noms :
  Les noms apparaissent comme 2 PAIRES consécutives juste après les en-têtes [LABEL].
  Chaque paire = une ligne [AR] suivie d'une ligne [FR] avec le MÊME nom dans les deux écritures.
  Paire 1 (plus haut) = last_name (nom de famille). Paire 2 (juste en dessous) = first_name (prénom).
  IMPORTANT : last_name et first_name sont deux mots DIFFÉRENTS. Si vous trouvez le même mot
  pour les deux, c'est une erreur — cherchez le mot différent sur les lignes adjacentes.
  Indice : une ligne [AR] et la ligne [FR] juste à côté qui contiennent des lettres-only
  (pas de chiffres, pas de dates) forment une paire nom.

Champs : last_name_fr, last_name_ar, first_name_fr, first_name_ar,
         birth_date, birth_place_fr, birth_place_ar, card_number, expiry_date, gender

Exemple d'entrée :
[0] [LABEL] المملكة
[1] [LABEL] ROYAUME DU MAROC
[2] [LABEL] البطاقة الوطنية
[3] [LABEL] CARTE NATIONALE D'IDENTITE
[4] [AR] العلوي
[5] [FR] ALAOUI
[6] [AR] محمد
[7] [FR] MOHAMMED
[8] [LABEL] Né le
[9] [FR] 15.06.1990
[10] [LABEL] مزداد بتاريخ
[11] [AR] الدار البيضاء
[12] [FR] a CASABLANCA
[13] [LABEL] Valable jusqu'au
[14] [FR] 20.06.2030
[15] [LABEL] صالحة الى غاية
[16] [FR] AB123456
[17] [FR] M

Exemple de sortie :
{"last_name_fr": 5, "last_name_ar": 4, "first_name_fr": 7, "first_name_ar": 6, "birth_date": 9, "birth_place_fr": 12, "birth_place_ar": 11, "card_number": 16, "expiry_date": 14, "gender": 17}
User
Lignes OCR:

[0] [LABEL] المعربية
[1] [LABEL] المملكة
[2] [LABEL] ROYAUME DU MAROC
[3] [LABEL] للتعريف
[4] [LABEL] البطاقة الوطنية
[5] [LABEL] CARTE NATIONALE D'IDENTITE
[6] [AR] بلال
[7] [FR] BILAL
[8] [AR] شافي
[9] [FR] CHAFI
[10] [LABEL] Né le
[11] [FR] 22.01.2001
[12] [LABEL] مزداد بتانيخ
[13] [AR] الرياة
[14] [FR] a RABAT
[15] [LABEL] Valable jusqu'au
[16] [FR] 19.03.2029
[17] [LABEL] صالحة الى غاية
[18] [FR] AS13538
[19] [FR] M
[20] [FR] Thy

Raw Output
▼
{"last_name_fr": 9, "last_name_ar": 8, "first_name_fr": 7, "first_name_ar": 6, "birth_date": 11, "birth_place_fr": 14, "birth_place_ar": 13, "card_number": 18, "expiry_date": 16, "gender": 19}