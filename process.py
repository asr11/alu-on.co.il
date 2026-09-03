import os, glob, re, subprocess

base_dir = '/home/asr11/ASHER/לקוחות חדשים אפיון צרכים ואפשרויות/alu-on.co.il/staging/preview/alu-on.co.il/'

# 1. logo.svg
subprocess.run(['npx', '-y', 'svgo', base_dir + 'wp-content/themes/aluon-wp-theme/images/logo.svg', '-o', base_dir + 'wp-content/themes/aluon-wp-theme/images/logo.svg'])

# 2. CSS (style.css)
css_path = base_dir + 'wp-content/themes/aluon-wp-theme/style.css'
if os.path.exists(css_path):
    with open(css_path, 'r') as f: css = f.read()
    css = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?family=Rubik.*?swap'\);\n?", '', css)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)  # remove comments
    css = re.sub(r'\s+', ' ', css)  # collapse whitespace
    css = re.sub(r'\s*([{};:,])\s*', r'\1', css)  # remove space around symbols
    with open(css_path, 'w') as f: f.write(css.strip())
    print(f'CSS minified')

# 3. JS (app.js)
js_path = base_dir + 'wp-content/themes/aluon-wp-theme/js/app.js'
if os.path.exists(js_path):
    with open(js_path, 'r') as f: js_lines = f.readlines()
    clean_js = []
    for line in js_lines:
        line = re.sub(r'//.*', '', line)
        line = line.strip()
        if line: clean_js.append(line)
    
    js = ' '.join(clean_js)
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    js = re.sub(r'\s+', ' ', js)
    js = re.sub(r'\s*([{};:,=+\-*/()])\s*', r'\1', js)
    with open(js_path, 'w') as f: f.write(js.strip())
    print(f'JS minified')

# 4. HTML Files
html_files = glob.glob(base_dir + '*.html')

google_fonts = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700;800;900&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700;800;900&display=swap"></noscript>
"""

fa_old = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
fa_new = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>"""

preload_img = '\n'

for html_file in html_files:
    with open(html_file, 'r') as f: content = f.read()
    
    # Preload and Google fonts
    if '<link rel="icon"' in content:
        content = re.sub(r'(<link rel="icon".*?>)', r'\1' + '\n' + preload_img + google_fonts, content)
    else:
        # Fallback to after <head>
        content = re.sub(r'(<head.*?>)', r'\1' + '\n' + preload_img + google_fonts, content, flags=re.IGNORECASE)
    
    content = content.replace(fa_old, fa_new)
    
    # Defer app.js
    content = re.sub(r'(<script id="aluon-app-js" src="[^"]*?")\s*(>)', r'\1 defer\2', content)
    
    # Fetchpriority to hero
    # On the hero image (section1.webp with loading="eager"), add fetchpriority="high"
    content = re.sub(r'(<img[^>]*src="[^"]*section1\.webp"[^>]*loading="eager"[^>]*)>', r'\1 fetchpriority="high">', content)
    
    # Lazy load footer logo
    # Find footer logo and add loading="lazy". We look for logo.svg inside footer.
    # To be safer, we can just find any logo.svg that doesn't have it.
    content = re.sub(r'(<img[^>]*src="[^"]*logo\.svg"[^>]*)>', lambda m: m.group(1) + ' loading="lazy">' if 'loading=' not in m.group(1) else m.group(0), content)

    with open(html_file, 'w') as f: f.write(content)
print("HTML modified")
