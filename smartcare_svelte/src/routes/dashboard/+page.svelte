<script>
    import { browser } from '$app/environment';
    import { getContext } from "svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import { API_ENDPOINT } from '$lib/constants';
    import { DataHandler, RowCount } from '@vincjo/datatables';
    import Th from "$lib/components/Th.svelte";
    import ThFilter from "$lib/components/ThFilter.svelte";

    const session = getContext("session");
    let doctorTypes = [0,1,2,3]

    const handler = new DataHandler([], { rowsPerPage: 50 })
    const rows = handler.getRows()
    const selected = handler.getSelected()
    const isAllSelected = handler.isAllSelected()

    let prescriptions = []
                  
    async function loadPrescriptions() {
        let response;
        let api_route = API_ENDPOINT;
        if ($session.userType == 5) {
            api_route = api_route + "/prescriptions/my_prescriptions/";
        } else if (doctorTypes.includes($session.userType)) {
            api_route = api_route + "prescriptions/";
        }

        try {
            response = await fetch(api_route, {
                method: "GET",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });
            prescriptions = await response.json();
            handler.setRows(prescriptions)
        } catch (error) {
            console.log(error);
        }
    };

    $: {
        if (browser)
            loadPrescriptions();
    }

    async function requestButtonClick() {
        console.log(1)
        let response;
        let api_route = API_ENDPOINT;
        api_route = api_route + "/prescriptions/createPrescriptionRequest/"
        
    }
</script>

<IdleDetection userType={$session.userType} {session} />

<!--

    if staff:
        staff dashboard homepage
    else:
        all patient components

-->

{#if doctorTypes.includes($session.userType)}
    <table class="table">
        <thead class="table-light">
            <tr>
                <th class="selection">
                    <input
                        type="checkbox"
                        on:click={() => handler.selectAll({ selectBy: 'id' })}
                        checked={$isAllSelected}
                    />
                </th>
                <Th {handler} orderBy={(row) => row.patient.first_name}
                    >First name</Th
                >
                <Th {handler} orderBy={(row) => row.patient.last_name}
                    >Last Name</Th
                >
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
{:else if $session.userType === 5}
    <table class="table">
        <thead class="table-light">
            <tr>
                <th class="selection"></th>
                <Th {handler} orderBy={(row) => row.patient.first_name}
                    >First name</Th
                >
                <Th {handler} orderBy={(row) => row.patient.last_name}
                    >Last Name</Th
                >
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
    {#if $selected.length > 0 }
        <button class="btn btn-lg btn-primary float-end" on:click="{requestButtonClick}">Make Request</button>
    {:else }
        <button class="btn btn-lg btn-primary float-end" on:click="{requestButtonClick}" disabled>Make Request</button>
    {/if}
{/if}
