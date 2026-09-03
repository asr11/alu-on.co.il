const { chromium } = require('playwright');

(async () => {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  let workerResponded = false;
  let workerStatus = 0;

  // Listen for the POST request to the worker
  page.on('response', response => {
    const url = response.url();
    if (url.includes('hub-lead-worker') && response.request().method() === 'POST') {
      workerResponded = true;
      workerStatus = response.status();
      console.log(`Worker responded with status: ${workerStatus}`);
    }
  });

  // Intercept window.open for WhatsApp
  let waOpened = false;
  await page.exposeFunction('interceptWA', (url) => {
    if (url.includes('wa.me')) {
      waOpened = true;
      console.log('WhatsApp window opened:', url);
    }
  });

  await page.addInitScript(() => {
    const originalOpen = window.open;
    window.open = function(url, target, features) {
      if (url.includes('wa.me')) {
        window.interceptWA(url);
        return null;
      }
      return originalOpen.apply(this, arguments);
    };
  });

  console.log('Navigating to alu-on.co.il/contact/ ...');
  await page.goto('https://alu-on.co.il/contact/', { waitUntil: 'networkidle' });

  // Fill the form
  await page.fill('#formName', 'TEST Prod');
  await page.fill('#formPhone', '0509997753');

  // Accept privacy if exists
  const privacyCheck = await page.$('#privacyConsent');
  if (privacyCheck) {
    await privacyCheck.check();
  }

  console.log('Submitting form...');
  await page.click('button[type="submit"]');

  // Wait a bit for requests and WA to trigger
  await page.waitForTimeout(4000);

  console.log('Results:');
  console.log('- WhatsApp Opened:', waOpened);
  console.log('- Worker Hit:', workerResponded);
  console.log('- Worker Status:', workerStatus);

  await browser.close();
})();
