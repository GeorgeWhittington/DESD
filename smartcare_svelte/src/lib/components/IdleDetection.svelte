<script>
    export let userType;
    export let session;

    import { listen, idle } from "svelte-idle";
    import { apiPOST } from "$lib/apiFetch.js";
    import { BLANK_SESSION, mid_appointment } from "$lib/constants.js";
    import { goto } from "$app/navigation";
    import { page } from '$app/stores';

    $: console.log($page.url.pathname);

    let timer = null;
    $: {
        if (userType <= 1) {
            timer = 120_0000 // 20 mins
        } else if (userType <= 4) {
            timer = 60_0000 // 10 mins
        } else if (userType == 5) {
            timer = 30_0000 // 5 mins
        }
    }

    let listening = false
    $: {
        if (listening === false && timer !== null) {
            listen({ timer: timer });
            listening = true;
        }
    }

    async function logout() {
        let response = await apiPOST(session, "/auth/logout/", "");
        if (response && response.status < 500) {
            session.set(BLANK_SESSION);
            goto("/");
        }
    }

    function shouldLogout() {
        // need to be idle and logged in to be logged out
        if (!$idle || $session.token === "") {
            return;
        }

        // Check if on appointment page AND if a doctor is mid-appointment on it
        if ($page.url.pathname.includes("/dashboard/appointment/") && $mid_appointment) {
            return;
        }

        console.log(`User is idle! logging out ${JSON.stringify($session)}`);
        logout();
    }

    $: {
        shouldLogout();
    }
</script>