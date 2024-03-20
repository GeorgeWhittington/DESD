<script>
    import { getContext } from "svelte";
    import { browser } from '$app/environment';
    import { goto } from "$app/navigation";
    import { API_ENDPOINT, BLANK_SESSION } from "$lib/constants";
    import NavLink from "$lib/components/NavLink.svelte";

    let innerWidth;
    $: alwaysShowNav = innerWidth >= 992 ? "show" : "";

    const session = getContext("session");

    // need to be logged in as valid user to access dashboard (external users only have api access)
    $: {
        if (browser) {
            if ($session.token === BLANK_SESSION.token ||
                $session.userType === BLANK_SESSION.userType ||
                $session.userType === 4
            ) {
                // TODO: set up flash message system using localStorage
                // and here notify the user that they are not logged in
                session.set(BLANK_SESSION);  // clear all incase of only one being set
                goto("/");
            }
        }
    }

    let alert = "";

    async function logout() {
        let response;
        try {
            response = await fetch(`${API_ENDPOINT}/auth/logout/`, {
                method: "POST",
                headers: {
                    "Authorization": `Token ${$session.token}`
                }
            });
        } catch (error) {
            // TODO: helpful error msg
            return;
        }

        if (response.status < 500) {
            session.set(BLANK_SESSION);
            goto("/");
        } else {
            // TODO: replace with flash system implementation
            alert = "Server error, please try again later!";
        }
    }
</script>

<svelte:window bind:innerWidth={innerWidth} />

<div class="row">
    <div class="col-lg-3 sticky-top dashboard-nav-wrapper py-2">
        <nav class="navbar dashboard-nav-controls">
            <div class="container-fluid">
                <button
                    class="navbar-toggler ms-auto" type="button"
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
                <!-- superuser/admin -->
                {#if [0, 1].includes($session["userType"])}
                <NavLink link="#" iconClass="bi-house" title="Home" />
                <NavLink link="#" iconClass="bi-calendar" title="Schedules" />
                <NavLink link="#" iconClass="bi-bank" title="Turnover" />

                <!-- doctor/nurse -->
                {:else if [2, 3].includes($session["userType"])}
                <NavLink link="#" iconClass="bi-house" title="Home" />
                <NavLink link="#" iconClass="bi-calendar" title="Schedule" />
                <NavLink link="#" iconClass="bi-capsule" title="Prescriptions" />

                <!-- patient -->
                {:else if $session["userType"] === 5}
                <NavLink link="#appointments" iconClass="bi-calendar" title="My Appointments" />
                <NavLink link="#prescriptions" iconClass="bi-capsule" title="My Prescriptions" />
                {/if}
                <!-- svelte-ignore a11y-invalid-attribute -->
                <a class="nav-link" href="#" role="button" on:click|preventDefault={logout}>
                    <i class="bi bi-box-arrow-right"></i>
                    Log Out
                </a>
            </nav>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="dashboard-body container-fluid">
            <!-- TODO: Alert/Flash component would fit well here -->

            <!-- TODO: dummy data, remove -->
            <div id="appointments">
                <h4>My Appointments</h4>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc velit nibh, eleifend ac ligula eget, efficitur auctor magna. Sed maximus semper suscipit. Aenean ultrices turpis eget diam sagittis, vel interdum elit dignissim. Cras in dolor in arcu placerat commodo. Duis sed laoreet elit, et euismod nisl. Mauris varius ligula vitae porttitor porta. Phasellus aliquam, urna in convallis gravida, mauris est rutrum arcu, a mattis nibh orci sed sapien. Phasellus luctus facilisis dui eu rutrum. Integer velit quam, maximus quis semper quis, commodo pulvinar leo.</p>
                <p>Suspendisse pharetra elit in dui faucibus faucibus. Vivamus placerat rhoncus nisl, non scelerisque enim pulvinar vitae. Donec fringilla sapien sit amet leo scelerisque ullamcorper. Sed interdum nibh sed ultricies dapibus. Quisque quis tincidunt diam, id faucibus arcu. Duis volutpat in massa at interdum. Sed quam lacus, dictum tristique ex quis, feugiat ornare turpis. Quisque malesuada diam ut sapien tempor tempor.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc velit nibh, eleifend ac ligula eget, efficitur auctor magna. Sed maximus semper suscipit. Aenean ultrices turpis eget diam sagittis, vel interdum elit dignissim. Cras in dolor in arcu placerat commodo. Duis sed laoreet elit, et euismod nisl. Mauris varius ligula vitae porttitor porta. Phasellus aliquam, urna in convallis gravida, mauris est rutrum arcu, a mattis nibh orci sed sapien. Phasellus luctus facilisis dui eu rutrum. Integer velit quam, maximus quis semper quis, commodo pulvinar leo.</p>
                <p>Suspendisse pharetra elit in dui faucibus faucibus. Vivamus placerat rhoncus nisl, non scelerisque enim pulvinar vitae. Donec fringilla sapien sit amet leo scelerisque ullamcorper. Sed interdum nibh sed ultricies dapibus. Quisque quis tincidunt diam, id faucibus arcu. Duis volutpat in massa at interdum. Sed quam lacus, dictum tristique ex quis, feugiat ornare turpis. Quisque malesuada diam ut sapien tempor tempor.</p>
            </div>

            <div id="prescriptions">
                <h4>My Prescriptions</h4>
                <p>Duis hendrerit pharetra ligula eget interdum. Fusce porttitor lacinia tristique. Curabitur nec nibh a ex cursus consectetur eget id turpis. Nulla nec pretium dolor. Pellentesque ex urna, commodo nec accumsan id, ultrices non sapien. Mauris fringilla pulvinar purus. Integer eu dapibus justo. Morbi eu vehicula lacus. Nam tristique enim est, cursus facilisis nisi finibus ac. Ut vestibulum tincidunt tellus, eu sagittis nisl vulputate et. Sed sagittis lectus eu eros suscipit sodales. Duis imperdiet eget ipsum vitae luctus. Suspendisse potenti. Suspendisse imperdiet diam at ex efficitur, sed eleifend velit viverra.</p>
                <p>In varius dignissim risus. Mauris vitae egestas diam. Maecenas vitae risus vel diam egestas lacinia eu in metus. Vivamus eleifend aliquam sem, ut mollis quam dignissim quis. Curabitur viverra turpis non eleifend sagittis. Mauris sed urna vehicula, sodales quam vel, rhoncus augue. Duis in sem sed nunc vestibulum tempor vel non orci. Curabitur sem purus, pellentesque iaculis nisi et, posuere accumsan mauris. Quisque libero turpis, ullamcorper vitae sem sed, porta blandit lectus. Integer aliquet id nisl ut interdum.</p>
            </div>

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
            background-color: var(--bs-body-bg);
        }

        .dashboard-nav-controls {
            display: initial;
        }
    }
</style>