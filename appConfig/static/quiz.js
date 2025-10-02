const questions =  document.querySelectorAll(".question-block");
const nextButton = document.getElementById("nextButton");
const submitButton = document.getElementById("submitButton");
let currentQuestionIndex = 0;

function showQuestion(index)
{
    questions.forEach((q, i) => {
        q.classList.toggle("hidden", i !== index);
    });
}

nextButton.addEventListener("click", () => {
    const currentQuestion = questions[currentQuestionIndex];
    const selectedOption = currentQuestion.querySelector('input[type="radio"]:checked');

    if (!selectedOption)
    {
        alert("Please select an option before proceeeding.");
        return;
    }
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++; 
        showQuestion(currentQuestionIndex);

        if (currentQuestionIndex === questions.length - 1) {
            nextButton.classList.add("hidden");
            submitButton.classList.remove("hidden");
        }
    }
});

showQuestion(currentQuestionIndex);