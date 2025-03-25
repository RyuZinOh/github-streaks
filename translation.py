from typing import Union, Dict, List, TypedDict
from dataclasses import dataclass

class TranslationStrings(TypedDict):
    access_denied: List[str]
    total_contributions: str
    ongoing_streak: str
    days: str
    year_progress: str
    months: Dict[int, str]

@dataclass
class LanguageConfig:
    strings: TranslationStrings
    numerals: List[str] = None
    font_family: str = "font-family: 'Poppins', sans-serif;"

class TranslationService:
    def __init__(self):
        self._languages: Dict[str, LanguageConfig] = {
            #english
            "en": LanguageConfig(
                strings={
                    "access_denied": [
                        "Access Denied", 
                        "You are not authorized to use this route.",
                        "Please contact the administrator if you believe",
                        "this is a mistake."
                    ],
                    "total_contributions": "Total Contributions",
                    "ongoing_streak": "Ongoing Streak",
                    "days": "DAYS",
                    "year_progress": "{}% of {} completed",
                    "months": {
                        1: "January",
                        2: "February",
                        3: "March",
                        4: "April",
                        5: "May",
                        6: "June",
                        7: "July",
                        8: "August",
                        9: "September",
                        10: "October",
                        11: "November",
                        12: "December"
                    }
                }
            ),
            #nepali 
            "ne": LanguageConfig(
                strings={
                    "access_denied": [
                        "प्रवेश अस्वीकृत",
                        "तपाईंलाई यो मार्ग प्रयोग गर्न अनुमति छैन।",
                        "कृपया प्रशासकलाई सम्पर्क गर्नुहोस् यदि तपाईंलाई लाग्छ",
                        "यो गल्ती हो।"
                    ],
                    "total_contributions": "कुल योगदान",
                    "ongoing_streak": "चालु स्ट्रिक",
                    "days": "दिन",
                    "year_progress": "{}% {} पूरा भयो",
                    "months": {
                        1: "जनवरी",
                        2: "फेब्रुअरी",
                        3: "मार्च",
                        4: "अप्रिल",
                        5: "मे",
                        6: "जुन",
                        7: "जुलाई",
                        8: "अगस्ट",
                        9: "सेप्टेम्बर",
                        10: "अक्टोबर",
                        11: "नोभेम्बर",
                        12: "डिसेम्बर"
                    }
                },
                numerals=['\u0966', '\u0967', '\u0968', '\u0969', '\u096A', 
                         '\u096B', '\u096C', '\u096D', '\u096E', '\u096F'],
                font_family="font-family: 'Mangal', 'Poppins', 'Noto Sans Devanagari', sans-serif;"
            )
            ,
            # japanese
"ja": LanguageConfig(
    strings={
        "access_denied": [
            "アクセス拒否",
            "このルートを使用する権限がありません。",
            "間違いだと思われる場合は、",
            "管理者に連絡してください。"
        ],
        "total_contributions": "総コントリビューション",
        "ongoing_streak": "現在のストリーク",
        "days": "日",
        "year_progress": "{}% 進捗 ({}年)",
        "months": {
            1: "1月",
            2: "2月",
            3: "3月",
            4: "4月",
            5: "5月",
            6: "6月",
            7: "7月",
            8: "8月",
            9: "9月",
            10: "10月",
            11: "11月",
            12: "12月"
        }
    },
    numerals=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    font_family="font-family: 'Noto Sans JP', 'Poppins', sans-serif;"
)
        }

# NECESSARY DEFINATIONS

    def get_supported_languages(self) -> List[str]:
        return list(self._languages.keys())

    def get_language_config(self, lang: str = "en") -> LanguageConfig:
        return self._languages.get(lang, self._languages["en"])

    def convert_to_local_numeral(self, value: Union[int, float, str], lang: str = "en") -> str:
        config = self.get_language_config(lang)
        if not config.numerals:
            return str(value)
        
        num_str = str(value)
        result = []
        
        for char in num_str:
            if char.isdigit():
                try:
                    result.append(config.numerals[int(char)])
                except (ValueError, IndexError):
                    result.append(char)
            else:
                result.append(char)
        
        return ''.join(result)

    def get_month_name(self, month: int, lang: str = "en") -> str:
        config = self.get_language_config(lang)
        return config.strings["months"].get(month, "")

    def get_translation(self, key: str, lang: str = "en") -> str:
        config = self.get_language_config(lang)
        return config.strings.get(key, key)

    def get_font_style(self, lang: str = "en") -> str:
        config = self.get_language_config(lang)
        return config.font_family

translation_service = TranslationService()