// save as save.js
const fs = require("fs");
const path = require("path");

const subject = process.argv[2];

if (!subject) {
  console.error("Provide subject name");
  process.exit(1);
}

// read stdin (paste content)
let data = "";

process.stdin.on("data", chunk => {
  data += chunk;
});

process.stdin.on("end", () => {
  const dir = `/home/ap/Personal_Files/coding/upsc_question_bank/question_bank/${subject}/input`;

  fs.mkdirSync(dir, { recursive: true });

  const filePath = path.join(dir, "questions.md");

  fs.writeFileSync(filePath, data);

  console.log("Saved to:", filePath);
});