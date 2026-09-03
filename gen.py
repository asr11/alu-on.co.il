import os, json, subprocess, re

# Fetch the 3 posts from WP-CLI
cmd = "wp post list --post__in=46,47,48 --format=json --fields=post_name,post_title,post_content,post_date"
res = subprocess.run(cmd, cwd='/var/www/alu-on.co.il/', shell=True, capture_output=True, text=True)
posts = json.loads(res.stdout)

# Read the template from an existing article
template_path = '/var/www/alu-on.co.il/alucobond-facade-cladding-guide/index.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template_html = f.read()

# Split into head, main, and footer
head_part, rest = template_html.split('<main role="main"', 1)
main_part, footer_part = rest.split('</main>', 1)
# The head_part ends right before <main role="main".
# The footer_part starts right after </main>.

# Helper function to generate an article card
def make_card(post_title, post_name, post_date_str):
    return f"""      <article class="pillar-card post-card" onclick="window.location.href='/{post_name}/';" style="cursor: pointer;" tabindex="0" role="link" onkeydown="if(event.key === 'Enter' || event.key === ' ') {{ this.click(); }}">
        <div class="pillar-img-box">
          <a href="/{post_name}/" aria-label="{post_title}">
            <img src="/wp-content/themes/aluon-wp-theme/images/alucobond.webp" alt="{post_title}" width="600" height="400" loading="lazy">
          </a>
        </div>
        <small style="color:var(--foreground-muted); display:block; margin-top:0.75rem;">21 באוגוסט 2026</small>
        <h3 style="margin-top:0.4rem;" class="card-post-title">
          <a href="/{post_name}/" class="title-link">{post_title}</a>
        </h3>
        <p>לחץ לקריאת המאמר המלא ולהרחבת הידע המקצועי.</p>
        <a href="/{post_name}/" class="card-link-arrow">לקריאת המאמר המלא ←</a>
      </article>"""

cards = []

for p in posts:
    slug = p['post_name']
    title = p['post_title']
    content = p['post_content']
    date = p['post_date']
    
    # 1. Prepare HTML
    new_head = head_part
    new_head = re.sub(r'<title>.*?</title>', f'<title>{title} – Alu-on Group</title>', new_head)
    new_head = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title} – Alu-on Group">', new_head)
    new_head = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="https://alu-on.co.il/{slug}/">', new_head)
    new_head = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="/{slug}/">', new_head)
    
    # Clean WP Gutenberg tags
    content = content.replace('<!-- wp:html -->', '').replace('<!-- /wp:html -->', '').strip()
    
    # Assemble
    full_html = new_head + content + footer_part
    
    # Write to file
    out_dir = f'/var/www/alu-on.co.il/{slug}'
    os.makedirs(out_dir, exist_ok=True)
    with open(f'{out_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"Generated {slug}/index.html")
    cards.append(make_card(title, slug, date))

# Update articles/index.html
articles_index = '/var/www/alu-on.co.il/articles/index.html'
with open(articles_index, 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Make sure we don't duplicate
if cards[0] not in idx_content:
    idx_content = idx_content.replace('      </article>\n          </div>\n  </section>', '      </article>\n' + '\n'.join(cards) + '\n    </div>\n  </section>')
    with open(articles_index, 'w', encoding='utf-8') as f:
        f.write(idx_content)
    print("Updated articles/index.html")
else:
    print("Cards already in articles/index.html")
