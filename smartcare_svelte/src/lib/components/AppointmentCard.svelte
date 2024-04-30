<script>
    import { TIME_PREFERENCE, APPOINTMENT_STAGE, APPOINTMENT_STAGE_COLOURS } from "$lib/constants";
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
      <span class="card-title"><b>{appointment.patient.first_name} {appointment.patient.last_name}</b><span class="badge float-end" style="background-color: {APPOINTMENT_STAGE_COLOURS[appointment.stage]};">{APPOINTMENT_STAGE[appointment.stage]}</span></span>
      
      {#if appointment.assigned_start_time}

      <br>
      <span class="card-subtitle mb-2 text-muted">Scheduled For:  {new Date(appointment.assigned_start_time).toLocaleString("en-GB")}</span>

      {:else}
      <br>
      <span class="card-subtitle mb-2 text-muted">Created:  {new Date(appointment.date_created).toLocaleString("en-GB")}</span>
      
      <br>
      <span class="card-subtitle mb-2 text-muted">Requested For:  {appointment.date_requested} ({TIME_PREFERENCE[appointment.time_preference]})</span>
      {/if}

      {#if appointment.staff}
        <br>
        <span class="card-subtitle mb-2 text-muted">Assigned To: {appointment.staff.first_name} {appointment.staff.last_name}</span>
      {/if}

      <br>
      <span class="card-subtitle mb-2 text-muted">Symptom Duration: {appointment.symptom_duration} days</span>

      <br>
      <span class="card-subtitle mb-2 text-muted">Symptoms:</span>
      <br>
      <textarea class="form-control" style="resize:none; padding:4px; border: none;" readonly disabled
      rows="3">{appointment.symptoms}</textarea>
    </div>
</div>