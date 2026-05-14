const fs = require("fs");
const path = require("path");

const folder = "./"; // root of project

function updateFile(filePath) {
  let html = fs.readFileSync(filePath, "utf8");

  // replace image folder path
  const updated = html.replaceAll("./images/", "./compressed/");

  if (html !== updated) {
    fs.writeFileSync(filePath, updated, "utf8");
    console.log(`Updated: ${filePath}`);
  }
}

function walk(dir) {
  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);

    // ignore node_modules
    if (fullPath.includes("node_modules")) return;

    if (fs.statSync(fullPath).isDirectory()) {
      walk(fullPath);
    } else if (fullPath.endsWith(".html")) {
      updateFile(fullPath);
    }
  });
}

walk(folder);

console.log("Done updating all HTML files.");