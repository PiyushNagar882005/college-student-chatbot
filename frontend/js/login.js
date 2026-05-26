async function login() {

    const username =
        document.getElementById(
            "username"
        ).value;

    const password =
        document.getElementById(
            "password"
        ).value;

    const response = await fetch(
        `${BACKEND_URL}/login`,
        {

            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

                username,
                password
            })
        }
    );

    const data = await response.json();

    if (data.message) {

        localStorage.setItem(
            "username",
            username
        );

        window.location.href =
            "dashboard.html";

    } else {

        alert(data.error);
    }
}