<script>
    import { goto } from "$app/navigation";
    import { getContext } from "svelte";
    import { API_ENDPOINT, BLANK_SESSION ,USER_ID} from "$lib/constants.js";

    const session = getContext("session");

    let username = "";
    let password = "";
    let error = "";
    

    async function login() {
        let userpass = `${username}:${password}`;

        let response;
        let response_json;

        try {
            // Access django api via svelte proxy (in order to set auth cookie securely)
            response = await fetch(`${API_ENDPOINT}/auth/login/`, {
                method: "POST", headers: {"Authorization": `Basic ${btoa(userpass)}`}
            });
            response_json = await response.json();
        } catch (error) {
            error = "Error, please try again later!";
            return;
        }

        if (response.ok) {
            if (error) error = "";
            let newSession = structuredClone(BLANK_SESSION);
            let storeID = structuredClone(USER_ID);
            newSession.token = response_json.token;

            try {
                response = await fetch(`${API_ENDPOINT}/auth/user/me/`, {
                    method: "GET", headers: {"Authorization": `Token ${response_json.token}`}
                });
                response_json = await response.json();
            } catch (error) {
                error = "Error, please try again later!";
                return;
            }

            if (response.ok) {
                newSession.userType = response_json.user_type
                newSession.userId = response_json.id
                newSession.firstName = response_json.first_name
                newSession.lastName = response_json.last_name
                session.set(newSession);
                goto("/dashboard/");
            } else if (response.status < 500) {
                error = response_json.detail;
            } else {
                error = "Server Error, please try again later!";
            }

        } else if (response.status < 500) {
            error = response_json.detail;
        } else {
            error = "Server error, please try again later!"
        }
    }

</script>

<div class="d-flex flex-column vh-100 align-items-center justify-content-center gap-2">
    <form on:submit|preventDefault={login}>
        <div class=text-danger>
            <small>{error}</small>
        </div>
        <div class="form-floating mb-2">
            <input
                type="text" class="form-control"
                id="login-username-email" placeholder="name@example.com"
                required bind:value={username}
            />
            <label for="login-username-email">Username or Email</label>
        </div>
        <div class="form-floating mb-2">
            <input
                type="password" class="form-control"
                id="login-password" placeholder="Password"
                required bind:value={password}
            />
            <label for="login-password">Password</label>
        </div>
        <div class="form-text mb-2"><a href="/reset-password">Forgot your password?</a></div>
        <button type="submit" class="btn btn-primary mb-2">Login</button>
        <div class="form-text mb-2">Don't have an account? <a href="/register">Register</a></div>
    </form>
</div>