<script>
  import { onMount } from "svelte";
  import { bootstrapThemes } from "$lib/constants.js";
  import { getContext } from "svelte";
  import { BLANK_SESSION } from "$lib/constants";
  import { apiPOST } from "$lib/apiFetch.js";

  let openingHours = [
    { day: 'Monday', open: '8:00 AM', close: '6:00 PM' },
    { day: 'Tuesday', open: '8:00 AM', close: '6:00 PM' },
    { day: 'Wednesday', open: '8:00 AM', close: '6:00 PM' },
    { day: 'Thursday', open: '8:00 AM', close: '6:00 PM' },
    { day: 'Friday', open: '8:00 AM', close: '6:00 PM' },
    { day: 'Saturday', open: '8:00 AM', close: '6:00 PM' },
    { day: 'Sunday', open: '8:00 AM', close: '6:00 PM' }
  ];

  let contactMethod = [
    { header: 'Phone', value: '01189395643' },
    { header: 'Email', value: 'SmartcareSurgery@gmail.com' },
    { header: 'Address', value: '123 Bristol Rd., Bristol, BR127OL ' },
    { header: 'Out of hours', value: '111' }
  ];
</script>

<div class="container-fluid d-flex flex-column vh-100 justify-content-between">
  <header class="row">
     <div class="col text-center">
        <h1 class="my-4">Welcome to Smartcare Surgery</h1>
     </div>
  </header>

  <div class="row flex-grow-1 align-items-center justify-content-around">
     <div class="col-md-6 mb-3 mb-md-0 d-flex flex-column justify-content-center text-center"style="min-width: 300px;">
        <h2 class="mt-4">About us</h2>
        <p>We are a general practitioner business based in Bristol and dedicated to your health. Our team uses the latest techniques and technology to ensure the best outcomes, helping you return to your daily life with confidence.</p>
        <h2 class="mt-4">Opening hours</h2>
        <table class="table">
           <thead>
              <tr>
                 <th>Day</th>
                 <th>Opening Time</th>
                 <th>Closing Time</th>
              </tr>
           </thead>
           <tbody>
              {#each openingHours as hour}
              <tr>
                 <td>{hour.day}</td>
                 <td>{hour.open}</td>
                 <td>{hour.close}</td>
              </tr>
              {/each}
           </tbody>
        </table>
        <h2 class="mt-4">Contact us</h2>
        <table class="table">
           {#each contactMethod as row}
           <tr>
              <td><strong>{row.header}</strong></td>
              <td>{row.value}</td>
           </tr>
           {/each}
        </table>
        <div class="card mt-4">
           <div class="card-body">
              <div>
                 <h6>For life-threatening emergencies, dial 999.</h6>
                 <p>This includes severe bleeding, difficulty breathing, or unconsciousness. Immediate help is required in these cases.</p>
                 <h6>For non-emergency medical advice, dial 111.</h6>
                 <p>This service is available for situations where medical guidance is needed quickly but it is not a life-threatening emergency. NHS 111 can also direct you to the best local service that can provide the care you need.</p>
              </div>
           </div>
        </div>
     </div>
     <div class="col-md-6 d-flex flex-column justify-content-center text-center" style="min-width: 300px;">
        <img src="https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="image of man in blue scrubs smiling.royalty free, found at Unsplash" >
     </div>
  </div>
</div>

<style>
  header, footer {
    flex-shrink: 0;
  }
</style>