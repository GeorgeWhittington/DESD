<script>
    import { getContext, onMount } from "svelte";
    import { writable } from "svelte/store";
    import { apiGET, apiPATCH, apiPOST } from "$lib/apiFetch.js";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import Field from "$lib/components/Field.svelte";

    const session = getContext("session");
    const payrates = writable([]);
    let error = "";
    let result = "";

    async function loadPayrates() {
        error = "";
        let response = await apiGET(session, "/payrate/");
        if (response && response.ok) {
            payrates.set(await response.json());
        } else {
            error = "Server error, please try again later!";
        }
    }

    async function updatePayrate(payrate) {
        error = "";
        result = "";
        let response = await apiPATCH(session, `/payrate/${payrate.id}/`, JSON.stringify({
            title: payrate.title, rate: payrate.rate
        }));
        if (!response) {
            error = "Server error, please try again later!";
            return;
        }

        let response_json;
        try {
            response_json = await response.json();
        } catch {
            error = "Server error, please try again later!";
            return;
        }

        if (response.ok) {
            result = `Updated payrate #${response_json.id}`;
            loadPayrates();
            return;
        } else {
            error = response_json.detail;
        }
    }

    let newPayrateTitle = "";
    let newPayrateRate = "";

    async function createPayrate() {
        error = "";
        result = "";
        let response = await apiPOST(session, "/payrate/", JSON.stringify({
            title: newPayrateTitle, rate: newPayrateRate
        }));

        newPayrateTitle = "";
        newPayrateRate = "";

        if (!response) {
            error = "Server error, please try again later!";
            return;
        }

        let response_json;
        try {
            response_json = await response.json();
        } catch {
            error = "Server error, please try again later!";
            return;
        }

        if (response.ok) {
            result = `Created payrate #${response_json.id}`;
            loadPayrates();
            return;
        } else {
            error = response_json.detail;
        }
    }

    onMount(() => {
        loadPayrates();
    })
</script>

<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1]} />

<div class="card mt-3">
    <div class="card-body">
        <h2 class="card-title">Manage Payrates</h2>

        {#if error !== ""}
        <div class="alert alert-danger" role="alert">{error}</div>
        {/if}

        {#if result !== ""}
        <div class="alert alert-success" role="alert">{result}</div>
        {/if}

        <form class="d-flex justify-content-between mb-4" on:submit|preventDefault={createPayrate} >
            <button type="submit" class="btn btn-primary d-flex text-nowrap align-items-center"><i class="bi bi-plus h3 mb-0"></i><span>Add New</span></button>
            <Field type="text" bind:value={newPayrateTitle} id="new-payrate-title" label="Title" errors={[]} custom_classes="w-100 ms-2" />
            <Field type="number" bind:value={newPayrateRate} id="new-payrate-rate" label="Rate" errors={[]} custom_classes="w-100 ms-2" />
        </form>

        {#each $payrates as payrate}
        <form class="d-flex justify-content-between mt-2" on:submit|preventDefault={updatePayrate.bind(null, payrate)} >
            <span class="align-self-center">#{payrate.id}</span>
            <Field type="text" bind:value={payrate.title} id="payrate-{payrate.id}-title" label="Title" errors={[]} custom_classes="w-100 ms-2" />
            <Field type="number" bind:value={payrate.rate} id="payrate-{payrate.id}-rate" label="Rate" errors={[]} custom_classes="w-100 ms-2" />
            <button type="submit" class="btn btn-primary ms-2">Update</button>
        </form>
        {/each}
    </div>
</div>

