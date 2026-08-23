/**
 * Alu-on group (האב מערכות מתקדמות בע"מ) - Application Logic with Instant Search Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initCalculator();
  initContactForm();
  initInstantSearch();
  initMobileMenu();
  initSolutionsDropdown();
  initAccessibilityWidget();
  initPrivacyConsentSystem();
});

/* ==========================================================================
   0. Mobile Hamburger Menu & Solutions Dropdown
   ========================================================================== */
function initMobileMenu() {
  const btn = document.getElementById('hamburgerBtn');
  const menu = document.getElementById('mobileMenu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    btn.classList.toggle('active');
    menu.classList.toggle('open');
    document.body.classList.toggle('menu-open');
    const isExpanded = btn.getAttribute('aria-expanded') === 'true' || false;
    btn.setAttribute('aria-expanded', !isExpanded);
  });

  // Close on link click
  menu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      btn.classList.remove('active');
      btn.setAttribute('aria-expanded', 'false');
      menu.classList.remove('open');
      document.body.classList.remove('menu-open');
    });
  });
}

function initSolutionsDropdown() {
  const trigger = document.getElementById('solutionsDropdownBtn');
  const panel = document.getElementById('solutionsDropdown');
  if (!trigger || !panel) return;

  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    panel.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (!panel.contains(e.target) && e.target !== trigger) {
      panel.classList.remove('open');
    }
  });
}

/* ==========================================================================
   1. Real-Time Cost Estimator & Direct WhatsApp Lead Routing
   ========================================================================== */
function initCalculator() {
  const pillarSelect = document.getElementById('calcPillar');
  const areaInput = document.getElementById('calcArea');
  const areaDisplay = document.getElementById('areaValDisplay');
  const subSelect = document.getElementById('calcSubstructure');
  const priceDisplay = document.getElementById('calcPriceDisplay');
  const whatsappLink = document.getElementById('calcWhatsappLink');

  if (!pillarSelect || !areaInput) return;

  const rates = {
    aluminum: 550,
    alucobond: 450,
    hpl: 480,
    curtain: 950
  };

  const phoneNum = '972525887454';

  function updateCalc() {
    const area = parseFloat(areaInput.value);
    if (areaDisplay) areaDisplay.textContent = `${area} מ״ר`;

    const rate = rates[pillarSelect.value] || 450;
    const subMult = subSelect.value === 'thermal' ? 1.2 : 1.0;

    const total = Math.round(area * rate * subMult);
    if (priceDisplay) priceDisplay.textContent = `₪${total.toLocaleString('he-IL')}`;

    const pillarName = pillarSelect.options[pillarSelect.selectedIndex].text;
    const subName = subSelect.options[subSelect.selectedIndex].text;

    const text = encodeURIComponent(
      `שלום Alu-on group (האב מערכות מתקדמות בע"מ),\n` +
      `ברצוני לקבל הצעת מחיר עבור מעטפת מבנה:\n` +
      `• *סוג חיפוי:* ${pillarName}\n` +
      `• *שטח מוערך:* ${area} מ״ר\n` +
      `• *מפרט תת-קונסטרוקציה:* ${subName}\n` +
      `• *אומדן מחיר משוער:* ₪${total.toLocaleString('he-IL')}\n\n` +
      `אשמח ליצירת קשר לתיאום ייעוץ ומדידה בשטח בכל הארץ.`
    );

    if (whatsappLink) {
      whatsappLink.href = `https://wa.me/${phoneNum}?text=${text}`;
    }
  }

  pillarSelect.addEventListener('change', updateCalc);
  areaInput.addEventListener('input', updateCalc);
  subSelect.addEventListener('change', updateCalc);
  updateCalc();
}

/* ==========================================================================
   2. Contact Form Direct Routing to WhatsApp & Instant Feedback
   ========================================================================== */
function initContactForm() {
  const contactForm = document.getElementById('contactForm');
  const phoneNum = '972525887454';

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('formName').value;
      const phone = document.getElementById('formPhone').value;
      const service = document.getElementById('formService') ? document.getElementById('formService').value : 'כללי';
      const notes = document.getElementById('formNotes') ? document.getElementById('formNotes').value : '';

      const text = encodeURIComponent(
        `פנייה חדשה מאתר Alu-on group:\n` +
        `• *שם:* ${name}\n` +
        `• *טלפון:* ${phone}\n` +
        `• *תחום מבוקש:* ${service}\n` +
        (notes ? `• *הערות:* ${notes}\n` : '')
      );

      window.open(`https://wa.me/${phoneNum}?text=${text}`, '_blank');
      showToast(`תודה ${name}! פנייתך הועברה בהצלחה לצוות האב מערכות מתקדמות בע"מ.`);
      contactForm.reset();
    });
  }
}

/* ==========================================================================
   3. Instant Search Engine Modal & Ctrl+K Shortcut
   ========================================================================== */
function initInstantSearch() {
  const searchTrigger = document.getElementById('searchTriggerBtn');
  const searchModal = document.getElementById('searchModal');
  const searchClose = document.getElementById('searchCloseBtn');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');

  // Search Index Data (Articles, Specs, Claddings, Pages)
  const searchData = [
    { title: "חיפוי אלוקובונד (ACP)", desc: "לוח מרוכב מאלומיניום המאפשר חיפוי חזית חלק, מדויק ומודרני.", url: "index.html#solutions" },
    { title: "חיפוי אלומיניום מלא 2 מ״מ", desc: "חיפוי אלומיניום מלא עמיד בפני קורוזיה ושריפות לבית ולמשרד.", url: "index.html#solutions" },
    { title: "חיפוי HPL יוקרתי", desc: "לוח למינציה בלחץ גבוה עמיד בפני קרינת UV ולחות.", url: "index.html#solutions" },
    { title: "קירות מסך מתקדמים (Curtain Walls)", desc: "מערכות מעטפת שקופות משולבות זכוכית ואלומיניום למבנים גבוהים.", url: "index.html#solutions" },
    { title: "מדריך לחיפוי חזית באלוקובונד", desc: "מאמר מקצועי על טכנולוגיית האלוקובונד ותקני בנייה בישראל.", url: "/articles/" },
    { title: "חיפוי HPL חיצוני בישראל", desc: "מאמר על עמידות HPL בתנאי אקלים ימיים ושמש אינטנסיבית.", url: "/articles/" },
    { title: "מדריך אדריכלי למערכות קיר מסך", desc: "מפרט אדריכלי לקירות מסך ומעטפות זכוכית.", url: "/articles/" },
    { title: "הורדת שרטוטי DWG ו-PDF לאדריכלים", desc: "מרכז ההורדות הטכניות לאדריכלים ומתכננים.", url: "/architects/" },
    { title: "מחשבון עלויות מעטפת בלייב", desc: "חישוב אומדן מחיר לחיפוי לפי מ״ר ושליחה ל-WhatsApp.", url: "index.html#calculator" },
    { title: "פרויקטים נבחרים", desc: "גלריית פרויקטים ומבני ציבור שבוצעו על ידי החברה.", url: "/projects/" },
    { title: "אודות האב מערכות מתקדמות בע\"מ", desc: "תכנון, ייצור ועיבוד CNC במפעלנו באזור תעשייה קריית ים.", url: "/about/" }
  ];

  function openSearch() {
    if (searchModal) {
      searchModal.classList.add('open');
      setTimeout(() => { if (searchInput) searchInput.focus(); }, 100);
    }
  }

  function closeSearch() {
    if (searchModal) searchModal.classList.remove('open');
  }

  if (searchTrigger) searchTrigger.addEventListener('click', openSearch);
  if (searchClose) searchClose.addEventListener('click', closeSearch);
  if (searchModal) {
    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) closeSearch();
    });
  }

  // Ctrl+K or Cmd+K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') closeSearch();
  });

  // Filter Search Results
  if (searchInput && searchResults) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim().toLowerCase();
      if (!query) {
        searchResults.innerHTML = '<p style="color:var(--foreground-muted); text-align:center; padding:1rem;">הקלד חיפוש למשל: אלוקובונד, HPL, DWG, מחשבון...</p>';
        return;
      }

      const filtered = searchData.filter(item => 
        item.title.toLowerCase().includes(query) || item.desc.toLowerCase().includes(query)
      );

      if (filtered.length === 0) {
        searchResults.innerHTML = '<p style="color:var(--foreground-muted); text-align:center; padding:1rem;">לא נמצאו תוצאות. נסה לחפש: אלומיניום, HPL, קירות מסך, 052-588-7454</p>';
      } else {
        searchResults.innerHTML = filtered.map(item => `
          <a href="${item.url}" class="search-result-item" onclick="document.getElementById('searchModal').classList.remove('open')">
            <span class="search-result-title">${item.title}</span>
            <span class="search-result-snippet">${item.desc}</span>
          </a>
        `).join('');
      }
    });
  }
}

function showToast(message) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: #fff;"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/* ==========================================================================
   5. Accessible Floating Widget & Toolbar (WCAG 2.1 AA Compliance)
   ========================================================================== */
function initAccessibilityWidget() {
  if (document.getElementById('aluonA11yBtn') || document.getElementById('a11yBtn')) return;

  // Remove any redundant elements if present
  document.querySelectorAll('.aluon-a11y-btn, .a11y-widget-btn').forEach((btn, idx) => {
    if (idx > 0) btn.remove();
  });

  const btn = document.createElement('button');
  btn.id = 'aluonA11yBtn';
  btn.className = 'aluon-a11y-btn';
  btn.setAttribute('aria-label', 'תפריט נגישות מתקדם');
  btn.setAttribute('title', 'תפריט נגישות');
  btn.innerHTML = `<i class="fa-solid fa-universal-access"></i>`;

  const panel = document.createElement('div');
  panel.id = 'a11yPanel';
  panel.className = 'a11y-widget-panel';
  panel.setAttribute('aria-label', 'אפשרויות נגישות מתקדמות');
  panel.innerHTML = `
    <div class="a11y-panel-header">
      <span><i class="fa-solid fa-universal-access"></i> סרגל נגישות מתקדם</span>
      <button class="a11y-close-btn" id="a11yCloseBtn" aria-label="סגור"><i class="fa-solid fa-xmark"></i></button>
    </div>
    <div class="a11y-grid-options">
      <button class="a11y-option-btn" id="a11yFontInc"><i class="fa-solid fa-text-height"></i> הגדלת טקסט</button>
      <button class="a11y-option-btn" id="a11yFontDec"><i class="fa-solid fa-font"></i> הקטנת טקסט</button>
      <button class="a11y-option-btn" id="a11yReadableFont"><i class="fa-solid fa-glasses"></i> פונט קריא</button>
      <button class="a11y-option-btn" id="a11yContrast"><i class="fa-solid fa-circle-half-stroke"></i> ניגודיות גבוהה</button>
      <button class="a11y-option-btn" id="a11yInvert"><i class="fa-solid fa-circle-nodes"></i> ניגודיות הפוכה</button>
      <button class="a11y-option-btn" id="a11yGrayscale"><i class="fa-solid fa-palette"></i> גווני אפור</button>
      <button class="a11y-option-btn" id="a11yLightBg"><i class="fa-solid fa-sun"></i> רקע בהיר</button>
      <button class="a11y-option-btn" id="a11yLinks"><i class="fa-solid fa-link"></i> הדגשת קישורים</button>
      <button class="a11y-option-btn" id="a11yCursor"><i class="fa-solid fa-arrow-pointer"></i> סמן מוגדל</button>
      <button class="a11y-option-btn" id="a11yStopAnim"><i class="fa-solid fa-hand"></i> עצירת תנועה</button>
    </div>
    <div class="a11y-panel-footer">
      <a href="/accessibility/" class="a11y-option-btn"><i class="fa-solid fa-file-contract"></i> הצהרת נגישות</a>
      <button class="a11y-option-btn a11y-reset-btn" id="a11yReset"><i class="fa-solid fa-rotate-left"></i> איפוס הגדרות</button>
    </div>
  `;

  document.body.appendChild(btn);
  document.body.appendChild(panel);

  btn.addEventListener('click', () => panel.classList.toggle('open'));
  document.getElementById('a11yCloseBtn').addEventListener('click', () => panel.classList.remove('open'));

  function toggleState(btnId, className) {
    const el = document.getElementById(btnId);
    if (!el) return;
    const isActive = document.body.classList.toggle(className);
    if (isActive) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  }

  document.getElementById('a11yFontInc').addEventListener('click', () => {
    document.body.classList.remove('a11y-font-sm');
    toggleState('a11yFontInc', 'a11y-font-lg');
    document.getElementById('a11yFontDec').classList.remove('active');
  });

  document.getElementById('a11yFontDec').addEventListener('click', () => {
    document.body.classList.remove('a11y-font-lg');
    toggleState('a11yFontDec', 'a11y-font-sm');
    document.getElementById('a11yFontInc').classList.remove('active');
  });

  document.getElementById('a11yReadableFont').addEventListener('click', () => toggleState('a11yReadableFont', 'a11y-readable-font'));
  document.getElementById('a11yContrast').addEventListener('click', () => toggleState('a11yContrast', 'a11y-high-contrast'));
  document.getElementById('a11yInvert').addEventListener('click', () => toggleState('a11yInvert', 'a11y-invert-contrast'));
  document.getElementById('a11yGrayscale').addEventListener('click', () => toggleState('a11yGrayscale', 'a11y-grayscale'));
  document.getElementById('a11yLightBg').addEventListener('click', () => toggleState('a11yLightBg', 'a11y-light-bg'));
  document.getElementById('a11yLinks').addEventListener('click', () => toggleState('a11yLinks', 'a11y-highlight-links'));
  document.getElementById('a11yCursor').addEventListener('click', () => toggleState('a11yCursor', 'a11y-big-cursor'));
  document.getElementById('a11yStopAnim').addEventListener('click', () => toggleState('a11yStopAnim', 'a11y-stop-animations'));

  document.getElementById('a11yReset').addEventListener('click', () => {
    document.body.classList.remove(
      'a11y-font-lg', 'a11y-font-sm', 'a11y-readable-font',
      'a11y-high-contrast', 'a11y-invert-contrast', 'a11y-grayscale',
      'a11y-light-bg', 'a11y-highlight-links', 'a11y-big-cursor', 'a11y-stop-animations'
    );
    panel.querySelectorAll('.a11y-option-btn').forEach(b => b.classList.remove('active'));
  });
}

/* ==========================================================================
   6. RTL Privacy & Cookie Consent Component (Israeli Law & GDPR)
   ========================================================================== */
function initPrivacyConsentSystem() {
  const savedConsent = localStorage.getItem('aluon_privacy_consent');

  // Tracking engine controller
  window.aluonTrackingEnabled = savedConsent === 'all' || savedConsent === 'custom_analytics';
  
  if (savedConsent) return; // User already made a choice

  // Build Floating Bottom Privacy Card Markup
  const card = document.createElement('div');
  card.className = 'privacy-consent-card show';
  card.setAttribute('role', 'dialog');
  card.setAttribute('aria-label', 'הודעת פרטיות וקובצי עוגיות');
  card.setAttribute('aria-modal', 'false');

  card.innerHTML = `
    <div class="privacy-card-header">
      <i class="fa-solid fa-shield-halved"></i>
      <span>פרטיות ועוגיות</span>
    </div>
    <div class="privacy-card-body">
      אנו משתמשים בקובצי עוגיות לשיפור הגלישה ולצרכים סטטיסטיים. מידע נוסף ב-<a href="/privacy-policy/"><i class="fa-solid fa-shield-halved"></i> מדיניות הפרטיות</a>.
    </div>
    <div class="privacy-btn-trio">
      <button type="button" class="btn-consent-accept" id="consentAcceptBtn" aria-label="מאשר/ת את כל קובצי העוגיות">מאשר/ת</button>
      <button type="button" class="btn-consent-decline" id="consentDeclineBtn" aria-label="דוחה קובצי עוגיות שאינם חיוניים">דוחה</button>
      <button type="button" class="btn-consent-prefs" id="consentPrefsBtn" aria-label="העדפות פרטיות ועוגיות">העדפות</button>
    </div>
  `;

  // Build Preferences Modal Markup
  const modalOverlay = document.createElement('div');
  modalOverlay.className = 'privacy-prefs-overlay';
  modalOverlay.setAttribute('role', 'dialog');
  modalOverlay.setAttribute('aria-label', 'הגדרות העדפות פרטיות');
  modalOverlay.setAttribute('aria-modal', 'true');

  modalOverlay.innerHTML = `
    <div class="privacy-prefs-modal">
      <div class="prefs-header">
        <h3><i class="fa-solid fa-sliders" style="color:#0055ff;"></i> הגדרות העדפות פרטיות</h3>
        <button type="button" class="prefs-close-btn" id="prefsCloseBtn" aria-label="סגור חלון העדפות">✕</button>
      </div>
      <div class="prefs-list">
        <div class="pref-item">
          <div class="pref-info">
            <h4>קובצי חובה (חיוניים)</h4>
            <p>הכרחיים לתפעול תקין של האתר, אבטחה ונגישות.</p>
          </div>
          <div class="pref-toggle">
            <input type="checkbox" checked disabled id="prefNecessary" aria-label="עוגיות חיוניות">
          </div>
        </div>
        <div class="pref-item">
          <div class="pref-info">
            <h4>ניטור וסטטיסטיקה</h4>
            <p>מסייעים לנו להבין כיצד גולשים משתמשים באתר לצורך שיפור ביצועים.</p>
          </div>
          <div class="pref-toggle">
            <input type="checkbox" id="prefAnalytics" aria-label="עוגיות ניטור וסטטיסטיקה">
          </div>
        </div>
        <div class="pref-item">
          <div class="pref-info">
            <h4>שיווק והתאמה אישית</h4>
            <p>משמשים להצגת תוכן מותאם אישית והצעות רלוונטיות.</p>
          </div>
          <div class="pref-toggle">
            <input type="checkbox" id="prefMarketing" aria-label="עוגיות שיווק">
          </div>
        </div>
      </div>
      <button type="button" class="btn-pill btn-white" id="savePrefsBtn" style="width:100%; font-weight:700; margin-top:0.5rem;">
        שמירת העדפות <i class="fa-solid fa-check"></i>
      </button>
    </div>
  `;

  document.body.appendChild(card);
  document.body.appendChild(modalOverlay);

  // Handlers
  const closeAll = (consentType) => {
    localStorage.setItem('aluon_privacy_consent', consentType);
    window.aluonTrackingEnabled = (consentType === 'all' || consentType === 'custom_analytics');
    card.classList.remove('show');
    modalOverlay.classList.remove('open');
    setTimeout(() => {
      card.remove();
      modalOverlay.remove();
    }, 300);
  };

  document.getElementById('consentAcceptBtn').addEventListener('click', () => closeAll('all'));
  document.getElementById('consentDeclineBtn').addEventListener('click', () => closeAll('necessary_only'));
  
  document.getElementById('consentPrefsBtn').addEventListener('click', () => {
    modalOverlay.classList.add('open');
  });

  document.getElementById('prefsCloseBtn').addEventListener('click', () => {
    modalOverlay.classList.remove('open');
  });

  document.getElementById('savePrefsBtn').addEventListener('click', () => {
    const isAnalytics = document.getElementById('prefAnalytics').checked;
    closeAll(isAnalytics ? 'custom_analytics' : 'necessary_only');
  });
}
