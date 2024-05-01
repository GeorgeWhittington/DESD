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

    const today = new Date().toISOString().split("T")[0];

    let registrationSchema = yup.object({
        first_name: yup.string().required("Please enter your first name").max(150),
        last_name: yup.string().required("Please enter your last name").max(150),
        email: yup.string().required("Please enter your email").email("Please enter a valid email address"),
        password: yup.string().required("Please enter a password").password(),
        password_confirm: yup.string().required("Please confirm your password").oneOf([yup.ref("password")], "Passwords must match"),
        user_type: yup.string().required("Please select a user type").oneOf(user_types.map(ut => ut.id), "Please select a user type"),
        date_of_birth: yup.date().required("Please enter your date of birth").max(today),
        phone_number: yup.string().required().max(14).matches(/^[\d -]*$/, {message: "Phone numbers cannot contain values other than digits and hyphens"}).min(3, "Phone numbers must be atleast 3 digits long"),
        address_line_1: yup.string().required().max(50).min(1),
        address_line_2: yup.string().max(50),
        city: yup.string().required().max(30).min(1).matches(/^\D+$/, {message: "City/Town names cannot include digits"}),
        postcode: yup.string().required().max(7).matches(/^[0-9a-zA-Z]{5,7}$/, {message: "Please enter a valid postcode which is 5 to 7 characters long"})
    })
    let patientRegistrationSchema = registrationSchema.pick(["first_name", "last_name", "email", "password", "password_confirm", "date_of_birth", "phone_number", "address_line_1", "address_line_2", "city", "postcode"]);

    let first_name = "";
    let last_name = "";
    let email = "";
    let password = "";
    let password_confirm = "";
    let user_type = "";
    let date_of_birth = "";
    let phone_number = "";
    let address_line_1 = "";
    let address_line_2 = "";
    let city = "";
    let postcode = "";

    let errors = {};

    $: first_name_errors = errors.hasOwnProperty("first_name") ? errors["first_name"] : [];
    $: last_name_errors = errors.hasOwnProperty("last_name") ? errors["last_name"] : [];
    $: email_errors = errors.hasOwnProperty("email") ? errors["email"] : [];
    $: password_errors = errors.hasOwnProperty("password") ? errors["password"] : [];
    $: password_confirm_errors = errors.hasOwnProperty("password_confirm") ? errors["password_confirm"] : [];
    $: user_type_errors = errors.hasOwnProperty("user_type") ? errors["user_type"] : [];
    $: date_of_birth_errors = errors.hasOwnProperty("date_of_birth") ? errors["date_of_birth"] : [];
    $: phone_number_errors = errors.hasOwnProperty("phone_number") ? errors["phone_number"] : [];
    $: address_line_1_errors = errors.hasOwnProperty("address_line_1") ? errors["address_line_1"] : [];
    $: address_line_2_errors = errors.hasOwnProperty("address_line_2") ? errors["address_line_2"] : [];
    $: city_errors = errors.hasOwnProperty("city") ? errors["city"] : [];
    $: postcode_errors = errors.hasOwnProperty("postcode") ? errors["postcode"] : [];

    let serverError = "";

    async function register() {
        let regData = {
            first_name: first_name,
            last_name: last_name,
            email: email,
            password: password,
            password_confirm: password_confirm,
            user_type: data.slug == "patient" ? "5" : user_type,
            date_of_birth: date_of_birth == "" ? null : date_of_birth,
            phone_number: phone_number,
            address_line_1: address_line_1,
            address_line_2: address_line_2,
            city: city,
            postcode: postcode
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

<div class="d-flex flex-column justify-content-center align-items-center register-container">
    <form class="container" on:submit|preventDefault={register} novalidate>
        {#if data.slug == "staff"}
        <div class="alert alert-primary mt-2" role="alert">
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
        <div class="row mb-2">
            <div class="col">
                <Field type="text" bind:value={address_line_1} errors={address_line_1_errors} id="register-address-line-1" label="Address Line 1" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col">
                <Field type="text" bind:value={address_line_2} errors={address_line_2_errors} id="register-address-line-2" label="Address Line 2" />
            </div>
        </div>
        <div class="row mb-2 g-2">
            <div class="col-sm">
                <Field type="text" bind:value={city} errors={city_errors} id="register-city" label="City/Town" />
            </div>
            <div class="col-sm">
                <Field type="text" bind:value={postcode} errors={postcode_errors} id="register-postcode" label="Postcode" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col">
                <Field type="text" bind:value={phone_number} errors={phone_number_errors} id="register-phone-number" label="Phone Number" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col">
                <Field type="date" bind:value={date_of_birth} errors={date_of_birth_errors} id="register-date-of-birth" label="Date Of Birth" />
            </div>
        </div>
        <div class="row">
            <div class="col">
                <button type="submit" class="btn btn-primary mb-2">Register</button>
            </div>
        </div>
    </form>
</div>

<style>
    .register-container {
        min-height: 100vh;
    }
</style>