<script>
    import { API_ENDPOINT, BLANK_SESSION, QUICK_SYMPTOMS } from "$lib/constants";
    import { getContext, onMount } from "svelte";
    import QuickSymptomSelect from "$lib/components/QuickSymptomSelect.svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import { apiPOST, apiGET } from "$lib/apiFetch.js";
    import { goto } from '$app/navigation';
    import { writable } from "svelte/store";

    const session = getContext("session");

    const staff_members = writable([{id: "any", text: "No Preference"}]);
    let selected_staff_member = "any";

    let symptoms = "";
    let symptomsElement;
    let time_preference;
    let symptom_duration = 1;
    let date_requested = new Date().toISOString().slice(0, 10);

    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' });
     };

    function quickSymptomClicked(event) {
        if (symptoms.length > 0) {
            symptoms += "\n";
        }
        symptoms += event.detail.text;
        scrollToBottom(symptomsElement);
    }

    async function loadStaffMembers() {
        let response = await apiGET(session, "/auth/user/staff/");

        if (response && response.ok) {
            try {
                let response_json = await response.json();
                for (const staff_member of response_json) {
                    staff_members.update((value) => [
                        ...value,
                        {id: staff_member.id, text: `${staff_member.first_name} ${staff_member.last_name}`}
                    ]);
                }
            } catch {
            }
        }
        // No need to notify user if staff list can't be fetched, the *any* option is still available
    }

    async function requestAppointment() {
        let data = {
            symptoms: symptoms, time_preference: time_preference,
            symptom_duration: symptom_duration,
            date_requested: date_requested
        }
        if (selected_staff_member != "any") {
            data["staff_preference_id"] = selected_staff_member;
        }

        console.log(data);

        let response = await apiPOST(session, "/appointments/", JSON.stringify(data));

        if (response && response.ok) {
            let new_appointment = await response.json();
            console.log('New Appointment = ', new_appointment);
            goto(`/dashboard/appointment/${new_appointment.id}`);
        } else {
            return "Server error, please try again later!";
        }
    }

    onMount(() => {
        loadStaffMembers();
    })
</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[5]} />

<div>
    <h2>Request Appointment</h2>

    <form on:submit|preventDefault={requestAppointment}>
        <div class="mb-3">

            <!-- Date -->

            <div class="mb-3">
                <label for="txtDate" class="form-label">Date</label>
                <input type="date" id="txtDate" class="form-control" bind:value={date_requested}>
            </div>

            <!-- Time Slot -->
            <div class="mb-3">
                <label for="selTimeSlot" class="form-label">Time Slot</label>
                <select
                    class="form-select"
                    id="selTimeSlot"
                    aria-label="Select time slot"
                    bind:value={time_preference}
                >
                    <option value="0" selected>Morning</option>
                    <option value="2">Afternoon</option>
                </select>
            </div>

            <!-- Preferred Staff Member -->
            <div class="mb-3">
                <label for="select-preferred-doctor" class="form-label">Preferred Staff Member</label>
                <select 
                    class="form-select" id="select-preferred-doctor" aria-label="Select preferred staff member"
                    bind:value={selected_staff_member}
                >
                {#each $staff_members as staff_member}
                    <option value="{staff_member.id}">{staff_member.text}</option>
                {/each}
                </select>
            </div>
        </div>

        <QuickSymptomSelect on:symptomClicked={quickSymptomClicked}></QuickSymptomSelect>

        <!-- Reason -->
        <div class="mb-3">
            <label for="txtNotes" class="form-label"
                >Describe Symptoms</label
            >
            <textarea bind:this={symptomsElement}
                class="form-control"
                id="txtNotes"
                rows="6"
                bind:value={symptoms}
            ></textarea>
        </div>

        <!-- Symptom Duration -->
        <div class="mb-3">

            <label for="txtSymptomDuration" class="form-label"
                >Duration of symptoms</label>

            <div class="input-group mb-3">

            <input type="number" class="form-control" id="txtSymptomDuration" bind:value={symptom_duration}>

            <select disabled
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
