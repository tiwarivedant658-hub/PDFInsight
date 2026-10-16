
const fileInput = document.getElementById("pdf_file");
const fileName = document.getElementById("file-name");

if (fileInput && fileName) {
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
        } else {
            fileName.textContent = "No file selected";
        }
    });
}

console.log("Daily labels:", dailyLabels);
console.log("Daily values:", dailyValues);
console.log("Transaction types:", typeLabels);
console.log("Type values:", typeValues);
console.log("Merchant labels:", merchantLabels);
console.log("Merchant values:", merchantValues);

