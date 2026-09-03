import os
import re

staging_dir = "/home/asr11/ASHER/לקוחות חדשים אפיון צרכים ואפשרויות/alu-on.co.il/staging/preview/alu-on.co.il"

# 1. SVGs (P0-20 to P0-22)
images_dir = os.path.join(staging_dir, "wp-content/themes/aluon-wp-theme/images")
os.makedirs(images_dir, exist_ok=True)
svg_template = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <rect width="100%" height="100%" fill="#eee"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="24" fill="#666">{text}</text>
</svg>'''

for img in ["hero.jpg", "pivot_door.jpg", "pergola.jpg"]:
    with open(os.path.join(images_dir, img), "w") as f:
        f.write(svg_template.format(text=img))

modified_files = set()
fixes_applied = 0

def update_file(path, content):
    global fixes_applied, modified_files
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    modified_files.add(path)

for root, _, files in os.walk(staging_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            original_content = content
            
            # P0-01 to P0-06
            if path.endswith("index.html") and root == staging_dir:
                content, n = re.subn(r'href="/about\.html"', r'href="/about/"', content)
                fixes_applied += n
                content, n = re.subn(r'href="/claddings/aluminum\.html"', r'href="/aluminum/"', content)
                fixes_applied += n
                content, n = re.subn(r'href="/claddings/alucobond\.html"', r'href="/alucobond/"', content)
                fixes_applied += n
                content, n = re.subn(r'href="/claddings/hpl\.html"', r'href="/hpl/"', content)
                fixes_applied += n
                content, n = re.subn(r'href="/claddings/curtain-walls\.html"', r'href="/curtain-walls/"', content)
                fixes_applied += n
                content, n = re.subn(r'href="/projects\.html"', r'href="/projects/"', content)
                fixes_applied += n
                
                # P0-29 Calculator disclaimer
                if 'id="calculator-output"' in content and "האומדן להמחשה בלבד" not in content:
                    content = re.sub(
                        r'(<div id="calculator-output"[^>]*>.*?</div>)',
                        r'\1\n          <div class="disclaimer" style="margin-top:1rem; font-size:0.9rem; color:#666;">∗ האומדן להמחשה בלבד. המחיר הסופי תלוי במפרט, בתנאי השוק ובמורכבות הפרויקט.</div>',
                        content, flags=re.DOTALL
                    )
                    fixes_applied += 1

            # P0-25 form action and disclaimer
            if '<form id="contactForm"' in content:
                content, n = re.subn(r'(<form id="contactForm"[^>]*)>', r'\1 action="javascript:void(0)" method="POST">', content)
                fixes_applied += n
                if 'הטופס מפנה אל WhatsApp' not in content:
                    content, n = re.subn(r'(</form>)', r'\1\n          <div class="disclaimer" style="font-size:0.9rem; margin-top:10px;">הטופס מפנה אל WhatsApp. נתוניך לא נשמרים במערכת.</div>', content)
                    fixes_applied += n

            # P0-27
            if path.endswith("about/index.html"):
                content, n = re.subn(r'\*\*האב מערכות מתקדמות בע"מ\*\*', r'<strong>האב מערכות מתקדמות בע"מ</strong>', content)
                fixes_applied += n

            # P0-28
            if path.endswith("articles/index.html"):
                content, n = re.subn(r'<p>.*?Alu-on group בית פתרונות.*?</p>', r'<p>לחץ לקריאת המאמר המלא ולהרחבת הידע המקצועי.</p>', content)
                fixes_applied += n

            # P0-07 to P0-11
            content, n = re.subn(r'href="\.\./specs/[^"]*\.html"', r'href="#" onclick="alert(\'מפרט יהיה זמין בקרוב\')"', content)
            fixes_applied += n
            content, n = re.subn(r'href="specs/[^"]*\.html"', r'href="#" onclick="alert(\'מפרט יהיה זמין בקרוב\')"', content)
            fixes_applied += n

            # P0-15
            if path.endswith("privacy-policy/index.html"):
                content, n = re.subn(r'http://alu-on\.co\.il/', r'/', content)
                fixes_applied += n

            # P0-17, P0-18
            content, n = re.subn(r'href="/images/logo\.svg"', r'href="/wp-content/themes/aluon-wp-theme/images/logo.svg"', content)
            fixes_applied += n
            content, n = re.subn(r'href="images/logo\.svg"', r'href="/wp-content/themes/aluon-wp-theme/images/logo.svg"', content)
            fixes_applied += n

            # P0-23
            content, n = re.subn(r'<a href="/cdn-cgi/l/email-protection[^>]*>', r'<a href="#" title="צור קשר בטלפון">', content)
            fixes_applied += n

            # P0-24
            content, n = re.subn(r'<a href="#" class="social-icon[^>]*" title="LinkedIn">', r'<a href="#" class="social-icon-btn" title="בקרוב">', content)
            fixes_applied += n
            content, n = re.subn(r'<a href="#" class="social-icon[^>]*" title="Facebook">', r'<a href="#" class="social-icon-btn" title="בקרוב">', content)
            fixes_applied += n
            
            # P0-32 to P0-35
            content, n = re.subn(r'<h4>', r'<h2>', content)
            fixes_applied += n
            content, n = re.subn(r'</h4>', r'</h2>', content)
            fixes_applied += n

            if content != original_content:
                update_file(path, content)

        elif file == "app.js":
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            original_content = content

            # P0-16
            content, n = re.subn(r'articles\.html', r'/articles/', content)
            fixes_applied += n
            content, n = re.subn(r'architects\.html', r'/architects/', content)
            fixes_applied += n
            content, n = re.subn(r'projects\.html', r'/projects/', content)
            fixes_applied += n
            content, n = re.subn(r'about\.html', r'/about/', content)
            fixes_applied += n

            # P0-39
            content, n = re.subn(r'translateX\(-100%\)', r'translateX(100%)', content)
            fixes_applied += n

            if content != original_content:
                update_file(path, content)

print(f"Fixes applied: {fixes_applied}")
print(f"Files modified: {len(modified_files)}")
for f in modified_files:
    print(f)
