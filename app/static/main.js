document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('question-form');
    const questionInput = document.getElementById('question-input');
    const errorMessage = document.getElementById('error-message');
    const answerContainer = document.getElementById('answer-container');
    const askButton = document.getElementById('ask-button');
    const clearButton = document.getElementById('clear-button');
    const placeholderText = document.querySelector('.placeholder-text');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const userQuestion = questionInput.value.trim();
        if (userQuestion === '') {
            errorMessage.textContent = 'Please enter a question.';
            errorMessage.style.display = 'block';
            return;
        } else {
            errorMessage.style.display = 'none';
        }

        // Disable the submit button and show loading spinner
        askButton.disabled = true;
        askButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';

        // Hide placeholder text
        if (placeholderText) {
            placeholderText.style.display = 'none';
        }

        // Send POST request to /ask-question endpoint
        fetch('/ask-question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_question: userQuestion })
        })
            .then(response => response.json())
            .then(data => {
                if (data && data.answer) {
                    displayResponse(data);
                } else {
                    errorMessage.textContent = 'Unexpected response from the server.';
                    errorMessage.style.display = 'block';
                }
                // Re-enable the submit button
                askButton.disabled = false;
                askButton.innerHTML = '<i class="fas fa-paper-plane"></i> Ask';
            })
            .catch(error => {
                console.error('Error:', error);
                errorMessage.textContent = 'An error occurred while fetching the answer.';
                errorMessage.style.display = 'block';
                askButton.disabled = false;
                askButton.innerHTML = '<i class="fas fa-paper-plane"></i> Ask';
                // Restore placeholder if it's not already hidden
                if (!placeholderText) {
                    const newPlaceholder = document.createElement('p');
                    newPlaceholder.classList.add('placeholder-text');
                    newPlaceholder.textContent = 'Your answer will appear here after you submit a question.';
                    answerContainer.appendChild(newPlaceholder);
                }
            });
    });

    clearButton.addEventListener('click', function () {
        questionInput.value = '';
        answerContainer.innerHTML = '<p class="placeholder-text">Your answer will appear here after you submit a question.</p>';
        errorMessage.style.display = 'none';
        questionInput.focus();
    });

    function displayResponse(data) {
        // Clear previous content
        answerContainer.innerHTML = '';

        // Reset opacity for animation
        answerContainer.style.opacity = '0';

        // Create elements to display the response
        const sourceElement = document.createElement('p');
        sourceElement.innerHTML = `<i class="fas fa-database"></i> <strong>Source:</strong> ${data.source}`;

        const matchedQuestionElement = document.createElement('p');
        matchedQuestionElement.innerHTML = `<i class="fas fa-question-circle"></i> <strong>Matched Question:</strong> ${data.matched_question}`;

        const answerElement = document.createElement('p');
        answerElement.innerHTML = `<i class="fas fa-comment-dots"></i> <strong>Answer:</strong> ${data.answer}`;

        // Append elements to the container
        answerContainer.appendChild(sourceElement);
        answerContainer.appendChild(matchedQuestionElement);
        answerContainer.appendChild(answerElement);

        // Trigger reflow for animation
        void answerContainer.offsetWidth;

        // Add fade-in effect
        answerContainer.style.opacity = '1';
    }
});
