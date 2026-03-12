"""
French → Arabic city name lookup for Moroccan cities.
Fixes birth_place_ar after LLM extraction.
"""

_CITY_MAP = {
    "RABAT": "الرباط",
    "CASABLANCA": "الدار البيضاء",
    "FES": "فاس",
    "FEZ": "فاس",
    "MARRAKECH": "مراكش",
    "MARRAKESH": "مراكش",
    "TANGER": "طنجة",
    "TANGIER": "طنجة",
    "AGADIR": "أكادير",
    "MEKNES": "مكناس",
    "OUJDA": "وجدة",
    "KENITRA": "القنيطرة",
    "TETOUAN": "تطوان",
    "SAFI": "آسفي",
    "MOHAMMEDIA": "المحمدية",
    "KHOURIBGA": "خريبكة",
    "EL JADIDA": "الجديدة",
    "BENI MELLAL": "بني ملال",
    "NADOR": "الناظور",
    "TAZA": "تازة",
    "SETTAT": "سطات",
    "BERRECHID": "برشيد",
    "KHEMISSET": "الخميسات",
    "INEZGANE": "إنزكان",
    "KSAR EL KEBIR": "القصر الكبير",
    "LARACHE": "العرائش",
    "GUELMIM": "كلميم",
    "ERRACHIDIA": "الراشيدية",
    "OUARZAZATE": "ورزازات",
    "SALE": "سلا",
    "TEMARA": "تمارة",
    "IFRANE": "إفران",
    "AZROU": "أزرو",
    "MIDELT": "ميدلت",
    "TAROUDANT": "تارودانت",
    "TIZNIT": "تيزنيت",
    "ESSAOUIRA": "الصويرة",
    "AL HOCEIMA": "الحسيمة",
    "CHEFCHAOUEN": "شفشاون",
    "DAKHLA": "الداخلة",
    "LAAYOUNE": "العيون",
    "TAN TAN": "طانطان",
    "SIDI KACEM": "سيدي قاسم",
    "SIDI SLIMANE": "سيدي سليمان",
    "TAOURIRT": "تاوريرت",
    "BERKANE": "بركان",
    "FIGUIG": "فجيج",
    "JERADA": "جرادة",
    "BOUARFA": "بوعرفة",
    "SEFROU": "صفرو",
    "AZILAL": "أزيلال",
    "DEMNATE": "دمنات",
    "CHICHAOUA": "شيشاوة",
    "BENSLIMANE": "بنسليمان",
    "SIDI BENNOUR": "سيدي بنور",
    "YOUSSOUFIA": "اليوسفية",
    "BEN GUERIR": "ابن جرير",
    "KELAAT SRAGHNA": "قلعة السراغنة",
    "TIFLET": "تيفلت",
    "SOUK EL ARBAA": "سوق الأربعاء",
}


def fix_city_arabic(fields):
    """
    Override birth_place_ar with correct Arabic if birth_place_fr is a known city.
    Modifies fields dict in place and returns it.
    """
    city_fr = (fields.get("birth_place_fr") or "").strip().upper()
    if city_fr in _CITY_MAP:
        fields["birth_place_ar"] = _CITY_MAP[city_fr]
    return fields
