<script>
    import * as yup from "yup";
    import YupPassword from "yup-password";
    YupPassword(yup);
    import { goto } from "$app/navigation";
    import Field from "$lib/components/Field.svelte";
    import { API_ENDPOINT } from "$lib/constants.js";
    export let data;

    let resetPasswordSchema = yup.object({
        new_password: yup.string().required("Please enter a password").password(),
        new_password_confirm: yup.string().required("Please confirm your password").oneOf([yup.ref("new_password")], "Passwords must match")
    })

    let new_password = "";
    let new_password_confirm = "";

    let errors = {};

    $: new_password_errors = errors.hasOwnProperty("new_password") ? errors["new_password"] : [];
    $: new_password_confirm_errors = errors.hasOwnProperty("new_password_confirm") ? errors["new_password_confirm"] : [];

    let serverError = "";

    async function reset_password() {
        try {
            await resetPasswordSchema.validate(
                {"new_password": new_password, "new_password_confirm": new_password_confirm},
                { abortEarly: false }
            );
        } catch (outerErr) {
            errors = {};
            for (let err of outerErr.inner) {
                if (err.path in errors) {
                    errors[err.path].push(err.message);
                } else {
                    errors[err.path] = [err.message];
                }
            }
            return;
        }

        let response;
        let response_json;
        try {
            response = await fetch(`${API_ENDPOINT}/auth/password-reset/after/`, {
                method: "POST",
                body: JSON.stringify({"new_password": new_password, "token": data.token}),
                headers: {
                    "content-type": "application/json",
                },
            });
            response_json = await response.json();
        } catch (error) {
            serverError = "Error, please try again later!";
            return;
        }

        if (response.ok) {
            goto("/login");
        } else if (response.status < 500) {
            serverError = response_json.detail;
        } else {
            serverError = "Server error, please try again later!"
        }
    }

</script>

<div class="d-flex flex-column vh-100 align-items-center justify-content-center gap-2">
    <form on:submit|preventDefault={reset_password}>
        <div class=text-danger>
            <small>{serverError}</small>
        </div>
        <Field type="password" bind:value={new_password} errors={new_password_errors} id="new-password" label="New Password" custom_classes="mb-2" />
        <Field type="password" bind:value={new_password_confirm} errors={new_password_confirm_errors} id="new-password-confirm" label="Confirm New Password" custom_classes="mb-2" />
        <button type="submit" class="btn btn-primary mb-2">Reset Password</button>
    </form>
</div>