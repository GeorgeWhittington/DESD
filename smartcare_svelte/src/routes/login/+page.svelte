<script>
    import { goto } from '$app/navigation';

    let username = "";
    let password = "";
    let error = "";

    // TODO: check if already logged in (make a /api/me/ endpoint to check token is valid?)
    // redirect straight to dashboard if so

    async function login() {
        let userpass = `${username}:${password}`;

        let response;
        let response_json;

        try {
            // Access django api via svelte proxy (in order to set auth cookie securely)
            response = await fetch(`/api/login/`, {
                method: "POST",
                body: JSON.stringify({ credentials: btoa(userpass) }),
                headers: {
                    "content-type": "application/json"
                }
            });
            response_json = await response.json();
        } catch (error) {
            return;
        }

        if (response.ok) {
            if (error) error = "";
            goto("/dashboard/");
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