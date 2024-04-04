<script>
    import { TIME_PREFERENCE, APPOINTMENT_STAGE } from "$lib/constants";
    import { API_ENDPOINT } from "$lib/constants";
    import { getContext } from "svelte";
    export let appointment;

    const session = getContext("session");

    export async function approveRequest(id) {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/${id}/approve/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

            console.log(response.text())

        } catch (error) {
            console.log("Failed to load appointments:", error);
            return "Server error, please try again later!";
        }
    }

    export async function rejectRequest(id) {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/${id}/reject/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

            console.log(response.text())

        } catch (error) {
            console.log("Failed to load appointments:", error);
            return "Server error, please try again later!";
        }
    }


</script>

<div class="card" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">{appointment.patient.first_name} {appointment.patient.last_name}</h5>
      <h6 class="card-subtitle mb-2 text-muted">Requested for {TIME_PREFERENCE[appointment.time_preference]}</h6>
      <p class="card-text">{appointment.symptoms}</p>
      <p class="card-text">{APPOINTMENT_STAGE[appointment.stage]}</p>
      <button class='btn btn-sm btn-primary' on:click={approveRequest(appointment.id)}>Approve</button>
      <button class='btn btn-sm btn-secondary' on:click={rejectRequest(appointment.id)}>Reject</button>
    </div>
</div>