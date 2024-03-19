<script>
    let innerWidth;
    $: alwaysShowNav = innerWidth >= 992 ? "show" : "";

    function logout() {
        // TODO: access logout endpoint
    }
</script>

<svelte:window bind:innerWidth={innerWidth} />

<div class="row">
    <div class="col-lg-3 sticky-top dashboard-nav-wrapper py-2">
        <nav class="navbar dashboard-nav-controls">
            <div class="container-fluid">
                <button
                    class="navbar-toggler" type="button"
                    data-bs-toggle="collapse" data-bs-target="#dashboard-nav"
                    aria-controls="dashboard-nav" aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
        </nav>
        <div class="dashboard-nav collapse {alwaysShowNav}" id="dashboard-nav">
            <nav class="nav nav-pills flex-column align-items-stretch">
                <a class="nav-link" href="#item-1">
                    <i class="bi bi-calendar"></i>
                    My Appointments
                </a>
                <a class="nav-link" href="#item-2">
                    <i class="bi bi-capsule"></i>
                    My Prescriptions
                </a>
                <!-- svelte-ignore a11y-invalid-attribute -->
                <a class="nav-link" href="#" role="button" on:click|preventDefault={logout}>
                    <i class="bi bi-box-arrow-right"></i>
                    Log Out
                </a>
            </nav>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="dashboard-body">
            <slot />
        </div>
    </div>
</div>

<style>
    .dashboard-body {
        height: 100vh;
        overflow-y: scroll;
    }

    .dashboard-nav-controls {
        display: none;
    }

    @media only screen and (max-width: 992px) {
        .dashboard-body {
            height: initial;
            overflow-y: initial;
        }

        .dashboard-nav-wrapper {
            background-color: white;
        }

        .dashboard-nav-controls {
            display: initial;
        }
    }
</style>