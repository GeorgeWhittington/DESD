<script>
    import { DataHandler } from '@vincjo/datatables';
    import * as yup from "yup";
    import Th from "$lib/components/Th.svelte";
    import ThFilter from "$lib/components/ThFilter.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import { getContext, onMount } from "svelte";
    import { API_ENDPOINT } from "$lib/constants";
    import { apiGET, apiPOST } from "$lib/apiFetch.js";
    import Field from "$lib/components/Field.svelte";

    const session = getContext("session");

    let token;
    session.subscribe(value => {
        token = value.token;
    });
    // token = session.token

    let prescription_requests = []
    const handler = new DataHandler(prescription_requests, { rowsPerPage: 50 })
    const rows = handler.getRows()
    const selected = handler.getSelected()
    const isAllSelected = handler.isAllSelected()

    async function loadPrescriptions() {
        let response = await apiGET(session, "/prescription-requests/");

        if (response && response.ok) {
            prescription_requests = await response.json();
            handler.setRows(prescription_requests)
            console.log(prescription_requests);
        } else {
            return "Server error, please try again later!";
        }
    }
    async function approveRequest() {
        let response = await apiPOST(session, "/prescription-requests/respond_request/", JSON.stringify({prescription_request_ids : $selected, is_approved: true}));
        
        if (response === null) {
            alert("Server error, please try again later!");
            return;
        }

        if (response.ok) {
            loadPrescriptions();
        } else {
            try {
                let response_json = await response.json();
                alert(response_json.message)
            } catch {
                alert("Server error, please try again later!");
            }
        }
    }

    onMount(() => {
        loadPrescriptions();
    })

    let prescriptionSchema = yup.object({
        patient_id: yup.string().required("Please enter a Patient ID"),
        is_repeating: yup.string().required("Please enter a boolean value"),
        medicine: yup.string().required("Enter Medicine"),
        notes: yup.string().required("Enter Notes")
    })

    let patient_id = "";
    let is_repeating = "";
    let medicine = "";
    let notes = "";

    let errors = {};

    $: patient_id_errors = errors.hasOwnProperty("patient_id") ? errors["patient_id"] : [];
    $: is_repeating_errors = errors.hasOwnProperty("is_repeating") ? errors["is_repeating"] : [];
    $: medicine_errors = errors.hasOwnProperty("medicine") ? errors["medicine"] : [];
    $: notes_errors = errors.hasOwnProperty("patient_id") ? errors["notes"] : [];

    let serverError = "";

    async function createPrescription() {
        let PrescData = {
            patient_id: patient_id,
            is_repeating: is_repeating,
            medicine: medicine,
            notes: notes
        }

        try {
            await prescriptionSchema.validate(PrescData, {abortEarly: false});
        } catch (outerErr) {
            errors = {};
            for (let err of outerErr.inner) {
                if (err.path in errors) {
                    errors[err.path].push(err.message);
                } else {
                    errors[err.path] = [err.message];
                }
            }
            return;
        }

        let response;
        let response_json;

        try {
            response = await fetch(`${API_ENDPOINT}/prescriptions/create_prescription/`, {
                method: "POST",
                body: JSON.stringify(PrescData),
                headers: {
                    "content-type": "application/json",
                    "Authorization": `Token ${token}`
                }
            });
            response_json = await response.json();
        } catch(error) {
            return;
        }
        if (response.ok) {
            if (serverError) serverError = "";
            if (errors) errors = {};

            loadPrescriptions();
        } else if (response.status < 500) {
            error = response_json.detail;
        } else {
            error = "Server error, please try again later!"
        }

    }
    // check the form's method and send the fetch accordingly
				
		
	

</script>

<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3, 5]} />

<h2>Create New Prescription</h2>

<div class="d-flex flex-column justify-content-center align-items-center register-container">
    <form class="container" on:submit|preventDefault={createPrescription} novalidate>
        <div class="row mb-2 g-2">
            <div class="col-sm">
                <Field type="text" bind:value={patient_id} errors={patient_id_errors} id="prescription-patientid" label="Patient ID" />
            </div>
            <div class="col-sm">
                <Field type="text" bind:value={is_repeating} errors={is_repeating_errors} id="prescription-isrepeating" label="Repeat Prescription" />
            </div>
        </div>
        <div class="row mb-2">
            <div class="col-sm">
                <Field type="email" bind:value={medicine} errors={medicine_errors} id="prescription-medicine" label="Medicine" />
            </div>
            <div class="col-sm">
                <Field type="email" bind:value={notes} errors={notes_errors} id="prescription-notes" label="Notes" />
            </div>
        </div>
        <div class="row">
            <div class="col">
                <button type="submit" class="btn btn-primary mb-2">Create Prescription</button>
            </div>
        </div>
    </form>
</div>

<h2>Prescription Requests</h2>
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
            <Th {handler} orderBy={row => row.prescription.patient.first_name}>First name</Th>
            <Th {handler} orderBy={row => row.prescription.patient.last_name}>Last Name</Th>
            <Th {handler} orderBy={row => row.prescription.medicine}>Medicine</Th>
            <Th {handler} orderBy={row => row.prescription.notes}>Notes</Th>
            <Th {handler} orderBy={row => row.prescription.is_repeating}>Repeating</Th>
            <Th {handler} orderBy={row => row.is_approved}>Is Approved</Th>
        </tr>
        <tr>
            <th class="selection" />
            <ThFilter
                {handler}
                filterBy={(row) => row.prescription.patient.first_name}
            />
            <ThFilter {handler} filterBy={row => row.prescription.patient.first_name}/>
            <ThFilter {handler} filterBy={row => row.prescription.patient.last_name}/>
            <ThFilter {handler} filterBy={row => row.prescription.medicine}/>
            <ThFilter {handler} filterBy={row => row.prescription.notes}/>
            <ThFilter {handler} filterBy={row => row.prescription.is_repeating}/>
            <ThFilter {handler} filterBy={row => row.is_approved}/>
        </tr>
    </thead>
    <tbody>
        {#each $rows as row}
            <tr>
                <tr class:active={$selected.includes(row.id)}>                    
                        <td class="selection">
                            <input
                                type="checkbox"
                                on:click={() => handler.select(row.id)}
                                checked={$selected.includes(row.id)}
                            />
                        </td>
                <td>{row.prescription.patient.first_name}</td>
                <td>{row.prescription.patient.last_name}</td>
                <td>{row.prescription.medicine}</td>
                <td>{row.prescription.notes}</td>
                <td>{row.prescription.is_repeating}</td>
                <td>{#if row.is_approved}✔️{:else}❌{/if}</td>
            </tr>
        {/each}
    </tbody>
</table>
<button class="btn btn-lg btn-primary float-end" on:click="{approveRequest}" disabled="{$selected.length <= 0}">Approve Prescription</button>