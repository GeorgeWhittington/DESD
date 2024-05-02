<script>
    import {
        API_ENDPOINT,
        BLANK_SESSION,
        QUICK_SYMPTOMS,
        TIME_PREFERENCE,
        APPOINTMENT_STAGE,
        APPOINTMENT_STAGE_COLOURS
    } from "$lib/constants";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import { onMount, getContext } from "svelte";
    import { apiGET, apiPOST } from "$lib/apiFetch.js";
    import { mid_appointment } from "$lib/constants.js";
    import { writable } from "svelte/store";

    const session = getContext("session");

    export let data;

    let appointment = {};
    let patient = {};
    let staff = {};
    let comments = [];
    let time_preference;
    let date_requested = new Date().toISOString().slice(0, 10);
    let alertText = "";
    let alertType = "primary"

    const staff_members = writable([{id: "any", text: "No Preference"}]);
    let selected_staff_member = "any";

    // modals
    let manualScheduleDate = new Date().toISOString().slice(0, 10);
    
    onMount(async () => {
        loadAppointmentData();
        loadStaffMembers();
    });

    async function loadAppointmentData() {
        let response = await apiGET(session, `/appointments/${data.slug}/`);
        if (response && response.ok) {
            appointment = await response.json();
            patient = appointment.patient;
            staff = appointment.staff;
            comments = appointment.appointment_comments;
            console.log(appointment);
            console.log(staff)
            console.log();
        } else {
            return "Server error, please try again later!";
        }
    };

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

    async function doAppointmentAction(name) {
        let response = await apiPOST(session, `/appointments/${appointment.id}/${name}/`, "");

        let json = await response?.json();
        alertText = json["message"];
        alertType = json["result"] ? "primary" : "danger";

        if (response && response.ok) {
            console.log(response.text())
            
        } else {
            return "Server error, please try again later!";
        }
        loadAppointmentData();
    }

    async function appointmentScheduleManually() {
        let data = {
            time_preference: time_preference,
            date_requested: date_requested
        }
        if (selected_staff_member != "any") {
            data["staff_preference_id"] = selected_staff_member;
        }

        console.log(data);

        let response = await apiPOST(session, `/appointments/${appointment.id}/schedule_manually/`, JSON.stringify(data));
        let json = await response?.json();
        alertText = json["message"];
        alertType = json["result"] ? "primary" : "danger";
        location.reload();
    }

    async function addAppointmentComment() {
        if (!txtNewComment || txtNewComment.length == 0) {
            return;
        }

        let response = await apiPOST(
            session, `/appointments/${appointment.id}/add_comment/`,
            JSON.stringify({comment : txtNewComment})
        );

        if (response && response.ok) {
            alertText = response.json["message"];
            loadAppointmentData();
        } else {
            alertText = "An error occured with your request";
            alertType = "danger";
            return "Server error, please try again later!";
        }
        
    }

    let txtNewComment = "";

    let isStaff = $session.userType == 2 || $session.userType == 3;
</script>

<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3, 5]} />

<div>
    <h2>View Appointment</h2>
    <br>

    {#if alertText.length > 0}
    <div class="alert alert-{alertType}" role="alert">
        {alertText}
    </div>
    {/if}

    <br />

    <div class="card">
        <div class="card-body">
            <p class="card-text">
                <span class="badge" style="background-color: {APPOINTMENT_STAGE_COLOURS[appointment.stage]};">{APPOINTMENT_STAGE[appointment.stage]}</span> <br />
                <i class="bi bi-calendar pe-2"></i><b>Created:&nbsp;</b>{new Date(appointment.date_created).toString()} <br />

                {#if appointment.assigned_start_time}
                    <i class="bi bi-calendar pe-2"></i><b>Scheduled For:&nbsp;</b>{new Date(appointment.assigned_start_time).toString()} <br />
                {/if}
            </p>
        </div>
    </div>

    <br />

    <div class="container-fluid g-0">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-header"><i class="bi bi-person-fill pe-2"></i>Patient</div>
                    <div class="card-body">
                        <p class="card-text">
                            <b>Name:&nbsp;</b>{patient.first_name}
                            {patient.last_name} <br />
                            <b>Email Address:&nbsp;</b>{patient.email}
                        </p>
                    </div>
                </div>
            </div>

            <div class="col">
                <div class="card">
                    <div class="card-header"><i class="bi bi-person-fill pe-2"></i>Staff</div>
                    <div class="card-body">
                        {#if !appointment.staff}
                        <p class="card-text">Not assigned to any staff.</p>
                        {:else}
                        <p class="card-text">
                            <b>Name:&nbsp;</b>{appointment.staff.first_name}
                            {appointment.staff.last_name} <br />
                            <b>Email Address:&nbsp;</b>{appointment.staff.email}
                        </p>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <br />

    <!-- Actions -->
    {#if isStaff && appointment.stage <= 2}
        <div class="card">
            <div class="card-header">Actions</div>
            <div class="card-body">
                
                <!-- Requested Stage -->
                {#if appointment.stage === 0 }
                <button type="submit" class="btn btn-primary" on:click={() => doAppointmentAction("approve")}>Approve</button>
                <button type="submit" class="btn btn-danger"  on:click={() => doAppointmentAction("reject")}>Reject</button>
                {/if}

                <!-- Approved Stage -->
                {#if appointment.stage === 1 }
                <button type="submit" class="btn btn-primary" on:click={() => doAppointmentAction("schedule_automatically")}
                        >Schedule Automatically</button
                    >
                    <br>
                    <br>
                <!-- Manual Schedule form -->
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Schedule Manually</h5>
                        <form on:submit|preventDefault={appointmentScheduleManually}>
                            <div class="mb-3">
                                <label for="select-preferred-doctor" class="form-label">Staff Member</label>
                                <select 
                                    class="form-select" id="select-preferred-doctor" aria-label="Select preferred staff member"
                                    bind:value={selected_staff_member}
                                >
                                {#each $staff_members as staff_member}
                                    <option value="{staff_member.id}">{staff_member.text}</option>
                                {/each}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="txtDate" class="form-label">Date</label>
                                <input type="date" id="txtDate" class="form-control" bind:value={date_requested}>
                            </div>
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
                            <button type="submit" class="btn btn-primary">Schedule</button>
                          </form>
                    </div>
                  </div>
                

                {/if}
                

                <!-- Begin Appointment -->
                {#if appointment.stage === 2 && !appointment.actual_start_time && !appointment.actual_end_time}
                <button type="submit" class="btn btn-primary " on:click={() => doAppointmentAction("begin")}
                        >Start Appointment</button
                    >

                <button type="submit" class="btn btn-danger float-end" on:click={() => doAppointmentAction("unschedule")}
                    >Unschedule</button
                >
                {/if}

                <!-- End Appointment -->
                {#if appointment.actual_start_time && !appointment.actual_end_time}
                <button type="submit" class="btn btn-primary"  on:click={() => doAppointmentAction("end")}
                        >End Appointment</button
                    >
                {/if}

            </div>
        </div>
        <br />
    {/if}

    

    <!-- Original Request -->
    <div class="card">
        <div class="card-header">Request</div>
        <div class="card-body">
            <p class="card-text">
                <i class="bi bi-calendar pe-2"></i><b>Requested For:&nbsp;</b>{TIME_PREFERENCE[
                    appointment.time_preference
                ]} of {appointment.date_requested}<br />
                <i class="bi bi-clock-fill pe-2"></i><b>Symptom Duration:&nbsp;</b>{appointment.symptom_duration} day(s)
            </p>
            <textarea class="form-control" rows="3" readonly="1"
                >{appointment.symptoms}</textarea
            >
        </div>
    </div>

    <br />

    <!-- Prescriptions -->

    <div class="card">
        <div class="card-header">Related Prescriptions (0)</div>
        <div class="card-body">
            <p class="card-text">No related prescriptions</p>
        </div>
    </div>

    <br />

    <!-- Posts -->

    <div class="card">
        <div class="card-header">Messages</div>
        <div class="card-body">
            {#each comments as c}
                <div>
                    <b
                        >{c.created_by.first_name}
                        {c.created_by.last_name} ({c.created_by.id == appointment.patient.id ? 'Patient' : 'Staff'})</b
                    ><br />
                    <span class="text-muted small"
                        >[{new Date(c.created_time).toString()}]</span
                    >
                    <div>{c.text}</div>
                </div>
                <u></u>
                <hr>
            {/each}

            <!-- Comment Box -->
            <br />
            <form on:submit|preventDefault={addAppointmentComment}>
                <div class="mb-3">
                    <textarea
                        class="form-control"
                        rows="3"
                        bind:value={txtNewComment}
                    ></textarea>
                    <button type="submit" class="btn btn-sm btn-primary"
                        >Send</button
                    >
                </div>
            </form>
        </div>
    </div>
</div>
  