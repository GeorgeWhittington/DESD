<script>
    import { onMount } from 'svelte';
    import FullCalendar from 'svelte-fullcalendar';
    import interactionPlugin from '@fullcalendar/interaction'
    import daygridPlugin from '@fullcalendar/daygrid';

    let selectedStart = null;
    let selectedEnd = null;

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


    let options2 = {
        initialView: 'dayGridMonth',
        plugins: [daygridPlugin, interactionPlugin],
        editable: false,
        selectable: false,
        aspectRatio: 1.5,
        height: 660,
        events: [...appointmentEvents, ...holidayEvents]
    }

    let options1 = {
        initialView: 'dayGridMonth',
        plugins: [daygridPlugin, interactionPlugin],
        editable: true,
        selectable: true,
        aspectRatio: 1.5,
        height: 660,
        select: handleDateSelect,
        events: [...appointmentEvents, ...holidayEvents]
    }

    // @ts-ignore
    function handleDateSelect(selectInfo) {
        const today = new Date();
        const twoWeeksFromToday = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 14);
        const startDate = new Date(selectInfo.startStr);
        selectedStart = selectInfo.startStr
        selectedEnd = selectInfo.endStr

        console.log("range1: ",selectedEnd-selectedStart)

        if (startDate >= twoWeeksFromToday){
            document.getElementById('bookTimeOffButton').disabled = false;
            
        }
  
    }

    function bookTimeOff() {

        document.getElementById('bookTimeOffButton').disabled = true;
        let confirmed = confirm(`Book the selected date/days off?`);
        if(confirmed){
            console.log("range: ",selectedEnd-selectedStart)
        }
        selectedStart = null;
        selectedEnd = null;
        
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
                <p>To book time off, click or drag the desired dates. Please note, holiday must be booked at least 2 weeks in advance.</p>
                <button class="btn btn-primary mt-2" id="bookTimeOffButton" on:click="{bookTimeOff}" disabled> Book Time Off</button>
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


                    <div class="form-group">
                        <p>Please enter the dates and time you will not be available within the next two weeks. Any appointments must be appointed to another member of staff else </p>

                    </div>

                    <button type="submit" class="btn btn-primary mt-3">Report</button>

                </div>
            </div>
        </div>
    </div>
</div>
    

