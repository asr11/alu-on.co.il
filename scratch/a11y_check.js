const fs = require('fs');
const path = require('path');

const rootDir = '/home/asr11/ASHER/לקוחות חדשים אפיון צרכים ואפשרויות/alu-on.co.il';

function walk(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        if (dirPath.includes('/staging/') || dirPath.includes('/snapshot-')) return;
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walk(dirPath, callback) : callback(path.join(dir, f));
    });
}

const htmlFiles = [];
const cssFiles = [];

walk(rootDir, (filePath) => {
    if (filePath.endsWith('.html')) htmlFiles.push(filePath);
    if (filePath.endsWith('.css')) cssFiles.push(filePath);
});

console.log(`Found ${htmlFiles.length} HTML files and ${cssFiles.length} CSS files.`);

let imgNoAlt = 0;
let buttonNoAria = 0;
let linkNoAria = 0;
let focusOutlineMissing = 0;

htmlFiles.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let hasChanges = false;

    // Fix img missing alt
    const imgRegex = /<img(?![^>]*\balt=)[^>]*>/gi;
    let match;
    while ((match = imgRegex.exec(content)) !== null) {
        console.log(`Missing alt in ${file}:`, match[0]);
        imgNoAlt++;
    }
    
    // Fix button missing text/aria
    // Check buttons that might just have icons
    const btnRegex = /<button[^>]*>([\s\S]*?)<\/button>/gi;
    while ((match = btnRegex.exec(content)) !== null) {
        let btnContent = match[1].trim();
        let btnTag = match[0];
        if (!btnTag.includes('aria-label') && !btnTag.includes('aria-labelledby') && btnContent.replace(/<[^>]*>/g, '').trim() === '') {
            console.log(`Button missing text/aria in ${file}:`, match[0]);
            buttonNoAria++;
        }
    }

    // Fix link missing text/aria
    const linkRegex = /<a\s[^>]*>([\s\S]*?)<\/a>/gi;
    while ((match = linkRegex.exec(content)) !== null) {
        let linkContent = match[1].trim();
        let linkTag = match[0];
        if (!linkTag.includes('aria-label') && !linkTag.includes('aria-labelledby') && linkContent.replace(/<[^>]*>/g, '').trim() === '') {
            console.log(`Link missing text/aria in ${file}:`, match[0]);
            linkNoAria++;
        }
    }
});

cssFiles.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    if (content.includes('outline: none') && !content.includes(':focus-visible')) {
        console.log(`Potential focus outline issue in ${file}`);
        focusOutlineMissing++;
    }
});
