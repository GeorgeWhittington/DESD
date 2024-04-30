<script>
    import { API_ENDPOINT, MEDIA_ENDPOINT } from "$lib/constants";
    import { apiPOST } from "$lib/apiFetch.js";
    export let session;

    const today = new Date().toISOString().split("T")[0];
    let from_date = today;
    let to_date = today;

    const invoice_types = [
        { id: "all", text: "All"},
        { id: "nhs", text: "NHS"},
        { id: "private", text: "Private"}
    ];

    let selected_invoice_type = invoice_types[0].id;

    function date_change(item) {
        if (item === "to" && to_date < from_date) {
            from_date = to_date;
        }

        if (item === "from" && from_date > to_date) {
            to_date = from_date;
        }
    }

    let report = "";
    let error = "";

    async function generate_report() {
        error = "";
        report = "";
        let response = await apiPOST(session, "/generate-turnover-report/", JSON.stringify({
            from: from_date, to: to_date, type: selected_invoice_type
        }));

        if (response) {
            let response_json = await response.json();

            if (response.ok) {
                report = response_json.pdf;
            } else if (response.status < 500) {
                error = response_json.detail;
            } else {
                error = "Server Error, Please try again";
            }
        } else {
            error = "Server Error, Please try again";
        }
    }
</script>

<div class="card">
    <div class="card-body">
        <h2 class="card-title">Generate Reports</h2>
        {#if error != ""}
            <p class="text-danger">{error}</p>
        {/if}
        <form on:submit={generate_report}>
            <div class="col input-group">
                <span class="input-group-text">From</span>
                <input type="date" class="form-control" max={today} bind:value={from_date} on:input={ () => date_change("from") } />
            </div>
            <div class="col input-group mt-2">
                <span class="input-group-text">To</span>
                <input type="date" class="form-control" max={today} bind:value={to_date} on:input={ () => date_change("to") } />
            </div>
            <div class="input-group mt-2">
                <label class="input-group-text" for="generate-report-invoice-type">Invoice Type</label>
                <select id="generate-report-invoice-type" class="form-select" bind:value={selected_invoice_type}>
                    {#each invoice_types as invoice_option}
                    <option value={invoice_option.id}>{invoice_option.text}</option>
                    {/each}
                </select>
            </div>
            <input type="submit" value="Generate turnover report" class="btn btn-primary mt-2" />
            {#if report != ""}
                <a href="{MEDIA_ENDPOINT}{report}">Download Report</a>
            {/if}
        </form>
    </div>
</div>