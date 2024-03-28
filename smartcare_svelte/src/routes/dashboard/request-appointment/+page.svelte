<script>
    import { API_ENDPOINT, BLANK_SESSION, QUICK_SYMPTOMS } from "$lib/constants";
    import { getContext } from "svelte";
    import QuickSymptomSelect from "$lib/components/QuickSymptomSelect.svelte";
    import { goto } from '$app/navigation';

    const session = getContext("session");

    let reason = "";
    let reasonElement;
    let time_slot;
    let symptom_duration = 1;

    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' });
     }; 
  
    function quickSymptomClicked(event) {
        if (reason.length > 0) {
            reason += "\n";
        }
        reason += event.detail.text;
        scrollToBottom(reasonElement);
    }

    export async function requestAppointment() {
        let response;

        let req_body = { reason: reason, time_slot: time_slot, symptom_duration : symptom_duration };

        try {
            response = await fetch(`${API_ENDPOINT}/appointments/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
                body: JSON.stringify(req_body),
            });

            goto('/dashboard/appointments');
            
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

        
        <QuickSymptomSelect on:symptomClicked={quickSymptomClicked}></QuickSymptomSelect>

        <!-- Reason -->
        <div class="mb-3">
            <label for="txtNotes" class="form-label"
                >Describe Symptoms</label
            >
            <textarea bind:this={reasonElement}
                class="form-control"
                id="txtNotes"
                rows="6"
                bind:value={reason}
            ></textarea>
        </div>

        <!-- Symptom Duration -->
        <div class="mb-3">

            <label for="txtSymptomDuration" class="form-label"
                >Duration of symptoms</label>

            <div class="input-group mb-3">
                
            
            <input type="number" class="form-control" id="txtSymptomDuration" bind:value={symptom_duration}>

            <select
                    class="form-select"
                    id="selSymptomDuration"
                >
                    <option value="0" selected>Hours</option>
                    <option value="1" selected>Days</option>
                    <option value="2">Months</option>
                </select>

              </div>

            

            
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary"> Submit </button>
    </form>
</div>
