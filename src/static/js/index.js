const codeInput = document.querySelector("#code-input");
const goToModuleForm = document.querySelector("#go-to-module");

goToModuleForm.onsubmit = (event) => {
    event.preventDefault();
    if (codeInput.value === "") {
        alert("Enter a module code.");
        return;
    }
    const module_url = `/module/${codeInput.value.toUpperCase()}`;
    fetch(module_url, {method: "HEAD"}).then(response => {
        switch (response.status) {
            case 404:
                alert("Couldn't find a module with that code.");
                break;
            case 200:
                window.location = module_url;
                break;
            default:
                alert("Unexpected response from the server. Please try again later.")
        }
    })
};
