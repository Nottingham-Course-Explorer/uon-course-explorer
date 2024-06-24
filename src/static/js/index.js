const codeInput = document.querySelector("#code-input");
const goToModuleForm = document.querySelector("#go-to-module");

goToModuleForm.addEventListener("submit", event => {
    event.preventDefault();
    let query = codeInput.value;
    if (query === "") {
        alert("Enter a module code.");
        return
    }
    fetch(`/find-module/${query.toUpperCase()}`).then(response => {
        switch (response.status) {
            case 404:
                alert("Couldn't find a module with that code.");
                break;
            case 200:
                response.text().then(text => window.location = text);
                break;
            default:
                alert("Unexpected response from the server. Please try again later.")
        }
    })
})
