<script>
    import { getContext, onMount } from "svelte";
    import { DataHandler } from "@vincjo/datatables";
    import Th from "$lib/components/Th.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import GenerateTurnoverReportsCard from "$lib/components/GenerateTurnoverReportsCard.svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import TablePagination from "$lib/components/TablePagination.svelte";
    import { API_ENDPOINT } from "$lib/constants.js";
    import { apiGET } from "$lib/apiFetch.js";

    const session = getContext("session");

    const today = new Date().toISOString().split("T")[0];
    let invoice_date = today;

    let invoices = [];
    const handler = new DataHandler(invoices, { rowsPerPage: 10 });
    const rows = handler.getRows();
    const rowCount = handler.getRowCount();

    const blank = "-";
    let income_total = blank;
    let income_settled = blank;

    $: {
        let total = 0;
        let settled = 0;

        for (const row of invoices) {
            total += row.amount;
            if (row.is_paid)
                settled += row.amount;
        }

        if (total === 0) {
            income_total = blank;
            income_settled = blank;
        } else {
            income_total = total.toFixed(2);
            income_settled = settled.toFixed(2);
        }
    }

    async function loadInvoices() {
        let response = await apiGET(session, `/invoice/?date=${invoice_date}`);
        if (response && response.ok) {
            invoices = await response.json();
            handler.setRows(invoices);
        } else if (response) {
            // TODO: other error
        } else {
            // TODO show server error
        }
    };

    onMount(() => {
        loadInvoices();
    });
</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1]} />

<GenerateTurnoverReportsCard session={session} />

<div class="card mt-3">
    <div class="card-body ">
        <h2 class="card-title">Invoices</h2>
        <form on:submit={loadInvoices}>
            <div class="input-group">
                <input type="date" class="form-control" max={today} bind:value={invoice_date} />
                <input type="submit" value="Fetch Invoices" class="btn btn-primary" />
            </div>
        </form>
        <div class="mt-2 d-flex align-items-center">
            <b><span>Total Income: </span></b>
            <span class="ms-1">£{income_total}</span>
            <b><span class="ms-4">Settled Income: </span></b>
            <span class="ms-1">£{income_settled}</span>
        </div>
        <table class="table mt-2">
            <thead class="table-light">
                <tr>
                    <Th handler={handler} orderBy={row => row.patient.first_name + row.patient.last_name}>Patient</Th>
                    <Th handler={handler} orderBy={row => row.staff.first_name + row.staff.last_name}>Staff</Th>
                    <Th handler={handler} orderBy="duration">Duration</Th>
                    <Th handler={handler} orderBy="amount">Amount Charged</Th>
                    <Th handler={handler} orderBy="paid_at">Paid At</Th>
                    <Th handler={handler} orderBy="is_paid">Paid</Th>
                </tr>
            </thead>
            <tbody>
                {#each $rows as row}
                    <tr>
                        <td>{row.patient.first_name} {row.patient.last_name}</td>
                        <td>{row.staff.first_name} {row.staff.last_name}</td>
                        <td>{row.duration.substring(0, 8)}</td>
                        <td>£{row.amount}</td>
                        <td>
                            {#if row.is_paid}
                                {(new Date(row.paid_at)).toDateString()}
                            {:else}
                                -
                            {/if}
                        </td>
                        <td>{#if row.is_paid} ✅ {:else} ❌ {/if}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
        <footer class="d-flex justify-content-between align-items-center">
            <div>
                {#if $rowCount.total > 0}
                    Showing <b>{$rowCount.start}</b>
                    to <b>{$rowCount.end}</b>
                    of <b>{$rowCount.total}</b>
                {:else}
                    No entries found
                {/if}
            </div>
            <TablePagination handler={handler} />
        </footer>
    </div>
</div>
