document.addEventListener('DOMContentLoaded', function() {
    const interactionPanel = document.getElementById('interaction-panel');
    if (!interactionPanel) return;

    const agentType = interactionPanel.dataset.agentType;
    const form = document.getElementById('agent-form');
    const input = document.getElementById('agent-input');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userInput = input.value.trim();
        if (!userInput) return;

        const endpointMap = {
            explainer: { func: handleExplain, loader: 'The Explainer is consulting the archives...' },
            summarizer: { func: handleSummarize, loader: 'The Summarizer is distilling the essence...' },
            quizmaster: { func: handleQuiz, loader: 'The Quizmaster is forging your challenge...' }
        };

        const handler = endpointMap[agentType];
        if (handler) {
            handler.func(userInput, handler.loader);
        }
        
        input.value = '';
    });

    const createLoader = (message) => `<div class="message loader-message"><span class="sender">Oracle</span>${message}</div>`;

    async function handleExplain(question, loaderMessage) {
        const chatBox = document.getElementById('chat-box');
        addMessageToChat('You', question);
        addMessageToChat('Explainer', createLoader(loaderMessage), true);

        try {
            const response = await fetch('/api/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });
            const data = await response.json();
            
            let agentMessage = data.explanation || data.error || "My apologies, the connection to the archives is unclear.";
            if (data.sources && data.sources.length > 0) {
                agentMessage += `<br><br><small>Sources Consulted: ${data.sources.join(', ')}</small>`;
            }
            updateLastMessage('Explainer', agentMessage);
        } catch (error) {
            updateLastMessage('Explainer', 'A connection error has occurred. The ether is disturbed.');
        }
    }

    async function handleSummarize(topic, loaderMessage) {
        const summaryOutput = document.getElementById('summary-output');
        summaryOutput.innerHTML = createLoader(loaderMessage);
        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic })
            });
            const data = await response.json();
            
            if (data.summary && typeof data.summary === 'object') {
                const summary = data.summary;
                const formattedSummary = `
                    <h3>Overview</h3>
                    <p>${summary.overview || 'Not Available.'}</p>
                    <h3>Key Points</h3>
                    <ul>
                        ${(summary.key_points || []).map(point => `<li>${point}</li>`).join('')}
                    </ul>
                    <h3>Conclusion</h3>
                    <p>${summary.conclusion || 'Not Available.'}</p>
                `;
                summaryOutput.innerHTML = formattedSummary;
            } else {
                summaryOutput.innerText = data.summary || data.error || 'Failed to retrieve a summary.';
            }
        } catch (error) {
             summaryOutput.innerText = 'A connection error has occurred. The ether is disturbed.';
        }
    }

    async function handleQuiz(topic, loaderMessage) {
        const quizOutput = document.getElementById('quiz-output');
        quizOutput.innerHTML = createLoader(loaderMessage);
        try {
            const response = await fetch('/api/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic })
            });
            const data = await response.json();
            renderQuiz(data.quiz || []);
        } catch (error) {
            quizOutput.innerText = 'A connection error has occurred. The ether is disturbed.';
        }
    }

    function addMessageToChat(sender, message, isLoader = false) {
        const chatBox = document.getElementById('chat-box');
        if (!chatBox) return;
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (sender.toLowerCase() === 'you') {
            messageElement.classList.add('user');
        }
        if (isLoader) {
            messageElement.classList.add('loader-message');
        }

        messageElement.innerHTML = `<span class="sender">${sender}</span> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    function updateLastMessage(sender, message) {
        const chatBox = document.getElementById('chat-box');
        const loaderMessage = chatBox.querySelector('.loader-message');
        if (loaderMessage) {
            loaderMessage.innerHTML = `<span class="sender">${sender}</span> ${message}`;
            loaderMessage.classList.remove('loader-message');
        }
    }

    function renderQuiz(quizData) {
        const quizOutput = document.getElementById('quiz-output');
        if (!quizOutput) return;
        quizOutput.innerHTML = '';
        if (quizData.length === 0) {
            quizOutput.innerText = 'The Quizmaster could not forge a challenge for this topic.';
            return;
        }
        quizData.forEach((q, index) => {
            const qContainer = document.createElement('div');
            qContainer.className = 'quiz-question';
            let optionsHTML = '';
            for (const [key, value] of Object.entries(q.options || {})) {
                optionsHTML += `<label><input type="radio" name="q${index}" value="${key}"> ${key}: ${value}</label><br>`;
            }
            qContainer.innerHTML = `
                <p><strong>Q${index+1}: ${q.question}</strong></p>
                <div class="options">${optionsHTML}</div>
                <button class="reveal-btn" data-answer="${q.correct_answer}">Reveal Answer</button>
                <p class="answer" style="display:none;"></p>
            `;
            quizOutput.appendChild(qContainer);
        });

        document.querySelectorAll('.reveal-btn').forEach(button => {
            button.addEventListener('click', function() {
                const answerEl = this.nextElementSibling;
                const correctAnswer = (this.getAttribute('data-answer') || '').trim().toUpperCase();
                answerEl.innerHTML = `The correct answer is ${correctAnswer}.`;
                answerEl.style.display = 'block';
            });
        });
    }
});
