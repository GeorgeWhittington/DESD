<script>
    import { API_ENDPOINT } from "$lib/constants.js";

    let email = "";
    let error = "";
    let submitted = false;

    async function request_password_reset() {
        let response;
        let response_json;

        try {
            response = await fetch(`${API_ENDPOINT}/auth/password-reset/`, {
                method: "POST",
                body: JSON.stringify({"email": email}),
                headers: {
                    "content-type": "application/json",
                },
            });
            response_json = await response.json();
        } catch (error) {
            error = "Error, please try again later!";
            return;
        }

        if (response.ok) {
            submitted = true;
        } else if (response.status < 500) {
            error = response_json.detail;
        } else {
            error = "Server error, please try again later!"
        }
    }

</script>

{#if !submitted}

<div class="d-flex flex-column vh-100 align-items-center justify-content-center gap-2">
    <form on:submit|preventDefault={request_password_reset}>
        <div class=text-danger>
            <small>{error}</small>
        </div>
        <div class="form-floating mb-2">
            <input
                type="email" class="form-control"
                id="reset-password-email" placeholder="name@example.com"
                required bind:value={email}
            />
            <label for="reset-password-email">Email</label>
        </div>
        <button type="submit" class="btn btn-primary mb-2">Reset Password</button>
    </form>
</div>

{:else}

<div class="d-flex flex-column vh-100 align-items-center justify-content-center gap-2">
    <p>Password reset request sent, please check your email!</p>
</div>

{/if}