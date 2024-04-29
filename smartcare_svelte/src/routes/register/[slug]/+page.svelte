<script>
// @ts-nocheck

    import * as yup from "yup";
    import YupPassword from "yup-password";
    YupPassword(yup);
    import { goto } from '$app/navigation';
    import Field from "$lib/components/Field.svelte";
    import { API_ENDPOINT } from "$lib/constants.js";
    export let data;

    let user_types = [
        {id: "2", text: "Doctor"},
        {id: "3", text: "Nurse"},
        {id: "1", text: "Admin"},
        {id: "4", text: "External"},
    ];
    let user_type_changed = false;

    let registrationSchema = yup.object({
        first_name: yup.string().required("Please enter your first name").max(150),
        last_name: yup.string().required("Please enter your last name").max(150),
        email: yup.string().required("Please enter your email").email("Please enter a valid email address"),
        password: yup.string().required("Please enter a password").password(),
        password_confirm: yup.string().required("Please confirm your password").oneOf([yup.ref("password")], "Passwords must match"),
        user_type: yup.string().required("Please select a user type").oneOf(user_types.map(ut => ut.id), "Please select a user type")
    })
    let patientRegistrationSchema = registrationSchema.pick(["first_name", "last_name", "email", "password", "password_confirm"]);

    let first_name = "";
    let last_name = "";
    let email = "";
    let password = "";
    let password_confirm = "";
    let user_type = "none";

    let errors = {};

    $: first_name_errors = errors.hasOwnProperty("first_name") ? errors["first_name"] : [];
    $: last_name_errors = errors.hasOwnProperty("last_name") ? errors["last_name"] : [];
    $: email_errors = errors.hasOwnProperty("email") ? errors["email"] : [];
    $: password_errors = errors.hasOwnProperty("password") ? errors["password"] : [];
    $: password_confirm_errors = errors.hasOwnProperty("password_confirm") ? errors["password_confirm"] : [];
    $: user_type_errors = errors.hasOwnProperty("user_type") ? errors["user_type"] : [];

    let serverError = "";

    async function register() {
        let regData = {
            first_name: first_name,
            last_name: last_name,
            email: email,
            password: password,
            password_confirm: password_confirm,
            user_type: data.slug == "patient" ? "5" : user_type
        }

        try {
            if (data.slug == "staff") {
                await registrationSchema.validate(regData, { abortEarly: false });
            } else {
                await patientRegistrationSchema.validate(regData, { abortEarly: false });
            }
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

        // destructure data to remove duplicate pw field
        let { password_confirm: _, ...registrationFinal } = regData;
        let response;
        let response_json;

        try {
            response = await fetch(`${API_ENDPOINT}/auth/user/`, {
                method: "POST",
                body: JSON.stringify(registrationFinal),
                headers: {
                    "content-type": "application/json"
                }
            });
            response_json = await response.json();
        } catch (error) {
            return;
        }

        if (response.ok) {
            if (serverError) serverError = "";
            if (errors) errors = {};

            goto("/login");
        } else if (response.status < 500) {
            error = response_json.detail;
        } else {
            error = "Server error, please try again later!"
        }
    }
</script>

<div class="d-flex flex-column vh-100 justify-content-center align-items-center">
    <form class="container" on:submit|preventDefault={register} novalidate>
        {#if data.slug == "staff"}
        <div class="alert alert-primary" role="alert">
            After registering, please ask an administrator to activate your account. You will not be able to login without them doing so.
        </div>
        {/if}
        <div class="row mb-2 g-2">
            <div class="col-sm">
                <Field type="text" bind:value={first_name} errors={first_name_errors} id="register-first-name" label="First Name" />
            </div>
            <div class="col-sm">
                <Field type="text" bind:value={last_name} errors={last_name_errors} id="register-last-name" label="Last Name" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col">
                <Field type="email" bind:value={email} errors={email_errors} id="register-email" label="Email" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col">
                <Field type="password" bind:value={password} errors={password_errors} id="register-password" label="Password" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col">
                <Field type="password" bind:value={password_confirm} errors={password_confirm_errors} id="register-password-confirm" label="Confirm Password" />
            </div>
        </div>
        {#if data.slug == "staff"}
        <div class="row mb-2">
            <div class="col">
                <div class="form-floating">
                    <select
                        class="form-select {user_type_errors.length > 0 ? 'is-invalid' : ''}" id="register-user-type"
                        aria-label="Select User Type"
                        bind:value={user_type}
                        on:change|once={() => {user_type_changed = true}}
                    >
                        <option disabled={user_type_changed} value="none">Please select a user type</option>
                        {#each user_types as user_type}
                            <option value="{user_type.id}">{user_type.text}</option>
                        {/each}
                    </select>
                    <label for="register-user-type">User Type</label>
                </div>
            </div>
        </div>
        {/if}
        <div class="row">
            <div class="col">
                <button type="submit" class="btn btn-primary mb-2">Register</button>
            </div>
        </div>
    </form>
</div>