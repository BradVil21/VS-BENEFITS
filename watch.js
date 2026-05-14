const chokidar = require('chokidar');
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const inputFolder = './images';
const outputFolder = './compressed';

if (!fs.existsSync(outputFolder)) {
  fs.mkdirSync(outputFolder);
}

chokidar.watch(inputFolder).on('add', (filePath) => {
  const fileName = path.parse(filePath).name;

  sharp(filePath)
    .resize({ width: 1400 })
    .webp({ quality: 70 })
    .toFile(`${outputFolder}/${fileName}.webp`)
    .then(() => {
      console.log(`Compressed: ${fileName}`);
    });
});