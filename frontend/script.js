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
    for (const file of fileInput.files) {
        formData.append("files", file);
    }

    try {
        const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        // Tabelle für hochgeladene Dateien aktualisieren
        const uploadedFilesTable = document.getElementById("uploadedFilesTable");
        const uploadedFilesBody = document.getElementById("uploadedFilesBody");

        uploadedFilesBody.innerHTML = ""; // Tabelle leeren
        uploadedFilesTable.style.display = "table"; // Tabelle sichtbar machen

        for (const filename of result.filenames) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");
            cell.textContent = filename;
            row.appendChild(cell);
            uploadedFilesBody.appendChild(row);
        }

    } catch (error) {
        document.getElementById("uploadResult").innerText = "Fehler beim Hochladen.";
        console.error(error);
    }
});