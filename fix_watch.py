import re

with open('src/views/PresenterView.vue', 'r') as f:
    content = f.read()

find_str = "watch([showArabic, showTranslation, showTransliteration, autoFit], () => {\n  applySizes();\n})"
replace_str = "watch([showArabic, showTranslation, showTransliteration, autoFit, arabicFont, englishFont, urduFont, currentIndex], () => {\n  applySizes();\n})"

if find_str in content:
    content = content.replace(find_str, replace_str)
    with open('src/views/PresenterView.vue', 'w') as f:
        f.write(content)
        print("Replaced watch successfully")
else:
    print("Could not find string")
