<script>
    import { getContext } from "svelte";
    import { API_ENDPOINT } from "$lib/constants";
    import AppointmentCard  from "$lib/components/AppointmentCard.svelte";

    const session = getContext("session");

    let openAppointments = []

    export async function loadOpenAppointments() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/`, {
                method: "GET",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

        openAppointments = await response.json();
        console.log(openAppointments);


        } catch (error) {
            console.log("Failed to load appointments:", error);
            return "Server error, please try again later!";
        }
    }

    loadOpenAppointments();

</script>

<div>
    <h2>Staff Dashboard</h2>

    <b>Appointments that need to be approved</b>

    {#each openAppointments as a, i }
        <AppointmentCard appointment=a></AppointmentCard>                    
    {/each}
    
</div>
