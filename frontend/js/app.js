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
/* Close Upload Menu */
/* ========================= */

function closeUploadMenu() {

    const menu =
        document.getElementById(
            "uploadMenu"
        );

    menu.classList.remove(
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

        if (uploadWrapper && !uploadWrapper.contains(e.target)) {

            closeUploadMenu();
        }
    }
);


/* ========================= */
/* Export Global Functions */
/* ========================= */

window.toggleUploadMenu = toggleUploadMenu;
window.closeUploadMenu = closeUploadMenu;
