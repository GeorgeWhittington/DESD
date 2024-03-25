<script>
    import { API_ENDPOINT, BLANK_SESSION, QUICK_SYMPTOMS } from "$lib/constants";
    import { getContext } from "svelte";

    const session = getContext("session");

    let reason;
    let time_slot;

    export async function requestAppointment() {
        let response;

        let req_body = { reason: reason, time_slot: time_slot };

        try {
            response = await fetch(`${API_ENDPOINT}/appointments/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
                body: JSON.stringify(req_body),
            });
        } catch (error) {
            return "Server error, please try again later!";
        }
    }
</script>

<div>
    <h2>Request Appointment</h2>

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
                    <option value="0" selected>Morning</option>
                    <option value="2">Afternoon</option>
                </select>
            </div>
        </div>

        <div class="card mb-2">
            <div class="card-body">
                <label class="card-title">Quick-Add Symptoms</label>

                <ul class="nav nav-tabs" id="myTab" role="tablist">
                {#each Object.entries(QUICK_SYMPTOMS) as [qs]}
                <li class="nav-item" role="presentation">
                    <button
                        class="nav-link active"
                        id={qs+"-tab"}
                        data-bs-toggle="tab"
                        data-bs-target={"#" + qs}
                        type="button"
                        role="tab"
                        aria-controls={qs}
                        aria-selected="true">{qs}</button
                    >
                </li>
                {/each}
                </ul>
                <div class="tab-content" id="myTabContent">
                    {#each Object.entries(QUICK_SYMPTOMS) as [qs]}

                    <div
                        class="tab-pane fade"
                        id={qs}
                        role="tabpanel"
                        aria-labelledby={qs+"-tab"}
                    >
                        hi
                        {#each Object.entries(qs) as [symptom]}
                            <p>{symptom}</p>
                            hi
                        {/each}
                    </div>
                    {/each}
                </div>
            </div>
        </div>

        <!-- Reason -->
        <div class="mb-3">
            <label for="txtNotes" class="form-label"
                >Reason for appointment</label
            >
            <textarea
                class="form-control"
                id="txtNotes"
                rows="3"
                bind:value={reason}
            ></textarea>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary"> Submit </button>
    </form>
</div>
