<script>
    import PatientDashboard from "$lib/components/PatientDashboard.svelte";
    import StaffDashboard from "$lib/components/StaffDashboard.svelte";
</script>

<!-- <div class="container">
    <h1>Dashboard</h1>
    {#if alert !== ""}
    <div class="alert alert-danger" role="alert">{alert}</div>
    {/if}
    <button type="button" class="btn btn-primary" on:click={logout}>
        Logout
    </button>
</div> -->
<div class="container-fluid">
    <PatientDashboard />

    <!-- <StaffDashboard>
        TODO: home component gets rendered here
    </StaffDashboard> -->
</div>
