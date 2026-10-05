import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Google Fonts link to include EB Garamond
old_link = 'family=Cardo:ital,wght@0,400;0,700;1,400&display=swap'
new_link = 'family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700&family=Cardo:ital,wght@0,400;0,700;1,400&display=swap'
if old_link in content:
    content = content.replace(old_link, new_link)

# We want to replace instances of 'Inter' and 'Cardo' with 'EB Garamond' where appropriate for English.
# The user wants the whole site to feel like that classic dictionary look.
# So we'll replace the main font families:
# `font-family: 'Cardo', 'ebl', 'Inter', -apple-system, sans-serif;` -> `'EB Garamond', 'Amiri', serif;`
# `font-family: 'Inter', sans-serif;` -> `'EB Garamond', 'Amiri', serif;`

content = re.sub(r"font-family:\s*'Cardo',\s*'ebl',\s*'Inter',\s*-apple-system,\s*sans-serif;", "font-family: 'EB Garamond', 'Amiri', serif;", content)
content = re.sub(r"font-family:\s*'Inter',\s*sans-serif;", "font-family: 'EB Garamond', 'Amiri', serif;", content)
content = re.sub(r"font-family:\s*'Cardo',\s*sans-serif;", "font-family: 'EB Garamond', 'Amiri', serif;", content)
content = re.sub(r"font-family:\s*'Cardo',\s*'ebl',\s*'Inter',\s*sans-serif;", "font-family: 'EB Garamond', 'Amiri', serif;", content)
content = re.sub(r"font-family:\s*'Cardo',\s*serif;", "font-family: 'EB Garamond', 'Amiri', serif;", content)
content = re.sub(r"font-family:\s*'Amiri',\s*serif;", "font-family: 'EB Garamond', 'Amiri', serif;", content)
content = re.sub(r"font-family:\s*'Scheherazade New',\s*'Amiri',\s*serif;", "font-family: 'EB Garamond', 'Amiri', 'Scheherazade New', serif;", content)
content = re.sub(r"font-family:\s*var\(--cuneiform-font\);", "font-family: var(--cuneiform-font);", content) # don't touch cuneiform

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fonts updated!")
