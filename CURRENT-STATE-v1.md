# CURRENT-STATE-v2 — alu-on.co.il (פרודקשן מאומת)

> **מצב:** READ-ONLY — אפס שינויים  
> **תאריך:** 2026-08-30 12:53  
> **שיטה:** `curl -sL` לכל דף חי + SHA-256 + השוואה לקבצים מקומיים  
> **WordPress הוסר בעקבות פריצה. אינו חלק מארכיטקטורת הפרודקשן.**

---

## ⚠️ ממצא מרכזי: הפרודקשן אינו זהה למקומי

> [!CAUTION]
> **אף קובץ לא תואם בינארית (SHA-256) בין הפרודקשן לתיקייה המקומית.**
> - `app.js` פרודקשן = **21,326 bytes** (ver=1.0.1) | מקומי = **17,780 bytes** (ver=1.0.0)
> - `style.css` פרודקשן = SHA `8ddfac77...` (ver=1.0.1) | מקומי = SHA `19337db8...` (ver=1.0.0)
> - `index.html` פרודקשן = **609 שורות, 36KB** | מקומי = **644 שורות, 51KB**
> - דפי `/specs/*.html` — **שונים לחלוטין** בין פרודקשן למקומי

---

## 1. Sitemap חי — 21 כתובות

```
https://alu-on.co.il/                                    priority=1.0
https://alu-on.co.il/about/                              priority=0.8
https://alu-on.co.il/projects/                           priority=0.9
https://alu-on.co.il/articles/                           priority=0.9
https://alu-on.co.il/aluminum/                           priority=0.8
https://alu-on.co.il/alucobond/                          priority=0.8
https://alu-on.co.il/hpl/                                priority=0.8
https://alu-on.co.il/curtain-walls/                      priority=0.8
https://alu-on.co.il/architects/                         priority=0.7
https://alu-on.co.il/contact/                            priority=0.8
https://alu-on.co.il/curtain-wall-systems-architectural-guide/  priority=0.7
https://alu-on.co.il/hpl-exterior-cladding-israel/       priority=0.7
https://alu-on.co.il/alucobond-facade-cladding-guide/    priority=0.7
https://alu-on.co.il/specs/aluminum-2mm-spec.html        priority=0.6
https://alu-on.co.il/specs/alucobond-spec.html           priority=0.6
https://alu-on.co.il/specs/hpl-spec.html                 priority=0.6
https://alu-on.co.il/specs/curtain-wall-spec.html        priority=0.6
https://alu-on.co.il/privacy-policy/                     priority=0.3
https://alu-on.co.il/terms/                              priority=0.3
https://alu-on.co.il/accessibility/                      priority=0.3
```

**דפים לא ב-sitemap אך נגישים:** `/thank-you/`, `/downloads/`

**סטטוס:** VERIFIED | **מקור:** `curl -sL https://alu-on.co.il/sitemap.xml`

---

## 2. טבלת השוואה — פרודקשן מול מקומי

| URL | HTTP | WA 050 PROD | WA 050 LOCAL | WA 052 PROD | WA 052 LOCAL | TEL 050 PROD | TEL 050 LOCAL | SHA תואם | הערה |
|-----|------|-------------|-------------|-------------|-------------|-------------|--------------|----------|------|
| `/` | 200 | 0 | 0 | 5 | 5 | 5 | 5 | ❌ | שורות/גודל שונים; כמויות WA/TEL זהות |
| `/about/` | 200 | 0 | 0 | 4 | 4 | 4 | 4 | ❌ | מספרים זהים |
| `/contact/` | 200 | 0 | 0 | 5 | 5 | 5 | 5 | ❌ | מספרים זהים |
| `/thank-you/` | 200 | **5** | **5** | 0 | 0 | 4 | 4 | ❌ | ⚠️ **050 כ-WA — חי בפרודקשן** |
| `/terms/` | 200 | **4** | **4** | 0 | 0 | 4 | 4 | ❌ | ⚠️ **050 כ-WA — חי בפרודקשן** |
| `/privacy-policy/` | 200 | 0 | 0 | 5 | 5 | 5 | 5 | ❌ | תקין |
| `/accessibility/` | 200 | 0 | 0 | 5 | 5 | 5 | 5 | ❌ | תקין |
| `/aluminum/` | 200 | 0 | 0 | **6** | **5** | 4 | 4 | ❌ | פרודקשן יש WA052 נוסף (כפתור מפרט עם onclick alert) |
| `/alucobond/` | 200 | 0 | 0 | **6** | **5** | 4 | 4 | ❌ | כנ"ל |
| `/hpl/` | 200 | 0 | 0 | **6** | **5** | 4 | 4 | ❌ | כנ"ל |
| `/curtain-walls/` | 200 | 0 | 0 | **6** | **5** | 4 | 4 | ❌ | כנ"ל |
| `/architects/` | 200 | 0 | 0 | **8** | **4** | 4 | 4 | ❌ | **פרודקשן יש 4 WA נוספים** |
| `/articles/` | 200 | 0 | 0 | 4 | 4 | 4 | 4 | ❌ | |
| `/projects/` | 200 | 0 | 0 | 4 | 4 | 4 | 4 | ❌ | |
| `/alucobond-facade-cladding-guide/` | 200 | 0 | 0 | 5 | 5 | 4 | 4 | ❌ | |
| `/hpl-exterior-cladding-israel/` | 200 | 0 | 0 | 5 | 5 | 4 | 4 | ❌ | |
| `/curtain-wall-systems...guide/` | 200 | 0 | 0 | 5 | 5 | 4 | 4 | ❌ | |
| **`/specs/aluminum-2mm-spec.html`** | 200 | 0 | 0 | **0** | **4** | **0** | **4** | ❌ | 🔴 **ראה סעיף 3** |
| **`/specs/alucobond-spec.html`** | 200 | 0 | 0 | **0** | **4** | **0** | **4** | ❌ | 🔴 **כנ"ל** |
| **`/specs/hpl-spec.html`** | 200 | 0 | 0 | **0** | **4** | **0** | **4** | ❌ | 🔴 **כנ"ל** |
| **`/specs/curtain-wall-spec.html`** | 200 | 0 | 0 | **0** | **4** | **0** | **4** | ❌ | 🔴 **כנ"ל** |
| `/downloads/` | 200 | 0 | — | 5 | — | 5 | — | N/A | קובץ מקומי ריק — ב-prod מוגש דף תקין |

---

## 3. 🔴 ממצא קריטי: דפי specs בפרודקשן = גרסה שונה לחלוטין

> [!CAUTION]
> **דפי `/specs/*.html` בפרודקשן שונים לגמרי מהקבצים המקומיים.**

| מאפיין | פרודקשן (חי) | מקומי |
|---------|-------------|-------|
| טלפון | **058-700-8133** (`tel:+972587008133`) | 050-999-7753 (`tel:+972509997753`) |
| WhatsApp | **058-700-8133** (`wa.me/972587008133`) | 052-588-7454 (`wa.me/972525887454`) |
| Header | minimal — אין social float, אין accessibility | full header כמו שאר הדפים |
| CSS | `../styles.css` (relative) | inline + `/wp-content/themes/...` |
| Footer | שורה אחת: `© 2026 האב מערכות + 058-7008133` | full footer כמו שאר הדפים |
| ניווט | קישורים ל-`../index.html`, `../about.html` | קישורים ל-`/about/`, `/contact/` |
| a11y widget | **אין** | יש |

> [!WARNING]
> **מספר טלפון 058-700-8133 מופיע רק בפרודקשן ב-specs — לא קיים בשום קובץ מקומי.**
> מקורו לא ידוע. הקבצים המקומיים נכתבו מחדש אך **לא פורסמו**.
> הגולש שנכנס לדפי specs מקבל מספר אחר מכל שאר האתר.

---

## 4. מספרי טלפון — מצב אמיתי בפרודקשן

| מספר | סוג | איפה חי | תקין? |
|------|------|---------|-------|
| **050-999-7753** | `tel:` שיחה | כל הדפים מלבד specs | ✅ |
| **052-588-7454** | `wa.me` WhatsApp | כל הדפים מלבד specs + thank-you + terms | ✅ |
| **050-999-7753** | `wa.me` WhatsApp | **thank-you + terms** | ❌ **050 אינו WA** |
| **058-700-8133** | `tel:` + `wa.me` | **specs (4 דפים)** | ❓ **לא מוכר** |

---

## 5. גרסאות נכסים — drift

| נכס | פרודקשן | מקומי | SHA תואם |
|-----|---------|-------|----------|
| `app.js` | **ver=1.0.1** (21,326 B) | ver=1.0.0 (17,780 B) | ❌ `3837...` vs `76cc...` |
| `style.css` | **ver=1.0.1** | ver=1.0.0 | ❌ `8ddf...` vs `1933...` |
| `accessibility.css` | קיים ונטען (plugin) | קיים מקומית | לא נבדק |

> [!IMPORTANT]
> **הפרודקשן מריץ גרסה חדשה יותר** של app.js ו-style.css מזו השמורה מקומית.
> אותן פונקציות (12 functions) — אך גודל שונה. ייתכן שבפרודקשן יש תוכן נוסף (privacy consent כפול?).

---

## 6. טפסים וסקריפטים — מצב חי

| רכיב | פרודקשן | סטטוס |
|-------|---------|--------|
| `#contactForm` | `action="javascript:void(0)"` → `initContactForm()` → `wa.me/972525887454` | VERIFIED — **WhatsApp בלבד, אפס שמירה** |
| Calculator | `wa.me/972525887454` עם טקסט הצעה מפורט | VERIFIED |
| `app.js` | נטען עם `defer` + `ver=1.0.1` | VERIFIED |
| `fetch`/`sendBeacon`/`gtag`/`pixel` | **לא קיים** | VERIFIED |
| Privacy consent | `initPrivacyConsentSystem()` — localStorage בלבד | VERIFIED |

---

## 7. מה נשאר מ-WordPress — פרודקשן

| שריד | בפרודקשן? | מזיק? |
|-------|-----------|-------|
| `wp-emoji-loader` inline | **כן** — 5 מופעים (speculationrules, emoji settings, emoji JS) | ⚠️ מנסה לטעון `wp-includes/js/wp-emoji-release.min.js` שלא קיים — 404 שקט |
| Redis cache comment | **כן** — `<!-- Retrieved 546 objects from Redis -->` | אפס — HTML comment |
| oEmbed JSON/XML links | **כן** — `wp-json/oembed/...` | ⚠️ מצביע על WP API שלא פעיל |
| `speculationrules` | **כן** — prefetch rules שמוציאות `wp-*.php` | לא מזיק אבל מיותר |
| `wp-content/` paths | **כן** — CSS, JS, images | תקינים — אלו הנכסים הפעילים |

---

## 8. סיכום מצב — מה הגולש מקבל עכשיו

```
┌─────────────────────────────────────────────────────┐
│              פרודקשן alu-on.co.il                    │
│                                                      │
│ דפים ראשיים (/, /contact/, /about/ וכו'):           │
│   📞 שיחה: tel:050-999-7753                 ✅      │
│   💬 WA:   wa.me/972525887454 (052)         ✅      │
│   📝 טופס: WhatsApp only, אפס שמירה        ⚠️      │
│   📊 אנליטיקה: אפס                         ⚠️      │
│                                                      │
│ דף /thank-you/ + /terms/:                            │
│   💬 WA: wa.me/972509997753 (050)           ❌ שגוי │
│                                                      │
│ דפי /specs/* (4 דפים):                              │
│   📞 שיחה: tel:058-700-8133                 ❓ מוכר?│
│   💬 WA:   wa.me/972587008133 (058)         ❓ מוכר?│
│   📐 Layout: שונה לחלוטין, אין a11y widget          │
│                                                      │
│ נכסים:                                               │
│   app.js:   ver=1.0.1 (≠ מקומי 1.0.0)              │
│   style.css: ver=1.0.1 (≠ מקומי 1.0.0)             │
│                                                      │
│ קבצים מקומיים ≠ פרודקשן בכל הפרמטרים               │
└─────────────────────────────────────────────────────┘
```

---

## 9. שאלה שלא ניתן לאמת טכנית

| שאלה | נדרש |
|-------|------|
| **מהו מספר 058-700-8133?** של מי הוא? האם עדיין תקף? | אישור בעל הפרויקט |
| מתי בוצע ה-deploy האחרון לפרודקשן? | `wrangler pages deployment list` (נבדק בעבר — ~1 שבוע) |
| למה app.js ו-style.css שונים? האם הגרסה המקומית חדשה יותר או ישנה יותר? | בעל הפרויקט / היסטוריית deploys |

---

> **לא בוצעו שינויים. אין הצעות ארכיטקטורה. אין קוד. אין deploy.**
