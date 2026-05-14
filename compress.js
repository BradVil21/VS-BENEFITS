const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const inputFolder = "./images";
const outputFolder = "./compressed";

if (!fs.existsSync(outputFolder)) {
  fs.mkdirSync(outputFolder);
}

const allowedExtensions = [".jpg", ".jpeg", ".png"];

fs.readdirSync(inputFolder).forEach(file => {
  const ext = path.extname(file).toLowerCase();
  if (!allowedExtensions.includes(ext)) return;

  const inputPath = path.join(inputFolder, file);

  const baseName = path.parse(file).name;

  const safeName = baseName
    .replace(/\s+/g, "-")
    .replace(/[^a-zA-Z0-9\-]/g, "")
    .toLowerCase();

  const isPNG = ext === ".png";

  const outputFile = isPNG
    ? `${safeName}.png`
    : `${safeName}.jpg`;

  const outputPath = path.join(outputFolder, outputFile);

  let pipeline = sharp(inputPath)
    .resize({
      width: 1200,
      withoutEnlargement: true
    });

  if (isPNG) {
    pipeline = pipeline.png({ compressionLevel: 8 });
  } else {
    pipeline = pipeline.jpeg({
      quality: 80,
      mozjpeg: true
    });
  }

  pipeline
    .toFile(outputPath)
    .then(() => {
      console.log(`Compressed: ${file} → ${outputFile}`);
    })
    .catch(err => console.error(err));
});