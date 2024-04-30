<script>
    export let session;
    export let is_doctor;

    import { onMount } from "svelte";
    import { DataHandler, RowCount } from '@vincjo/datatables';
    import Th from "$lib/components/Th.svelte";
    import ThFilter from "$lib/components/ThFilter.svelte";
    import { apiGET, apiPOST } from "$lib/apiFetch.js";

    const handler = new DataHandler([], { rowsPerPage: 50 })
    const rows = handler.getRows()
    const selected = handler.getSelected()
    const isAllSelected = handler.isAllSelected()

    let prescriptions = []
                
    async function loadPrescriptions() {
        let response;

        if (is_doctor) {
            response = await apiGET($session, "/prescriptions/");
        } else {
            response = await apiGET($session, "/prescriptions/my_prescriptions/");
        }

        if (response && response.ok) {
            prescriptions = await response.json();
            handler.setRows(prescriptions);
        } else {
            // TODO: display error to user
        }
    };

    async function requestButtonClick() {
        console.log($selected)
        //let response = await apiPOST($session, "/prescription-requests/create_request/", JSON.stringify({prescription_id : prescriptions[0].id}));
        //console.log(response)
    }

    onMount(() => {
        loadPrescriptions();
    })
</script>

<table class="table">
    <thead class="table-light">
        <tr>
            <th class="selection">
                {#if is_doctor}
                <input
                    type="checkbox"
                    on:click={() => handler.selectAll({ selectBy: 'id' })}
                    checked={$isAllSelected}
                />
                {/if}
            </th>
            <Th {handler} orderBy={(row) => row.patient.first_name}>First name</Th>
            <Th {handler} orderBy={(row) => row.patient.last_name}>Last Name</Th>
            <Th {handler} orderBy={(row) => row.medicine}>Medicine</Th>
            <Th {handler} orderBy={(row) => row.notes}>Notes</Th>
            <Th {handler} orderBy={(row) => row.is_repeating}>Repeating</Th>
        </tr>
        <tr>
            <th class="selection" />
            <ThFilter
                {handler}
                filterBy={(row) => row.patient.first_name}
            />
            <ThFilter {handler} filterBy={(row) => row.patient.last_name} />
            <ThFilter {handler} filterBy={(row) => row.medicine} />
            <ThFilter {handler} filterBy={(row) => row.notes} />
            <ThFilter {handler} filterBy={(row) => row.is_repeating} />
        </tr>
    </thead>
    <tbody>
        {#each $rows as row}
            <tr class:active={$selected.includes(row.id)}>
                <td class="selection">
                    <input
                        type="checkbox"
                        on:click={() => handler.select(row.id)}
                        checked={$selected.includes(row.id)}
                    />
                <td>{row.patient.first_name}</td>
                <td>{row.patient.last_name}</td>
                <td>{row.medicine}</td>
                <td>{row.notes}</td>
                <td>{row.is_repeating}</td>
            </tr>
        {/each}
    </tbody>
</table>
{#if !is_doctor}
    {#if $selected.length > 0 }
        <button class="btn btn-lg btn-primary float-end" on:click="{requestButtonClick}">Make Request</button>
    {:else }
        <button class="btn btn-lg btn-primary float-end" on:click="{requestButtonClick}" disabled>Make Request</button>
    {/if}
{/if}