<script>
    import { API_ENDPOINT, BLANK_SESSION, QUICK_SYMPTOMS } from "$lib/constants";
    import { getContext } from "svelte";

    const session = getContext("session");

    let appointments = []

    export async function loadAppointments() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/`, {
                method: "GET",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

        appointments = await response.json();
        console.log(appointments);


        } catch (error) {
            return "Server error, please try again later!";
        }

        
    }

    loadAppointments();

</script>

<div>
    <h2>My Appointments</h2>

    {#each appointments as a, i}
    <div class="card" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">Appointment {i+1}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{a.time_slot <= 1 ? 'Morning' : 'Aftenoon'}</h6>
          <p class="card-text">{a.reason}</p>
        </div>
    </div>
    <br>
    {/each}
    

</div>
