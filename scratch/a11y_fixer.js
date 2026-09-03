const fs = require('fs');
const path = require('path');

const rootDir = '/home/asr11/ASHER/לקוחות חדשים אפיון צרכים ואפשרויות/alu-on.co.il';
const modifiedFiles = [];

function walk(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        if (dirPath.includes('/staging/') || dirPath.includes('/snapshot-')) return;
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walk(dirPath, callback) : callback(path.join(dir, f));
    });
}

walk(rootDir, (filePath) => {
    if (filePath.endsWith('.html')) {
        let originalContent = fs.readFileSync(filePath, 'utf8');
        let content = originalContent;

        // Add aria-label to links with title but no text/aria-label
        content = content.replace(/<a([^>]*?)title="([^"]*)"([^>]*)>(\s*<i[^>]*><\/i>\s*)<\/a>/gi, (match, p1, p2, p3, p4) => {
            if (match.includes('aria-label')) return match;
            return `<a${p1}title="${p2}" aria-label="${p2}"${p3}>${p4}</a>`;
        });

        // Some links might have class="social-icon-btn" but no title? The previous script showed they all had titles.

        // Also fix any headings hierarchy if obvious? (Skipping for now unless requested, hard to automate blindly without breaking styles).

        if (content !== originalContent) {
            fs.writeFileSync(filePath, content, 'utf8');
            modifiedFiles.push({ file: filePath, fix: 'Added aria-label to icon-only links' });
        }
    }

    if (filePath.endsWith('.css')) {
        let originalContent = fs.readFileSync(filePath, 'utf8');
        let content = originalContent;
        let changed = false;

        if (content.includes('outline: none') || content.includes('outline: 0')) {
            // Check if focus-visible is already defined
            if (!content.includes(':focus-visible')) {
                // Add a global focus-visible rule at the end of the file
                content += `\n\n/* A11y Focus Outline Fix */\n*:focus-visible {\n    outline: 2px solid #0056b3 !important;\n    outline-offset: 2px !important;\n}\n`;
                changed = true;
            }
        }

        if (changed) {
            fs.writeFileSync(filePath, content, 'utf8');
            modifiedFiles.push({ file: filePath, fix: 'Added :focus-visible outline for keyboard navigation' });
        }
    }
});

fs.writeFileSync('scratch/a11y_fixes.json', JSON.stringify(modifiedFiles, null, 2));
console.log('Done fixing! Check scratch/a11y_fixes.json for details.');
