document.addEventListener("DOMContentLoaded", () => {
  // ----------------- Source Type Tab Switching -----------------
  const segmentBtns = document.querySelectorAll(".segment-btn");
  const sourceSections = {
    paste: document.getElementById("section-paste"),
    youtube: document.getElementById("section-youtube"),
    file: document.getElementById("section-file")
  };
  const sourceTypeInput = document.getElementById("source_type_input");

  if (segmentBtns.length > 0 && sourceTypeInput) {
    segmentBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const targetType = btn.getAttribute("data-type");
        
        segmentBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        sourceTypeInput.value = targetType;

        Object.keys(sourceSections).forEach(type => {
          if (sourceSections[type]) {
            sourceSections[type].style.display = (type === targetType) ? "block" : "none";
          }
        });
      });
    });
  }

  // ----------------- Interactive Quiz Submission -----------------
  const quizForm = document.getElementById("quiz-form");
  const submitBtn = document.getElementById("submit-answer-btn");
  const nextBtn = document.getElementById("next-question-btn");
  const feedbackBox = document.getElementById("feedback-box");
  const feedbackTitle = document.getElementById("feedback-title");
  const feedbackText = document.getElementById("feedback-text");
  const feedbackRationale = document.getElementById("feedback-rationale");

  // Radio button styling highlight
  const optionLabels = document.querySelectorAll(".mcq-option");
  optionLabels.forEach(label => {
    const radio = label.querySelector("input[type='radio']");
    if (radio) {
      radio.addEventListener("change", () => {
        optionLabels.forEach(l => l.classList.remove("selected"));
        if (radio.checked) {
          label.classList.add("selected");
        }
      });
    }
  });

  if (quizForm && submitBtn) {
    quizForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const attemptUuid = quizForm.getAttribute("data-attempt-uuid");
      const questionId = quizForm.getAttribute("data-question-id");
      const questionType = quizForm.getAttribute("data-question-type");

      let studentAnswer = "";

      if (questionType === "mcq") {
        const selectedRadio = quizForm.querySelector("input[name='mcq_option']:checked");
        if (!selectedRadio) {
          alert("Please select one of the options before submitting.");
          return;
        }
        studentAnswer = selectedRadio.value;
      } else {
        const textarea = document.getElementById("short-answer-input");
        if (!textarea || !textarea.value.trim()) {
          alert("Please write your answer before submitting.");
          return;
        }
        studentAnswer = textarea.value.trim();
      }

      // Disable inputs and show loading
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="loading-spinner"></span> Evaluating...';

      try {
        const response = await fetch(`/api/quiz/${attemptUuid}/submit`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question_id: questionId,
            student_answer: studentAnswer
          })
        });

        const data = await response.json();

        if (!data.success) {
          alert(data.error || "Failed to evaluate answer.");
          submitBtn.disabled = false;
          submitBtn.innerHTML = "Submit Answer";
          return;
        }

        // Lock form inputs
        quizForm.querySelectorAll("input, textarea").forEach(el => el.disabled = true);
        submitBtn.style.display = "none";

        // Highlight MCQ choices
        if (questionType === "mcq") {
          optionLabels.forEach(label => {
            const radio = label.querySelector("input[type='radio']");
            if (radio.value.trim().toLowerCase() === data.correct_answer.trim().toLowerCase()) {
              label.classList.add("correct");
            } else if (radio.checked && !data.is_correct) {
              label.classList.add("incorrect");
            }
          });
        }

        // Show Feedback Box
        feedbackBox.style.display = "block";
        if (data.is_correct) {
          feedbackBox.className = "feedback-box feedback-correct";
          feedbackTitle.innerHTML = "✓ Correct Answer!";
        } else {
          feedbackBox.className = "feedback-box feedback-incorrect";
          feedbackTitle.innerHTML = "✕ Incorrect / Incomplete";
        }

        feedbackText.innerText = data.feedback;
        if (data.diff_rationale && feedbackRationale) {
          feedbackRationale.style.display = "block";
          feedbackRationale.innerHTML = `<strong>Adaptive Engine:</strong> ${data.diff_rationale}`;
        }

        // Setup Next Button
        if (nextBtn) {
          nextBtn.style.display = "inline-flex";
          if (data.is_completed) {
            nextBtn.innerText = "View Final Learning Report →";
            nextBtn.onclick = () => {
              window.location.href = data.report_url;
            };
          } else {
            nextBtn.innerText = "Next Question →";
            nextBtn.onclick = () => {
              window.location.reload();
            };
          }
        }

      } catch (err) {
        console.error(err);
        alert("An error occurred while evaluating your answer. Please try again.");
        submitBtn.disabled = false;
        submitBtn.innerHTML = "Submit Answer";
      }
    });
  }
});
