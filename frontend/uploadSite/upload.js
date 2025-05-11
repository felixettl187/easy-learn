document.getElementById("fileInput").addEventListener("change", (e) => {
  const fileList = document.getElementById("fileList");
  fileList.innerHTML = "";

  const files = e.target.files;
  for (const file of files) {
    const listItem = document.createElement("div");
    listItem.textContent = file.name;
    fileList.appendChild(listItem);
  }
});

// "Upload"-Button klickt löst Upload aus
document.getElementById("uploadBtn").addEventListener("click", async (e) => {
  e.preventDefault(); // Verhindert Navigation

  const fileInput = document.getElementById("fileInput");
  if (fileInput.files.length === 0) {
    document.getElementById("uploadResult").innerText = "Bitte eine Datei auswählen.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    document.getElementById("uploadResult").innerText = "Upload erfolgreich.";
  } catch (error) {
    document.getElementById("uploadResult").innerText = "Fehler beim Hochladen.";
    console.error(error);
  }
});

// Beispiel für Submit-Logik (z. B. weiterleiten oder Feedback anzeigen)
document.getElementById("submitBtn").addEventListener("click", (e) => {
  e.preventDefault();
  alert("Submit wurde gedrückt!");
});