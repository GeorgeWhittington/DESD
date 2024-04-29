<script>
    import {
        API_ENDPOINT,
        BLANK_SESSION,
        QUICK_SYMPTOMS,
        TIME_PREFERENCE,
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
            console.log();
        } catch (error) {
            return "Server error, please try again later!";
        }
    });

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

</script>

<div>
    <h2>View Appointment</h2>

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
                        <p class="card-text">Not assigned to any staff.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <br />

    <!-- Original Request -->
    <div class="card">
        <div class="card-header">Request</div>
        <div class="card-body">
            <p class="card-text">
                <b>Requested:&nbsp;</b>{TIME_PREFERENCE[
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
                    <b>{c.created_by.first_name} {c.created_by.last_name} (Patient)</b><br
                    />
                    <span class="text-muted small"
                        >[{new Date(c.created_time).toUTCString()}]</span
                    >
                    <div>{c.text}</div>
                
                </div>
                <u></u>
            {/each}

            <!-- Comment Box -->
            <br>
    <form on:submit|preventDefault={postNewComment}>
        <div class="mb-3">
            <textarea class="form-control" rows="3" bind:value={txtNewComment}
                ></textarea
            >
            <button type="submit" class="btn btn-sm btn-primary">Send</button>
        </div>
    </form>

        </div>
    </div>
    
</div>
