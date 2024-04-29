<script>
    import { getContext } from "svelte";
    import { API_ENDPOINT } from "$lib/constants";
    import AppointmentCard from "$lib/components/AppointmentCard.svelte";

    const session = getContext("session");

    export let title = "Untitled";
    export let stage_id = -1;
    export let staff_id = -1;
    export let patient_id = -1;

    let appointments = [];

    export async function loadAppointments() {
        let url = `${API_ENDPOINT}/appointments?`;

        if (stage_id >= 0) {
            url += `stage_id=${stage_id}&`;
        }

        if (staff_id >= 0) {
            url += `staff_id=${staff_id}&`;
        }

        if (patient_id >= 0) {
            url += `patient_id=${patient_id}&`;
        }

        let response;
        try {
            response = await fetch(url, {
                method: "GET",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

            appointments = await response.json();
            console.log(appointments);
        } catch (error) {
            console.log("Failed to load appointments:", error);
            return "Server error, please try again later!";
        }
    }

    loadAppointments();

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
