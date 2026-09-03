import os, glob, re

base_dir = '/home/asr11/ASHER/לקוחות חדשים אפיון צרכים ואפשרויות/alu-on.co.il/staging/preview/alu-on.co.il/'

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

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
    # skip index.html since it was already modified
    if html_file == base_dir + 'index.html': continue
    
    with open(html_file, 'r') as f: content = f.read()
    
    # Preload and Google fonts
    if '<link rel="icon"' in content:
        content = re.sub(r'(<link rel="icon".*?>)', r'\1' + '\n' + preload_img + google_fonts, content)
    else:
        content = re.sub(r'(<head.*?>)', r'\1' + '\n' + preload_img + google_fonts, content, flags=re.IGNORECASE)
    
    content = content.replace(fa_old, fa_new)
    
    # Defer app.js
    content = re.sub(r'(<script id="aluon-app-js" src="[^"]*?")\s*(>)', r'\1 defer\2', content)
    
    # Fetchpriority to hero
    content = re.sub(r'(<img[^>]*src="[^"]*section1\.webp"[^>]*loading="eager"[^>]*)>', r'\1 fetchpriority="high">', content)
    
    # Lazy load footer logo
    content = re.sub(r'(<img[^>]*src="[^"]*logo\.svg"[^>]*)>', lambda m: m.group(1) + ' loading="lazy">' if 'loading=' not in m.group(1) else m.group(0), content)

    with open(html_file, 'w') as f: f.write(content)
print(f"Modified {len(html_files)-1} other HTML files")
