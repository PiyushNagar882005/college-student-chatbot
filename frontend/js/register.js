async function register() {

    const username =
        document.getElementById(
            "username"
        ).value;

    const password =
        document.getElementById(
            "password"
        ).value;

    const response = await fetch(
        `${BACKEND_URL}/register`,
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

        alert("Registration Successful");

        window.location.href =
            "login.html";

    } else {

        alert(data.error);
    }
}