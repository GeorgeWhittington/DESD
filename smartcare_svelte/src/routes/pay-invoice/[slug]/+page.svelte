<script>
    import { getContext, onMount } from "svelte";
    import { apiGET } from "$lib/apiFetch.js";
    import { goto } from "$app/navigation";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import GenerateTurnoverReportsCard from "$lib/components/GenerateTurnoverReportsCard.svelte";

    export let data;

    const session = getContext("session");
    let error = "";
    let paid = false;

    async function loadIfPaid() {
        error = "";
        let response = await apiGET(session, `/invoice/${data.slug}/is_invoice_paid/`);

        if (response.ok) {
            try {
                let response_json = await response.json();
                paid = response_json.is_paid;
            } catch {
                error = "Server error, please try again";
            }
        } else if (response.status == 403 || response.status == 404) {
            // user is not authorised to pay invoice / invoice does not exist
            alert("You are unauthorized.")
            goto("/")
        } else {
            error = "Server error, please try again";
        }
    }

    async function payInvoice() {
        error = "";
        let response = await apiGET(session, `/invoice/${data.slug}/pay_invoice/`);

        if (!response) {
            error = "Server error, please try again";
            return;
        }

        if (response.ok) {
            paid = true;
        } else if (response.status == 403 || response.status == 404) {
            // user is not authorised to pay invoice / invoice does not exist
            alert("You are unauthorized.")
            goto("/")
        } else {
            error = "Server error, please try again";
        }
    }

    onMount(() => {
        if (![4, 5].includes($session.userType)) {
            alert("You are unauthorized.")
            goto("/")
        }

        loadIfPaid();
    })
</script>

{#if [4, 5].includes($session.userType)}

{#if !paid}
<div class="d-flex vh-100 justify-content-center align-items-center">
    {#if error != ""}
    <div class="alert alert-danger" role="alert">
        {error}
    </div>
    {/if}
    <button class="btn btn-lg btn-primary" on:click={payInvoice}>Pay Invoice</button>
</div>

{:else}
<div class="d-flex vh-100 justify-content-center align-items-center">
    {#if error != ""}
    <div class="alert alert-danger" role="alert">
        {error}
    </div>
    {/if}
    <h2>Your invoice is paid!</h2>
</div>

{/if}

{/if}