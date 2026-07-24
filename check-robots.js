#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Pages that should NOT be indexed
// NOTE: client.html (Member Portal) is intentionally left OUT of this list.
// It is a public sign-in/sign-up page we want indexed (index,follow) so members
// can find it via search. Only truly private pages (e.g. admin) belong here.
const NOINDEX_PAGES = ['admin.html'];

// Get all HTML files in current directory and subdirectories
function getHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      // Skip node_modules and hidden folders
      if (file === 'node_modules' || file.startsWith('.')) continue;
      getHtmlFiles(fullPath, fileList);
    } else if (file.endsWith('.html')) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

const htmlFiles = getHtmlFiles('.');

console.log(`\n🔍 Checking ${htmlFiles.length} HTML files for robots meta tag...\n`);

let issues = 0;

for (const file of htmlFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const filename = path.basename(file);
  const relativePath = file.replace('./', '');

  const robotsMatch = content.match(/<meta\s+name=["']robots["']\s+content=["']([^"']+)["']/i)
    || content.match(/<meta\s+content=["']([^"']+)["']\s+name=["']robots["']/i);

  const shouldNoIndex = NOINDEX_PAGES.includes(filename);

  if (!robotsMatch) {
    if (shouldNoIndex) {
      console.log(`⚠️  MISSING (should be noindex): ${relativePath}`);
      console.log(`   👉 Add: <meta name="robots" content="noindex,nofollow" />\n`);
    } else {
      console.log(`❌ MISSING robots tag: ${relativePath}`);
      console.log(`   👉 Add: <meta name="robots" content="index,follow" />\n`);
    }
    issues++;
  } else {
    const value = robotsMatch[1];
    if (shouldNoIndex && !value.includes('noindex')) {
      console.log(`🚨 WRONG VALUE for protected page: ${relativePath}`);
      console.log(`   Found: "${value}" — should be "noindex,nofollow"\n`);
      issues++;
    } else if (!shouldNoIndex && value.includes('noindex')) {
      console.log(`🚨 ACCIDENTALLY NOINDEX: ${relativePath}`);
      console.log(`   Found: "${value}" — change to "index,follow"\n`);
      issues++;
    } else {
      console.log(`✅ OK: ${relativePath} → "${value}"`);
    }
  }
}

console.log('\n' + '─'.repeat(50));
if (issues === 0) {
  console.log('✅ All files look good! No issues found.');
} else {
  console.log(`⚠️  ${issues} issue(s) found. Fix them and re-run this script.`);
}
console.log('─'.repeat(50) + '\n');