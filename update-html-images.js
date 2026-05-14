const fs = require("fs");
const path = require("path");

const rootFolder = "./";

// Convert old image paths to new compressed structure
function updateHtmlFile(filePath) {
  let html = fs.readFileSync(filePath, "utf8");

  // 1. Fix folder path
  html = html.replaceAll("./images/", "./compressed/");

  // 2. Fix common JPG/PNG extensions → JPG (since your compressor outputs .jpg)
  html = html.replaceAll(".png", ".jpg");
  html = html.replaceAll(".jpeg", ".jpg");

  // 3. Fix spaces in filenames → dashes (IMPORTANT)
  html = html.replace(/src="([^"]*)"/g, (match, p1) => {
    let fixed = p1
      .replace(/\s+/g, "-")
      .replace(/[^a-zA-Z0-9\-./]/g, "")
      .toLowerCase();

    return `src="${fixed}"`;
  });

  fs.writeFileSync(filePath, html, "utf8");
  console.log(`Updated: ${filePath}`);
}

// Walk through folders and find HTML files
function walk(dir) {
  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);

    if (fullPath.includes("node_modules")) return;

    if (fs.statSync(fullPath).isDirectory()) {
      walk(fullPath);
    } else if (file.endsWith(".html")) {
      updateHtmlFile(fullPath);
    }
  });
}

walk(rootFolder);

console.log("DONE: All HTML files updated.");