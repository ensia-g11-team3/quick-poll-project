const pollForm = document.getElementById("pollForm");
const questionInput = document.getElementById("question");
const counter = document.getElementById("qCounter");
const formMessage = document.getElementById("formMessage");

// Update counter
questionInput.addEventListener("input", () => {
  counter.textContent = `${questionInput.value.length} / 200`;
});

// Handle form submission
pollForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = questionInput.value.trim();
  console.log("Submitting poll:", question);

  if (!question) {
    formMessage.textContent = "Poll question cannot be empty.";
    formMessage.style.color = "red";
    return;
  }

  try {
    const response = await fetch("/create_poll", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({pollQuestion: question})
    });
    const data = await response.json();
    if (response.ok) {
      formMessage.textContent = `✅ Poll created! ID: ${data.pollid}`;
      formMessage.style.color = "green";
      pollForm.reset();
      counter.textContent = "0 / 200";
    } else {
      formMessage.textContent = `❌ ${data.message}`;
      formMessage.style.color = "red";
    }
  } catch (err) {
    console.error(err);
    formMessage.textContent = "❌ Could not connect to server.";
    formMessage.style.color = "red";
  }
});
