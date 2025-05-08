// Dateien auswählen und Dateiliste anzeigen
document.getElementById("fileInput").addEventListener("change", (e) => {
    const fileList = document.getElementById("fileList");
    fileList.innerHTML = ""; // Liste leeren

    const files = e.target.files;
    for (const file of files) {
        const listItem = document.createElement("div");
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    }
});

// Dateien hochladen
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

    } catch (error) {
        document.getElementById("uploadResult").innerText = "Fehler beim Hochladen.";
        console.error(error);
    }
});