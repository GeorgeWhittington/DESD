<script>
    import * as yup from "yup";
    import YupPassword from "yup-password";
    YupPassword(yup);
    import { getContext, onMount } from "svelte";
    import { writable } from "svelte/store";
    import { apiGET, apiPATCH, apiPOST } from "$lib/apiFetch.js";
    import { PATIENT_PAY_TYPES, USER_TYPES } from "$lib/constants.js";

    const session = getContext("session");

    const user_data = writable({});
    let error = "";
    let result = "";
    let new_password = "";

    let password_schema = yup.object({
        password: yup.string().required("Please enter a password").password()
    });

    // from: https://stackoverflow.com/a/5574446
    String.prototype.toProperCase = function () {
        return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    };

    async function loadUserData() {
        error = "";
        let response = await apiGET(session, "/auth/user/me/");
        if (!response || !response.ok) {
            error = "Server error, please try again later!";
            return;
        }

        try {
            let response_json = await response.json();
            user_data.set(response_json);
            new_password = "";
        } catch {
            error = "Server error, please try again later!";
            return;
        }
    }

    async function updatePassword() {
        error = "";
        result = "";

        try {
            await password_schema.validate({password: new_password});
        } catch (err) {
            error = err.message;
            window.scrollTo(0, 0);
            return;
        }

        let response = await apiPOST(session, "/auth/user/update_password/", JSON.stringify({
            new_password: new_password
        }));

        if (!response || response.status >= 500) {
            error = "Server error, please try again later!";
            window.scrollTo(0, 0);
            return;
        } else if (response.ok) {
            result = "Password updated";
            new_password = "";
            window.scrollTo(0, 0);
            return;
        }

        try {
            let response_json = await response.json();
            error = response_json.detail;
        } catch {
            error = "Server error, please try again later!";
        }
        window.scrollTo(0, 0);
    }

    async function updateUserData(data_key) {
        error = "";
        result = "";
        let update = {};
        update[data_key] = $user_data[data_key];
        let response = await apiPATCH(session, `/auth/user/${$session.userId}/`, JSON.stringify(update));
        if (!response || response.status == 403 || response.status == 404 || response.status >= 500) {
            error = "Server error, please try again later!";
            window.scrollTo(0, 0);
            return;
        } else if (response.ok) {
            let data_key_formatted = data_key.split("_").join(" ").toProperCase();
            result = `Updated ${data_key_formatted}`;
            loadUserData();
            window.scrollTo(0, 0);
            return;
        }

        try {
            let response_json = await response.json();
            error = response_json[data_key];
        } catch {
            error = "Server error, please try again later!";
        }
        window.scrollTo(0, 0);
    }

    onMount(() => {
        loadUserData();
    });
</script>

<div class="card">
    <div class="card-body">
        <h5 class="card-title">Settings</h5>

        {#if error !== ""}
        <div class="alert alert-danger" role="alert">{error}</div>
        {/if}

        {#if result !== ""}
        <div class="alert alert-success" role="alert">{result}</div>
        {/if}

        <form on:submit|preventDefault={updatePassword}>
            <div class="mb-2">
                <label for="settings-password" class="form-label">Password</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="password" class="form-control" id="settings-password" bind:value="{new_password}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>

        <div class="mb-2">
            <label for="settings-first-name" class="form-label">First Name</label>
            <input type="text" disabled class="form-control" id="settings-first-name" value="{$user_data.first_name}">
        </div>

        <div class="mb-2">
            <label for="settings-last-name" class="form-label">Last Name</label>
            <input type="text" disabled class="form-control" id="settings-last-name" value="{$user_data.last_name}">
        </div>

        <form on:submit|preventDefault={updateUserData.bind(null, "email")}>
            <div class="mb-2">
                <label for="settings-email" class="form-label">Email</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="email" class="form-control" id="settings-email" bind:value="{$user_data.email}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>

        {#if $session.userType == 5 && $user_data.patient_info}
        <div class="mb-2">
            <label for="settings-patient-pay-type" class="form-label">Payment Method</label>
            <input type="text" disabled class="form-control" id="settings-patient-pay-type" value="{PATIENT_PAY_TYPES[$user_data.patient_info.pay_type]}">
        </div>
        {/if}

        {#if [0, 1, 2, 3, 4].includes($session.userType)}
        <div class="mb-2">
            <label for="settings-user-type" class="form-label">Account Type</label>
            <input type="text" disabled class="form-control" id="settings-user-type" value="{USER_TYPES[$session.userType]}">
        </div>
        {/if}

        <form on:submit|preventDefault={updateUserData.bind(null, "phone_number")}>
            <div class="mb-2">
                <label for="settings-phone-no" class="form-label">Phone Number</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="text" class="form-control" id="settings-phone-no" bind:value="{$user_data.phone_number}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>

        <div class="mb-2">
            <label for="settings-dob" class="form-label">Date of Birth</label>
            <input type="text" disabled class="form-control" id="settings-dob" value="{$user_data.date_of_birth}">
        </div>

        <form on:submit|preventDefault={updateUserData.bind(null, "address_line_1")}>
            <div class="mb-2">
                <label for="settings-addr-1" class="form-label">Address Line 1</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="text" class="form-control" id="settings-addr-1" bind:value="{$user_data.address_line_1}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>

        <form on:submit|preventDefault={updateUserData.bind(null, "address_line_2")}>
            <div class="mb-2">
                <label for="settings-addr-2" class="form-label">Address Line 2</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="text" class="form-control" id="settings-addr-2" bind:value="{$user_data.address_line_2}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>

        <form on:submit|preventDefault={updateUserData.bind(null, "city")}>
            <div class="mb-2">
                <label for="settings-city" class="form-label">City/Town</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="text" class="form-control" id="settings-city" bind:value="{$user_data.city}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>

        <form on:submit|preventDefault={updateUserData.bind(null, "postcode")}>
            <div class="mb-2">
                <label for="settings-post-code" class="form-label">Postcode</label>
                <div class="d-flex justify-content-between align-items-end">
                    <input type="text" class="form-control" id="settings-post-code" bind:value="{$user_data.postcode}">
                    <button class="btn btn-primary ms-2" type="submit">Update</button>
                </div>
            </div>
        </form>
    </div>
</div>