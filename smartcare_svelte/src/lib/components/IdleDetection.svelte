<script>
    // To control logout behaviour on sensitive pages
    // (such as when a doctor is mid-appointment)
    // set autoLogout to false and use the idle store or onIdle
    // event from svelte-idle to write your own behaviour
    export let autoLogout = true;
    export let userType;
    export let session;

    import { listen, idle } from "svelte-idle";
    import { apiPOST } from "$lib/apiFetch.js";
    import { BLANK_SESSION } from "$lib/constants.js";
    import { goto } from "$app/navigation";

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

    $: {
        if (autoLogout && $idle && $session.token !== "") {
            console.log(`User is idle! logging out ${JSON.stringify($session)}`);
            logout();
        }
    }
</script>