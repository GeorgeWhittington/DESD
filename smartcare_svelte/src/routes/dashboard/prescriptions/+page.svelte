<script>
    import { DataHandler } from '@vincjo/datatables';
    import Th from "$lib/components/Th.svelte";
    import ThFilter from "$lib/components/ThFilter.svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import { getContext, onMount } from "svelte";
    import { API_ENDPOINT } from "$lib/constants";
    import { apiGET } from "$lib/apiFetch.js";

    const session = getContext("session");

    const handler = new DataHandler([], { rowsPerPage: 50 })
    const rows = handler.getRows()

    let prescriptions = []


    async function loadPrescriptions() {
        let response = await apiGET(session, "/prescriptions/");

        if (response && response.ok) {
            prescriptions = await response.json();
            handler.setRows(prescriptions)
            console.log(prescriptions);
        } else {
            return "Server error, please try again later!";
        }
    }

    onMount(() => {
        loadPrescriptions();
    })

</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3, 5]} />

<table class="table">
    <thead class="table-light">
        <tr>
            <Th {handler} orderBy={row => row.patient.first_name}>First name</Th>
            <Th {handler} orderBy={row => row.patient.last_name}>Last Name</Th>
            <Th {handler} orderBy={row => row.medicine}>Medicine</Th>
            <Th {handler} orderBy={row => row.notes}>Notes</Th>
            <Th {handler} orderBy={row => row.is_repeating}>Repeating</Th>
        </tr>
        <tr>
            <ThFilter {handler} filterBy={row => row.patient.first_name}/>
            <ThFilter {handler} filterBy={row => row.patient.last_name}/>
            <ThFilter {handler} filterBy={row => row.medicine}/>
            <ThFilter {handler} filterBy={row => row.notes}/>
            <ThFilter {handler} filterBy={row => row.is_repeating}/>
        </tr>
    </thead>
    <tbody>
        {#each $rows as row}
            <tr>
                <td>{row.patient.first_name}</td>
                <td>{row.patient.last_name}</td>
                <td>{row.medicine}</td>
                <td>{row.notes}</td>
                <td>{row.is_repeating}</td>
            </tr>
        {/each}
    </tbody>
</table>