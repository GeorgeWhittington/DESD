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

<AppointmentDashboard title="My Appointments" staff_id={userId}, stage_id=3></AppointmentDashboard>
<br>
<AppointmentDashboard title="Waiting for approval" stage_id=0></AppointmentDashboard>
<br>
<AppointmentDashboard title="Requires Manual Scheduling" stage_id=1></AppointmentDashboard>
<!--

    if staff:
        staff dashboard homepage
    else:
        all patient components

-->
