<script>
    export let userType;
    export let session;

    import { listen, idle, onIdle } from "svelte-idle";
    import { apiPOST } from "$lib/apiFetch.js";
    import { BLANK_SESSION, mid_appointment } from "$lib/constants.js";
    import { goto } from "$app/navigation";
    import { page } from '$app/stores';

    let timer = null;
    $: {
        if (userType <= 1) {
            timer = 120_000 // 20 mins
        } else if (userType <= 4) {
            timer = 60_000 // 10 mins
        } else if (userType == 5) {
            timer = 30_000 // 5 mins
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

    onIdle(() => {
        // Not logged in
        if ($session.token === "")
            return;

        if ($page.url.pathname.includes("/dashboard/appointment/") && $mid_appointment) {
            console.log("User is idle, but they will not be logged out because they are conducting an appointment");
            return;
        }

        console.log(`User is idle! logging out ${JSON.stringify($session)}`);
        logout();
    })
</script>