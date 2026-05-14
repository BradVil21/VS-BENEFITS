const fs = require('fs');

const file = './index.html';

let html = fs.readFileSync(file, 'utf8');

// replace folder path
html = html.replaceAll('./images/', './compressed/');

fs.writeFileSync(file, html);

console.log('Updated image paths');