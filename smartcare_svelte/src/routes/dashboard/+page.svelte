<script>
    import { getContext } from "svelte";
    import { goto } from '$app/navigation';
    import { API_ENDPOINT } from "$lib/constants";
    import PatientDashboard from "$lib/components/PatientDashboard.svelte";

    const session = getContext("session");

    let accessToken = "";
    let alert = "";

	session.subscribe((values) => {
		accessToken = values.token ? values.token : "";
	});

    async function logout() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/auth/logout/`, {
                method: "POST",
                headers: {
                    "Authorization": `Token ${accessToken}`
                }
            });
        } catch (error) {
            return;
        }
        try {
            await fetch("/api/logout/", {method: "POST"});
        } catch (error) {}

        if (response.status < 500) {
            goto("/");
        } else {
            alert = "Server error, please try again later!";
        }
    }
</script>

<!-- <div class="container">
    <h1>Dashboard</h1>
    {#if alert !== ""}
    <div class="alert alert-danger" role="alert">{alert}</div>
    {/if}
    <button type="button" class="btn btn-primary" on:click={logout}>
        Logout
    </button>
</div> -->
<div class="container-fluid">
    <PatientDashboard />
</div>
