<script>
    import { onMount } from 'svelte';
    import { goto } from "$app/navigation";
    import {USER_TYPES} from "$lib/constants";
    import { getContext } from "svelte";
    import { apiGET, apiPOST } from "$lib/apiFetch.js";
    import FullCalendar from 'svelte-fullcalendar';
    import interactionPlugin from '@fullcalendar/interaction'
    import daygridPlugin from '@fullcalendar/daygrid';
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";

    const session = getContext("session");

    let selectedStart = null;
    let selectedEnd = null;
    let start_date;
    let end_date;
    let userId = $session.userId

    let timeOffEvents = []
    let appointmentEvents = []
    let staffList = []
    let staffTypes = [2,3]

    let options = reactiveOptions();

    function reactiveOptions() {
        return {
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
    }

    onMount(async () => {
        let staffResponse = await apiGET(session, "/staff/");
        if (staffResponse && staffResponse.ok) {
            let response_json = await staffResponse.json();
            staffList = response_json.filter(staff => staff.user.id !== userId);
        }

        await fetchData(userId)
        options = reactiveOptions()
    });

    async function fetchData(staffId){

        let timeOffResponse = await apiGET(session, "/timeoff?staff=${staffId}");
        if (timeOffResponse && timeOffResponse.ok) {
            let timeOffData  = await timeOffResponse.json();
            timeOffEvents = timeOffData
                .filter(item => item.staff === staffId)
                .map(item => ({
                    title: item.reason,
                    start: item.start_date,
                    end: item.end_date,
                    color: item.reason === 'Unplanned leave' ? 'red' : 'blue',
                    eventType: 'timeOff'
                }));
        } else {
            console.log("Error fetching timeoff data");
        }

        let appointmentResponse = await apiGET(session, `/appointments?staff_id=${staffId}`);
        if (appointmentResponse && appointmentResponse.ok) {
            let appointmentData = await appointmentResponse.json();
            appointmentEvents = appointmentData
                .map(item => ({
                    id: item.id,
                    title: "appointment" ,
                    start: item.assigned_start_time, 
                    end: item.assigned_start_time,
                    color: item.stage === 3 ? 'green' : item.stage === 4 ? 'red' : 'orange',
                    eventType: 'appointment'
                }));
        }

        options = reactiveOptions();
    }

    function handleDateSelect(selectInfo) {
        const today = new Date();
        const twoWeeksFromToday = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 14);
        const startDate = new Date(selectInfo.startStr);
        selectedStart = selectInfo.startStr
        selectedEnd = selectInfo.endStr


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
            goto(`/dashboard/appointment/${eventInfo.event.id}`);
        }
    }

    async function fetchAppointmentDetails(eventId){
        let response = await apiGET(session, `/appointments/${eventId}`);
        if (response && response.ok) {
            let response_json = await response.json();
            alert(`Patient: ${details.patient.first_name} ${details.patient.last_name}
            \nDescription: ${details.symptoms}
            \nStage: ${details.stage === 2 ? 'Completed' : details.stage === 3 ? 'Cancelled' : 'Scheduled'}`);
        } else {
            alert("There was an error fetching the appointment details.");
        }
    }

    export async function requestTimeOff(reason) {
        if (!start_date || !end_date) {
            alert('Both start date and end date are required.');
            return;
        }

        let response = await apiPOST(session, "/timeoff/", JSON.stringify({
            staff: $session.userId, start_date: start_date, end_date: end_date, reason: reason
        }));

        if (response && response.ok) {
            location.reload();
        } else {
            return "Server error, please try again later!";
        }
    }
    
    

</script>

<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3]} />

<div class="container mt-4">
    <h2 id="ScheduleHeader">Schedule</h2>
    <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
          View Staff Calendars
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li><a class="dropdown-item" href="#" on:click|preventDefault={() => fetchData(userId)}>You</a></li>
            <li><hr class="dropdown-divider"></li>
            {#each staffList as staff}
            <li><a class="dropdown-item" href="#" on:click|preventDefault={() => fetchData(staff.user.id)}>{staff.user.first_name} {staff.user.last_name}</a></li>
            {/each}  
        </ul>
    </div> 
    <div class="card mt-2">
        <div class="card-body">
            <div class="schedule-calendar">
                
                <FullCalendar options={options} />
                <p>To book time off, click or drag the desired dates. Please note, holiday must be booked at least 2 weeks in advance.</p>
                <button class="btn btn-primary mt-2" id="bookTimeOffButton" on:click="{bookTimeOff}" disabled> Book Time Off</button>
            </div>
        </div>
    </div>
</div>


  
{#if staffTypes.includes($session.userType)}
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
{/if}

    

