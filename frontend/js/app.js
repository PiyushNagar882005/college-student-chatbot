/* ========================= */
/* Toggle Upload Menu */
/* ========================= */

function toggleUploadMenu() {

    const menu =
        document.getElementById(
            "uploadMenu"
        );

    menu.classList.toggle(
        "show"
    );
}


/* ========================= */
/* Close menu on document click */
/* ========================= */

document.addEventListener(
    "click",
    (e) => {

        const uploadWrapper =
            document.querySelector(
                ".upload-wrapper"
            );

        if (!uploadWrapper.contains(e.target)) {

            const menu =
                document.getElementById(
                    "uploadMenu"
                );

            menu.classList.remove(
                "show"
            );
        }
    }
);


/* ========================= */
/* Handle PDF file selection */
/* ========================= */

document.addEventListener(
    "change",
    (e) => {

        if (e.target.id === "pdfFile") {

            if (e.target.files.length > 0) {

                uploadPDF();
            }
        }
    }
);
