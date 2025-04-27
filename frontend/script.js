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
        document.getElementById("uploadResult").innerText = result.message;

    } catch (error) {
        document.getElementById("uploadResult").innerText = "Fehler beim Hochladen.";
        console.error(error);
    }
});