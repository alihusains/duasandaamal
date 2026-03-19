export function getFontConfig(langCode) {
  // Read font preferences from localStorage or fallback to defaults
  const arabicFont = localStorage.getItem('arabicFont') || 'Al-Qalam';
  const englishFont = localStorage.getItem('englishFont') || 'RobotoFlex';
  const urduFont = localStorage.getItem('urduFont') || 'NotoNastaliqUrdu';

  const config = {
    arabic: arabicFont,
    transliteration: englishFont,
    english: englishFont,
  };

  // Set translation font based on the app language
  if (langCode === 'ur') {
    config.translation = urduFont;
  } else if (langCode === 'gu') {
    config.translation = 'DnaGujarati';
  } else {
    config.translation = englishFont;
  }

  return config;
}
