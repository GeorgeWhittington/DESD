<script>
    import { getContext, onMount } from "svelte";
    import { API_ENDPOINT } from "$lib/constants";
    import { apiGET } from "$lib/apiFetch.js";
    import AppointmentCard from "$lib/components/AppointmentCard.svelte";

    const session = getContext("session");

    export let title = "Untitled";
    export let stage_id = -1;
    export let staff_id = -1;
    export let patient_id = -1;

    let appointments = [];

    async function loadAppointments() {
        let endpoint = "/appointments?";

        if (stage_id >= 0) {
            endpoint += `stage_id=${stage_id}&`;
        }

        if (staff_id >= 0) {
            endpoint += `staff_id=${staff_id}&`;
        }

        if (patient_id >= 0) {
            endpoint += `patient_id=${patient_id}&`;
        }

        let response = await apiGET($session, endpoint, "");

        if (response && response.ok) {
            appointments = await response.json();
            console.log(appointments);
        } else {
            console.log("Failed to load appointments");
            return "Server error, please try again later!";
        }
    }

    onMount(() => {
        loadAppointments();
    })

</script>



<div class="card">
    <div class="card-header">
        {title}  ({appointments.length})
    </div>
    <div class="card-body d-flex flex-wrap justify-content-between">
        {#each appointments as a, i }
        <AppointmentCard appointment={a}></AppointmentCard>
    {/each}
    </div>
</div>
