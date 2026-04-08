(function () {
  // open all details
  document.querySelectorAll("details").forEach(d => d.open = true);

  function htmlToMarkdown(html) {
    let text = html;

    text = text
      .replace(/&nbsp;/g, ' ')
      .replace(/\u00A0/g, ' ')
      .replace(/<strong>(.*?)<\/strong>/gi, '**$1**')
      .replace(/<b>(.*?)<\/b>/gi, '**$1**')
      .replace(/<em>(.*?)<\/em>/gi, '*$1*')
      .replace(/<li>(.*?)<\/li>/gi, '- $1\n')

      // table support
      .replace(/<tr>/gi, '\n| ')
      .replace(/<\/tr>/gi, ' |')
      .replace(/<td>(.*?)<\/td>/gi, '$1 |')
      .replace(/<th>(.*?)<\/th>/gi, '**$1** |')

      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/p>/gi, '\n\n')
      .replace(/<[^>]+>/g, '')

      .replace(/[ \t]+/g, ' ')
      .replace(/\n\s+\n/g, '\n\n')
      .replace(/([a-d]\))/gi, '\n$1')

      .trim();

    return text;
  }

  function cleanDetails(details) {
    let clone = details.cloneNode(true);

    let summary = clone.querySelector("summary");
    if (summary) summary.remove();

    clone.querySelectorAll("button, script, style").forEach(el => el.remove());

    return htmlToMarkdown(clone.innerHTML);
  }

  let output = [];
  let questions = document.querySelectorAll("p");

  let visited = new Set();
  let qNum = 1;

  questions.forEach(p => {
    if (visited.has(p)) return;

    let node = p;
    let questionParts = [];

    // collect everything until first <details>
    while (node && node.tagName.toLowerCase() !== "details") {
      if (["p", "figure", "table"].includes(node.tagName.toLowerCase())) {
        questionParts.push(node.outerHTML);
        visited.add(node);
      }
      node = node.nextElementSibling;
    }

    if (!node) return;

    // collect answer + explanation
    let details = [];
    let temp = node;

    while (temp && details.length < 2) {
      if (temp.tagName.toLowerCase() === "details") {
        details.push(temp);
      }
      temp = temp.nextElementSibling;
    }

    if (details.length < 2) return;

    let question = htmlToMarkdown(questionParts.join("\n"));
    let answer = cleanDetails(details[0]);
    let explanation = cleanDetails(details[1]);

    output.push(
`### Question ${qNum++}
${question}

**Answer:**
${answer}

**Explanation:**
${explanation}

---`
    );
  });

  console.log("Extracted:", output.length, "questions");

  if (output.length === 0) {
    console.log("Nothing extracted. Your DOM structure is probably different. Inspect it.");
    return;
  }

  // download
  let blob = new Blob([output.join("\n\n")], { type: "text/markdown" });
  let a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "questions.md";
  a.click();
})();