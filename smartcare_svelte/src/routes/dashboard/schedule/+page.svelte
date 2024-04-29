<script>
    import { onMount } from 'svelte';
    import { API_ENDPOINT,USER_ID} from "$lib/constants";
    import { getContext } from "svelte";
    import FullCalendar from 'svelte-fullcalendar';
    import interactionPlugin from '@fullcalendar/interaction'
    import daygridPlugin from '@fullcalendar/daygrid';
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";

    const session = getContext("session");

    let selectedStart = null;
    let selectedEnd = null;
    let start_date;
    let end_date;

    let timeOffEvents = []
    let appointmentEvents = []

    let options = {
        initialView: 'dayGridMonth',
        plugins: [daygridPlugin, interactionPlugin],
        
    };

    onMount(async () => {

        const headers = {
        Authorization: `Token ${$session.token}`,
        "content-type": "application/json",
        };

        const timeOffResponse  = await fetch(`${API_ENDPOINT}/timeoff/`,{headers});
        const timeOffData  = await timeOffResponse.json();
        timeOffEvents = timeOffData
        .filter(item => item.staff === $session.userId)
        .map(item => ({
            title: item.reason,
            start: item.start_date,
            end: item.end_date,
            color: item.reason === 'Unplanned leave' ? 'red' : 'blue',
            eventType: 'timeOff'
        }));

        const appointmentResponse = await fetch(`${API_ENDPOINT}/appointments/`, { headers });
        const appointmentData = await appointmentResponse.json();
        appointmentEvents = appointmentData
        .filter(item => item.staff?.id === $session.userId)
        .map(item => ({
            id: item.id,
            title: "appointment" ,
            start: item.assigned_start_time, 
            end: item.assigned_start_time,
            color: item.stage === 2 ? 'green' : item.stage === 3 ? 'red' : 'orange',
            eventType: 'appointment'
        }));

        options = {
        initialView: 'dayGridMonth',
        plugins: [daygridPlugin, interactionPlugin],
        editable: false,
        selectable: true,
        aspectRatio: 1.5,
        height: 660,
        eventTimeFormat: {
        hour: '2-digit',
        minute: '2-digit',
        meridiem: 'short', 
        hour12: true
        },
        eventClick: handleEventClick,
        select: handleDateSelect,
        events: [...timeOffEvents, ...appointmentEvents]  
        };

        console.log(appointmentEvents)
    });


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
        else{
            document.getElementById('bookTimeOffButton').disabled = true;
        }
        
  
    }

    function bookTimeOff() {

        document.getElementById('bookTimeOffButton').disabled = true;
        let confirmed = confirm(`Book the selected date/days off?`);
        if(confirmed){
            console.log("range: ",selectedEnd-selectedStart)
            start_date = selectedStart
            end_date = selectedEnd
            requestTimeOff('Holiday')
        }
        selectedStart = null;
        selectedEnd = null;
        
    }

    function updateWorkingDays(){
        
    }

    function handleEventClick(eventInfo){
        if (eventInfo.event.extendedProps.eventType === 'appointment') {
            fetchAppointmentDetails(eventInfo.event.id);
        }
    }

    async function fetchAppointmentDetails(eventId){
        try {
            const response = await fetch(`${API_ENDPOINT}/appointments/${eventId}`, {
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "Content-Type": "application/json", 
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch appointment details');
            }

            const details = await response.json();

            
            let message = `Patient: ${details.patient.first_name} ${details.patient.last_name}
            \nDescription: ${details.symptoms}
            \nStage: ${details.stage === 2 ? 'Completed' : details.stage === 3 ? 'Cancelled' : 'Scheduled'}`;
            
            
            alert(message);
        } catch (error) {
            console.error("Error fetching appointment details:", error);
            alert("There was an error fetching the appointment details.");
        }
    }

    export async function requestTimeOff(reason) {
        if (!start_date || !end_date) {
            alert('Both start date and end date are required.');
            return;
        }

        let response;

        let req_body = { staff: $session.userId, start_date: start_date, end_date : end_date, reason : reason };

        try {
            response = await fetch(`${API_ENDPOINT}/timeoff/`, {
                method: "POST",
                headers: {
                    Authorization: `Token ${$session.token}`,
                    "content-type": "application/json",
                },
                body: JSON.stringify(req_body),
            });
            location.reload()
        } catch (error) {
            return "Server error, please try again later!";
        }
    }

</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3]} />

<div class="container mt-4">
    <h2 id="ScheduleHeader">Schedule</h2>
    <div class="card">
        <div class="card-body">
            <div class="schedule-calendar">
                
                <FullCalendar options={options} />
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
                    <p>Please enter the dates and time you will not be available within the next two weeks. Any appointments must be appointed to another member of staff else </p>

                    <form on:submit|preventDefault={() => requestTimeOff('Unplanned leave')}>
                        <div class="mb-3">
                
                            <div class="mb-3">
                                <label for="txtDate" class="form-label">Start Date</label>
                                <input type="date" id="txtDate" class="form-control" bind:value={start_date}>
                            </div>

                            <div class="mb-3">
                                <label for="txtDate" class="form-label">End Date</label>
                                <input type="date" id="txtDate" class="form-control" bind:value={end_date}>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary mt-3">Report</button>
                    </form>
          
                </div>
            </div>
        </div>
    </div>
</div>
    

