<script>
    import { DataHandler } from '@vincjo/datatables';
    import Th from "$lib/components/Th.svelte";
    import ThFilter from "$lib/components/ThFilter.svelte";
    import { getContext } from "svelte";
    import { API_ENDPOINT } from "$lib/constants";


    const session = getContext("session");

    const handler = new DataHandler([], { rowsPerPage: 50 })
    const rows = handler.getRows()

    let prescriptions = []


    export async function loadPrescriptions() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/prescriptions/`, {
                method: "GET",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

        prescriptions = await response.json();
        handler.setRows(prescriptions)
        console.log(prescriptions);


        } catch (error) {
            return "Server error, please try again later!";
        }
    }

    loadPrescriptions();   
   
</script>

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