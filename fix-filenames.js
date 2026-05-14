const fs = require("fs");
const path = require("path");

const DIR = "./images";

fs.readdirSync(DIR).forEach(file => {
  const oldPath = path.join(DIR, file);

  const newName = file
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9.\-]/g, "");

  const newPath = path.join(DIR, newName);

  if (oldPath !== newPath) {
    fs.renameSync(oldPath, newPath);
    console.log(`Renamed: ${file} → ${newName}`);
  }
});

console.log("DONE fixing filenames");