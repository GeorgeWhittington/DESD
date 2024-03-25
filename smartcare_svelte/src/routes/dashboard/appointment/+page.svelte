<script>
    import { API_ENDPOINT, BLANK_SESSION } from "$lib/constants";
    import { getContext } from "svelte";

    const session = getContext("session");

    let notes;
    let time_slot;

    export async function requestAppointment() {
        let response;

        let req_body = {'notes': notes, 'time_slot' : time_slot};

        try {
            response = await fetch(`${API_ENDPOINT}/appointments/`, {
                method: "POST",
                headers: {
                    "Authorization": `Token ${$session.token}`,
                    "content-type": "application/json"
                },
                body: JSON.stringify(req_body)
            });
        } catch (error) {
            return "Server error, please try again later!";
        }
        
    }

</script>

<div>
    <form on:submit|preventDefault={requestAppointment}>
    <div class="mb-3">
        <!-- Time Slot -->
        <div class="mb-3">
            <label for="selTimeSlot" class="form-label">Time Slot</label>
            <select
                class="form-select"
                id="selTimeSlot"
                aria-label="Default select example"
                bind:value={time_slot}
            >
                <option value="1" selected>Morning</option>
                <option value="2">Afternoon</option>

            </select>
        </div>
    </div>

    <!-- Notes -->
    <div class="mb-3">
        <label for="txtNotes" class="form-label">Notes</label>
        <textarea class="form-control" id="txtNotes" rows="3" bind:value={notes}></textarea>
    </div>

    <!-- Submit Button -->
    <button type="submit" class="btn btn-primary">
        Submit
    </button>
</form>

</div>
