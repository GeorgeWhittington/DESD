<script>
    import {
        API_ENDPOINT,
        BLANK_SESSION,
        QUICK_SYMPTOMS,
        TIME_PREFERENCE,
        APPOINTMENT_STAGE,
        APPOINTMENT_STAGE_COLOURS
    } from "$lib/constants";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import { onMount, getContext } from "svelte";
    import { apiGET, apiPOST } from "$lib/apiFetch.js";

    const session = getContext("session");

    export let data;

    let appointment = {};
    let patient = {};
    let staff = {};
    let comments = [];

    // modals
    let modalManualSchedule = false;

    onMount(async () => {
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
    });

    async function approveAppointment() {
        let response = await apiPOST(session, `/appointments/${appointment.id}/approve/`, "");

        if (response && response.ok) {
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }

    async function rejectAppointment() {
        let response = await apiPOST(session, `/appointments/${appointment.id}/reject/`, "");

        if (response && response.ok) {
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }

    async function beginAppointment() {
        let response = await apiPOST(session, `/appointments/${appointment.id}/begin/`, "");

        if (response && response.ok) {
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }

    async function endAppointment() {
        let response = await apiPOST(session, `/appointments/${appointment.id}/end/`, "");

        if (response && response.ok) {
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }

    async function assignToCurrentUser() {
        let response = await apiPOST(session, `/appointments/${appointment.id}/assign_to_current_user/`, "");

        if (response && response.ok) {
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }

    async function showManualScheduleModal() {
        modalManualSchedule = true;
    }

    async function doAppointmentAction(name) {
        let response = await apiPOST($session, `/appointments/${appointment.id}/${name}/`, "");

        if (response && response.ok) {
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
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
            console.log(response.text())
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }

    let txtNewComment = "";

    let isStaff = $session.userType == 2 || $session.userType == 3;
</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3, 5]} />

<div>
    <h2>View Appointment</h2>

    <br />

    <div class="card">
        <div class="card-body">
            <p class="card-text">
                <span class="badge" style="background-color: {APPOINTMENT_STAGE_COLOURS[appointment.stage]};">{APPOINTMENT_STAGE[appointment.stage]}</span> <br />
                <i class="bi bi-calendar pe-2"></i><b>Created:&nbsp;</b>{new Date(appointment.date_created).toUTCString()} <br />

                {#if appointment.assigned_start_time}
                    <i class="bi bi-calendar pe-2"></i><b>Scheduled For:&nbsp;</b>{new Date(appointment.assigned_start_time).toUTCString()} <br />
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
    {#if isStaff}
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
                <button type="submit" class="btn btn-primary"
                        >Automatically Schedule</button
                    >

                <button type="submit" class="btn btn-primary" on:click={showManualScheduleModal}
                        >Manual Schedule</button
                    >
                {/if}
                

                <!-- Begin Appointment -->
                {#if appointment.stage === 2 && !appointment.actual_start_time && !appointment.actual_end_time}
                <button type="submit" class="btn btn-primary " on:click={() => doAppointmentAction("begin")}
                        >Start Appointment</button
                    >
                
                <button type="submit" class="btn btn-warning" on:click={() => doAppointmentAction("unschedule")}
                    >Reschedule</button
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
                        >[{new Date(c.created_time).toUTCString()}]</span
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


<!-- Modals -->
{#if modalManualSchedule }
<div class="modal" id="onload" tabindex="-1" role="dialog" style="display: block;">
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">Manual Schedule</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <form>
                <div class="mb-3">
        
                    <!-- Date -->
        
                    <div class="mb-3">
                        <label for="txtDate" class="form-label">Date</label>
                        <input type="date" id="txtDate" class="form-control" bind:value={date_requested}>
                    </div>
                    </div>
            </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
        </div>
        </div>
    </div>
</div>
{/if}

  