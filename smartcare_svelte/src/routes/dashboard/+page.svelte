<script>
    import { getContext } from "svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import AppointmentDashboard from "$lib/components/AppointmentDashboard.svelte";
    const session = getContext("session");
    let userId = $session.userId
</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3, 5]} />

<h1> Dashboard </h1>

{#if $session.userType === 5}
<!-- USER DASHBOARD -->
<AppointmentDashboard title="Outstanding Appointments" stage_id=012></AppointmentDashboard>
<br>
<AppointmentDashboard title="Past Appointments" stage_id=34></AppointmentDashboard>

{:else if $session.userType === 2 || $session.userType === 3}
<!-- STAFF DASHBOARD-->
<AppointmentDashboard title="Appointments For Today" staff_id={userId} stage_id=2 today_only=true></AppointmentDashboard>
<br>
<AppointmentDashboard title="Assigned To Me" staff_id={userId}, stage_id=2></AppointmentDashboard>
<br>
<AppointmentDashboard title="Waiting For Approval" stage_id=0></AppointmentDashboard>
<br>
<AppointmentDashboard title="Requires Manual Scheduling" stage_id=1></AppointmentDashboard>
{/if}