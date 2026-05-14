const fs = require("fs");
const path = require("path");

const ROOT = __dirname;

function getHtmlFiles(dir, files = []) {
  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);

    if (fs.statSync(fullPath).isDirectory()) {
      return getHtmlFiles(fullPath, files);
    }

    if (file.endsWith(".html")) {
      files.push(fullPath);
    }
  });

  return files;
}

function fix(html) {
  return html.replace(/(src|href)=["']([^"']+\.(jpg|jpeg|png))["']/gi,
    (match, attr, url) => {

      let file = path.parse(url).name
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^a-z0-9\-]/g, "");

      // keep original extension type preference
      let ext = url.toLowerCase().includes(".png") ? ".png" : ".jpg";

      return `${attr}="/compressed/${file}${ext}"`;
    });
}

const htmlFiles = getHtmlFiles(ROOT);

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, "utf8");
  const updated = fix(content);

  if (content !== updated) {
    fs.writeFileSync(file, updated);
    console.log("Fixed:", file);
  }
});

console.log("DONE updating HTML files");