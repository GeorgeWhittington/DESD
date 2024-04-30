<script>
    import { TIME_PREFERENCE, APPOINTMENT_STAGE } from "$lib/constants";
    import { API_ENDPOINT } from "$lib/constants";
    import { getContext } from "svelte";
    import { apiPOST } from "$lib/apiFetch.js";
    export let appointment;

    const session = getContext("session");

    async function approveRequest(id) {
        let response = await apiPOST($session, `/appointments/${id}/approve/`, "");
        if (response && response.ok) {
            console.log(response.text())
        } else {
            return "Server error, please try again later!";
        }
    }

    async function rejectRequest(id) {
        let response = await apiPOST($session, `/appointments/${id}/reject/`, "");
        if (response && response.ok) {
            console.log(response.text())
        } else {
            return "Server error, please try again later!";
        }
    }

    function cardClicked() {
       window.open(`/dashboard/appointment/${appointment.id}`, "_blank");
    }

</script>

<style>
    .appointment-card:hover {
        cursor: pointer;
        box-shadow:  0 8px 16px 0 rgba(0, 0, 0, 0.2);
    }
</style>

<div class="card mb-3 appointment-card" style="width: 24rem;" >
    <div class="card-body" on:click={cardClicked}>
      <h5 class="card-title">{appointment.patient.first_name} {appointment.patient.last_name}</h5>
      <h6 class="card-subtitle mb-2 text-muted">Created:  {new Date(appointment.date_created).toUTCString()}</h6>
      <h6 class="card-subtitle mb-2 text-muted">Requested For:  {appointment.date_requested} ({TIME_PREFERENCE[appointment.time_preference]})</h6>

      {#if appointment.staff}
        <h6 class="card-subtitle mb-2 text-muted">Requested For:  {appointment.date_requested} ({TIME_PREFERENCE[appointment.time_preference]})</h6>
      {/if}
      <p class="card-text">{appointment.symptoms}</p>
    </div>
</div>