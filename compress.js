const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputFolder = './images';
const outputFolder = './compressed';

if (!fs.existsSync(outputFolder)) {
  fs.mkdirSync(outputFolder);
}

const allowedExtensions = ['.jpg', '.jpeg', '.png'];

fs.readdirSync(inputFolder).forEach(file => {
  const ext = path.extname(file).toLowerCase();

  if (!allowedExtensions.includes(ext)) {
    console.log(`Skipping: ${file}`);
    return;
  }

  const inputPath = path.join(inputFolder, file);
  const fileName = path.parse(file).name;

  // 🔥 FIX: normalize filenames (spaces → dashes, lowercase)
  const safeName = fileName
    .replace(/\s+/g, '-')   // replace spaces with dashes
    .replace(/[^a-zA-Z0-9\-]/g, '') // remove weird characters
    .toLowerCase();

  sharp(inputPath)
    .resize({
      width: 1400,
      withoutEnlargement: true
    })
    .jpeg({
      quality: 80,
      mozjpeg: true
    })
    .toFile(
      path.join(outputFolder, `${safeName}.jpg`)
    )
    .then(() => {
      console.log(`Compressed: ${file} → ${safeName}.jpg`);
    })
    .catch(err => {
      console.error(`Error processing ${file}:`, err);
    });
});