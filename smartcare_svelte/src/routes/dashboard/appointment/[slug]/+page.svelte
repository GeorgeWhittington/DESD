<script>
    import { API_ENDPOINT, BLANK_SESSION, QUICK_SYMPTOMS } from "$lib/constants";
    import { getContext } from "svelte";

    const session = getContext("session");

    export let data;
    console.log(data.slug);

    let appointment = {}

    export async function loadAppointment() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/appointments/${data.slug}`, {
                method: "GET",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
            });

        appointment = await response.json();
        console.log(appointment)

        } catch (error) {
            return "Server error, please try again later!";
        }

        
    }

    loadAppointment();
</script>

<div>
    <h2>View Appointment</h2>
    <div class="card">
       
        <div class="card-body">
            <h5 class="card-title">
                This is some text within a card body.
            </h5>
          This is some text within a card body.
        </div>
      </div>
</div>
