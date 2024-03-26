<script>
    import { onMount } from 'svelte';
    import FullCalendar from 'svelte-fullcalendar';
    import daygridPlugin from '@fullcalendar/daygrid';
    let options = {initialView: 'dayGridMonth', plugins: [daygridPlugin]}

</script>
  

<div class="container mt-4">
    <h2>Schedule</h2>
    <div class="card">
        <div class="card-body">
            <div class="form-group">
                <p> Calendar</p>
            
            </div>
        </div>
    </div>
</div>



<div class="container mt-4">
    <div class="row">
        <div class="col">

            <h2>Appointments</h2>
    
            <div class="card">
                <div class="card-body">
    
                    <!-- <button class="btn btn-primary" on:click={createAppointment}>
                        Create Appointment
                    </button> -->
    
                    <!-- <form on:submit|preventDefault={updateWorkingHours}> -->
                        
                        <div class="card mt-3">
                            <div class="card-body">
            
                                <p>Appointment details</p>
                                <p>Appointment status</p>
    
                                <!-- <button class="btn btn-primary mt-2" on:click={ammendAppointment}>
                                Ammend Appointment
                                </button> -->
                                
                            </div> 
                        </div>
    
                        <div class="card mt-3">
                            <div class="card-body">
    
                                <p>Appointment details</p>
                                <p>Appointment status</p>
    
                                <!-- <button class="btn btn-primary mt-2" on:click={ammendAppointment}>
                                Ammend Appointment
                                </button> -->
                                
                            </div> 
                        </div>
                    <!-- </form> -->
                </div>
            </div>

        </div>
    </div>
</div>

<div class="container mt-4">
    <div class="row">
        <div class="col">
            <h2>Working days</h2>
            <div class="card">
                <div class="card-body">
                    <!-- <form on:submit|preventDefault={updateWorkingHours}> -->

                    <div class="form-group">
                        <p>Please input your working days for the next two weeks</p>
                        <p> Calendar</p>
                        <FullCalendar {options} />
                    </div>

                    <button type="submit" class="btn btn-primary mt-3">Update Hours</button>
                    <!-- </form> -->
                </div>
            </div>
        </div>
    </div>
</div>        
            
        

    


<div class="container mt-4">
    <div class="row">
        <div class="col">
            <h2>Unplanned leave</h2>
            <div class="card">
                <div class="card-body">
                    <!-- <form on:submit|preventDefault={updateWorkingHours}> -->

                    <div class="form-group">
                        <p>Please enter the dates and time you will not be available</p>
                        <!-- <input type="time" bind:value={workingHours.start} />
                        <input type="time" bind:value={workingHours.end} /> -->
                    </div>

                    <button type="submit" class="btn btn-primary mt-3">Update Hours</button>
                    <!-- </form> -->
                </div>
            </div>
        </div>
    </div>
</div>
    

   