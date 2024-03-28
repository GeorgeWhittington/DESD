<script>
    import { onMount } from 'svelte';
    import FullCalendar from 'svelte-fullcalendar';
    import interactionPlugin from '@fullcalendar/interaction'
    import daygridPlugin from '@fullcalendar/daygrid';

    let appointmentEvents = [
      {
        title: 'Appointment',
        start: '2024-03-26',
        color: '#ff9f89'
      },
      {
        title: 'Appointment',
        start: '2024-03-26',
        color: '#ff9f89'
      }
    ]

    let holidayEvents = [
      {
        title: 'Holiday',
        start: '2024-03-28',
        end: '2024-03-30',
        color: '#a4bdfc'
      }
    ]


    let options1 = {
        initialView: 'dayGridMonth',
        plugins: [daygridPlugin, interactionPlugin],
        editable: false,
        selectable: false,
        aspectRatio: 1.5,
        height: 660,
        events: [...appointmentEvents, ...holidayEvents]
    }

    let options2 = {
        initialView: 'dayGridMonth',
        plugins: [daygridPlugin, interactionPlugin],
        editable: true,
        selectable: true,
        aspectRatio: 1.5,
        height: 660,
        select: handleDateSelect,
        events: holidayEvents
    }

    // @ts-ignore
    function handleDateSelect(selectInfo) {
        const today = new Date();
        const twoWeeksFromToday = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 14);
        const startDate = new Date(selectInfo.startStr);


        if (startDate >= twoWeeksFromToday){
            let confirmed = confirm(`Do you want to book off from ${selectInfo.startStr} to ${selectInfo.endStr}?`);
            if (confirmed) {
                console.log(selectInfo.startStr)
            }
        }
        
    }

    function updateWorkingDays(){
        
    }

</script>
  

<div class="container mt-4">
    <h2 id="ScheduleHeader">Schedule</h2>
    <div class="card">
        <div class="card-body">
            <div class="schedule-calendar">
                <FullCalendar options={options1} />
            </div>
        </div>
    </div>
</div>



<div class="container mt-4">
    <div class="row">
        <div class="col">

            <h2 id="appointmentHeader">Appointments</h2>
    
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
            <h2 id="holidaysHeader">Holiday</h2>
            <div class="card">
                <div class="card-body">

                    <div class="form-group">
                        <p>To book time off, click or drag the desired dates. Please note, holiday must be booked at least 2 weeks in advance.</p>
                        <FullCalendar options={options2} />
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>        
            
        

    


<div class="container mt-4">
    <div class="row">
        <div class="col">
            <h2 id="unplannedLeaverHeader">Unplanned leave</h2>
            <div class="card">
                <div class="card-body">
                    <!-- <form on:submit|preventDefault={updateWorkingDays}> -->

                    <div class="form-group">
                        <p>Please enter the dates and time you will not be available within the next two weeks. Any appointments must be appointed to another member of staff else </p>
                        <!-- <input type="time" bind:value={workingHours.start} />
                        <input type="time" bind:value={workingHours.end} /> -->
                    </div>

                    <button type="submit" class="btn btn-primary mt-3">Report</button>
                    <!-- </form> -->
                </div>
            </div>
        </div>
    </div>
</div>
    

