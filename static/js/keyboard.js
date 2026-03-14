document.addEventListener("DOMContentLoaded", function () {

    const inputs = Array.from(document.querySelectorAll("input, select"));

    inputs.forEach((input, index) => {

        input.addEventListener("keydown", function (e) {

            if (e.key === "Enter") {
                e.preventDefault();
                if (inputs[index + 1]) {
                    inputs[index + 1].focus();
                }
            }

            if (e.key === "ArrowDown") {
                e.preventDefault();
                if (inputs[index + 1]) {
                    inputs[index + 1].focus();
                }
            }

            if (e.key === "ArrowUp") {
                e.preventDefault();
                if (inputs[index - 1]) {
                    inputs[index - 1].focus();
                }
            }

        });

    });

    // CTRL + S submit form
    document.addEventListener("keydown", function(e){
        if(e.ctrlKey && e.key === "s"){
            e.preventDefault();
            document.querySelector("form").submit();
        }
    });

});