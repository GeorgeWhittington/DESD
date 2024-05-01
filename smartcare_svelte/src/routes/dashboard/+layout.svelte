<script>
    import { getContext } from "svelte";
    import { browser } from '$app/environment';
    import { goto } from "$app/navigation";
    import { page } from '$app/stores';
    import { BLANK_SESSION } from "$lib/constants";
    import NavLink from "$lib/components/NavLink.svelte";
    import { apiPOST } from "$lib/apiFetch.js";

    let innerWidth;
    $: alwaysShowNav = innerWidth >= 992 ? "show" : "";

    const session = getContext("session");
    let alert = "";

    async function logoutWrapper() {
        let response = await apiPOST(session, "/auth/logout/", "");
        if (response && response.status < 500) {
            session.set(BLANK_SESSION);
            goto("/");
        } else {
            alert = "Server error, please try again later!";
        }
    }
</script>

<svelte:window bind:innerWidth={innerWidth} />

<div class="row g-0">
    <div class="col-lg-3 sticky-top dashboard-nav-wrapper bg-secondary">
        <nav class="navbar d-flex flex-row justify-content-between align-items-center text-center flex-nowrap text-white pt-2 px-3">
            <span><i class="bi bi-person"></i> {$session.firstName} {$session.lastName}</span>
            <div>
                <div class="btn-group ms-1">
                    <a href="/" class="btn btn-light"><i class="bi bi-house"></i></a>
                    <a href="/dashboard/settings/" class="btn btn-light"><i class="bi bi-gear"></i></a>
                </div>
                <button
                    class="navbar-toggler bg-light ms-1 border-0 dashboard-nav-controls" type="button"
                    data-bs-toggle="collapse" data-bs-target="#dashboard-nav"
                    aria-controls="dashboard-nav" aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon text-white"></span>
                </button>
            </div>
        </nav>
        <div class="dashboard-nav collapse {alwaysShowNav} pb-2" id="dashboard-nav">
            <nav class="nav  flex-column align-items-stretch">
                <!-- superuser/admin -->
                {#if [0, 1].includes($session["userType"])}
                <NavLink link="/dashboard#" iconClass="bi-activity" title="Overview" />
                <NavLink link="/dashboard/schedule" iconClass="bi-calendar" title="Schedules" />
                <NavLink link="/dashboard/turnover" iconClass="bi-bank" title="Turnover" />
                <NavLink link="/dashboard/account-management" iconClass="bi-person-gear" title="Account Management" />
                <NavLink link="/dashboard/payrate-management" iconClass="bi-cash" title="Payrate Management" />

                <!-- doctor/nurse -->
                {:else if [2, 3].includes($session["userType"])}
                <NavLink link="/dashboard#" iconClass="bi-activity" title="Overview" />
                <NavLink link="/dashboard/schedule" iconClass="bi-calendar" title="Schedule" />
                    {#if $page.url.pathname === "/dashboard/schedule"}
                    <ul>
                        <li><NavLink link="/dashboard/schedule#ScheduleHeader" title="Schedule" /></li>
                        <li><NavLink link="/dashboard/schedule#unplannedLeaverHeader" title="Unplanned Leave" /></li>
                    </ul>
                    {/if}
                <NavLink link="/dashboard/prescriptions" iconClass="bi-capsule" title="Prescriptions" />

                <!-- patient -->
                {:else if $session["userType"] === 5}
                <NavLink link="/dashboard#appointments" iconClass="bi-calendar" title="My Appointments" />
                <NavLink link="/dashboard#prescriptions" iconClass="bi-capsule" title="My Prescriptions" />
                <NavLink link="/dashboard/request-appointment" iconClass="bi-pencil-square" title="Request Appointment" />
                {/if}
                <!-- svelte-ignore a11y-invalid-attribute -->
                <a class="nav-link text-white" href="#" role="button" on:click|preventDefault={logoutWrapper}>
                    <i class="bi bi-box-arrow-right"></i>
                    Log Out
                </a>
            </nav>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="dashboard-body container-fluid py-2">
            <slot />
        </div>
    </div>
</div>

<style>
    .nav-link {
        border-bottom: 1px solid transparent;
    }

    .nav-link:hover {
        border-bottom: 1px solid;
    }

    .dashboard-body {
        height: 100vh;
        overflow-y: scroll;
    }

    .dashboard-nav-controls {
        display: none;
    }

    .dashboard-nav-wrapper {
        height: 100vh;
    }

    ul {
        list-style: none;
    }

    @media only screen and (max-width: 992px) {
        .dashboard-body {
            height: initial;
            overflow-y: initial;
            margin-top: 70px;
        }

        .dashboard-nav-wrapper {
            height: initial;
            width: 100vw;
            position: fixed;
            top: 0;
            left: 0;
        }

        .dashboard-nav-controls {
            display: initial;
        }
    }
</style>