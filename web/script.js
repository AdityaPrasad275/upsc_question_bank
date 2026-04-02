document.addEventListener('DOMContentLoaded', function() {
    const questionList = document.getElementById('question-list');
    const questionDetails = document.getElementById('question-details');
    const questions = [];

    // Load all questions (assuming 47 questions)
    for (let i = 1; i <= 47; i++) {
        fetch(`data/question_${i}.json`)
            .then(response => response.json())
            .then(data => {
                questions.push({ id: i, data: data });
                addToSidebar(i, data);
            })
            .catch(error => console.error(`Error loading question ${i}:`, error));
    }

    function addToSidebar(id, data) {
        const li = document.createElement('li');
        li.textContent = `${id}. ${data.question_short_text}`;
        li.addEventListener('click', () => displayQuestion(data));
        questionList.appendChild(li);
    }

    function displayQuestion(data) {
        const optionsHtml = data.options.map((option, index) => 
            `<div class="option">${String.fromCharCode(97 + index)}) ${option}</div>`
        ).join('');

        const factsHtml = data.research.facts.map(fact => `<li>${fact}</li>`).join('');

        const sourcesHtml = data.research.sources.map(source => 
            `<li class="source"><strong>${source.title}</strong><br><a href="${source.url}" target="_blank">${source.url}</a><br><em>${source.whyUsed}</em></li>`
        ).join('');

        questionDetails.innerHTML = `
            <div class="question-title">${data.question_short_text}</div>
            <div class="question-text">${data.text.replace(/\n/g, '<br>')}</div>
            <div class="options">${optionsHtml}</div>
            <div class="answer"><strong>Answer:</strong> ${data.answerText}</div>
            <div class="explanation"><strong>Explanation:</strong> ${data.explanation}</div>
            <div class="research">
                <strong>Research Summary:</strong> ${data.research.summary}
                <div><strong>Key Facts:</strong><ul>${factsHtml}</ul></div>
                <div><strong>Sources:</strong><ul>${sourcesHtml}</ul></div>
                <div><strong>Search Meta:</strong> Used Web Search: ${data.research.searchMeta.usedWebSearch}, Confidence: ${data.research.searchMeta.confidence}</div>
            </div>
        `;
    }
});