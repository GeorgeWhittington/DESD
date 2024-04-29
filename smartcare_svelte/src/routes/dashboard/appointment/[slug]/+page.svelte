<script>
    import {
        API_ENDPOINT,
        BLANK_SESSION,
        QUICK_SYMPTOMS,
        TIME_PREFERENCE,
        APPOINTMENT_STAGE
    } from "$lib/constants";
    import { onMount, getContext } from "svelte";

    const session = getContext("session");

    export let data;
    console.log(data.slug);

    let appointment = {};
    let patient = {};
    let staff = {};
    let comments = [];

    onMount(async () => {
        try {
            let response = await fetch(
                `${API_ENDPOINT}/appointments/${data.slug}`,
                {
                    method: "GET",
                    headers: {
                        Authorization: `Token ${$session.token}`,
                        "content-type": "application/json",
                    },
                },
            );

            appointment = await response.json();
            patient = appointment.patient;
            staff = appointment.staff;
            comments = appointment.appointment_comments;
            console.log(appointment);
            console.log(staff)
            console.log();
        } catch (error) {
            return "Server error, please try again later!";
        }
    });

    export async function beginAppointment() {
        let response;
        console.log("begin appointment!!")
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/${appointment.id}/begin/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                }
            });

            console.log(response.text())
            location.reload();

        } catch (error) {
            return "Server error, please try again later!";
        }
    }

    export async function endAppointment() {
        let response;
        console.log("end appointment!!")
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/${appointment.id}/end/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                }
            });

            console.log(response.text())
            location.reload();
            
        } catch (error) {
            return "Server error, please try again later!";
        }
    }

    export async function assignToCurrentUser() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/${appointment.id}/assign_to_current_user/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                }
            });

            console.log(response.text())
            location.reload();

        } catch (error) {
            return "Server error, please try again later!";
        }
    }


    export async function postNewComment() {
        let response;

        let req_body = { appointment_id: appointment.id, text: txtNewComment };

        try {
            response = await fetch(`${API_ENDPOINT}/appointment_comments/`, {
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

    let txtNewComment = "";

    let isStaff = $session.userType == 2 || $session.userType == 3;
</script>

<div>
    <h2>View Appointment</h2>

    <br />

    <div class="card">
        <div class="card-body">
            <p class="card-text">
                <b>Created:&nbsp;</b>{new Date(appointment.date_created).toUTCString()} <br />
                <b>Stage:&nbsp;</b>{APPOINTMENT_STAGE[appointment.stage]}
            </p>
        </div>
    </div>

    <br />

    <div class="container-fluid g-0">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-header">Patient</div>
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
                    <div class="card-header">Staff</div>
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

    <!-- Staff Actions -->
    {#if isStaff}
        <div class="card">
            <div class="card-header">Staff Actions</div>
            <div class="card-body">
                
                <button type="submit" class="btn btn-sm btn-primary" on:click={assignToCurrentUser}
                        >Assign to current user</button
                    >

                <!-- Begin Appointment -->
                {#if !appointment.actual_start_time && !appointment.actual_end_time}
                <button type="submit" class="btn btn-sm btn-primary" on:click={beginAppointment}
                        >Start Appointment</button
                    >
                {/if}

                <!-- End Appointment -->
                {#if appointment.actual_start_time && !appointment.actual_end_time}
                <button type="submit" class="btn btn-sm btn-primary" on:click={endAppointment}
                        >End Appointment</button
                    >
                {/if}

            </div>
        </div>
    {/if}

    <br />

    <!-- Original Request -->
    <div class="card">
        <div class="card-header">Request</div>
        <div class="card-body">
            <p class="card-text">
                <b>Requested For:&nbsp;</b>{TIME_PREFERENCE[
                    appointment.time_preference
                ]} of {appointment.date_requested}<br />
                <b>Symptom Duration:&nbsp;</b>{appointment.symptom_duration} day(s)
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
            {/each}

            <!-- Comment Box -->
            <br />
            <form on:submit|preventDefault={postNewComment}>
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
