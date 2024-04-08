<script>
    const today = new Date().toISOString().split("T")[0];
    let from_date = today;
    let to_date = today;

    const invoice_types = [
        { id: 0, text: "All"},
        { id: 1, text: "NHS"},
        { id: 2, text: "Private"}
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

    function generate_report() {
        // TODO: actually request generation of invoice pdf (then render a link to download it next to or below button?)
    }
</script>

<div class="card">
    <div class="card-body">
        <h2 class="card-title">Generate Reports</h2>
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
        </form>
    </div>
</div>