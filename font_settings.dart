/// Centralized font configuration per language.
///
/// For each language code, specify which font to use for each content type.
/// If a font is `null`, the system default will be used.
class LanguageFontConfig {
  final String? arabic;
  final String? langName;
  final String? languageTitle;
  final String? translation;
  final String? transliteration;
  final String? englishName;
  final String? english;

  const LanguageFontConfig({
    this.arabic,
    this.langName,
    this.languageTitle,
    this.translation,
    this.transliteration,
    this.englishName,
    this.english,
  });
}

/// Default fallback config used when a language has no specific entry.
const _defaultConfig = LanguageFontConfig(
  arabic: 'ShiaEssentials',
  langName: 'NotoSans',
  languageTitle: 'NotoSans',
  translation: 'NotoSans',
  transliteration: 'Notosans',
  englishName: 'NotoSans',
  english: 'NotoSans',
);

/// Per-language font mappings.
/// Add or modify entries here to control fonts for each language.
const Map<String, LanguageFontConfig> _languageFonts = {
  'en': LanguageFontConfig(
    arabic: 'ShiaEssentials',
    langName: 'RobotoFlex',
    languageTitle: 'RobotoFlex',
    translation: 'RobotoFlex',
    transliteration: 'RobotoFlex',
    englishName: 'RobotoFlex',
    english: 'RobotoFlex',
  ),
  'gu': LanguageFontConfig(
    arabic: 'ShiaEssentials',
    langName: 'DnaGujarati',
    languageTitle: 'DnaGujarati',
    translation: 'DnaGujarati',
    transliteration: 'DnaGujarati',
    englishName: 'NotoSans',
    english: 'NotoSans',
  ),
  'ur': LanguageFontConfig(
    arabic: 'ShiaEssentials',
    langName: 'NotoNastaliqUrdu',
    languageTitle: 'NotoNastaliqUrdu',
    translation: 'NotoNastaliqUrdu',
    transliteration: 'NotoSans',
    englishName: 'NotoSans',
    english: 'NotoSans',
  ),
};

/// Returns the font config for the given language code.
/// Falls back to [_defaultConfig] if no specific config exists.
LanguageFontConfig getFontConfig(String langCode) {
  return _languageFonts[langCode] ?? _defaultConfig;
}
