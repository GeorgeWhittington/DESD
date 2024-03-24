<script>
    // To control logout behaviour on sensitive pages
    // (such as when a doctor is mid-appointment)
    // set autoLogout to false and use the idle store or onIdle
    // event from svelte-idle to write your own behaviour
    export let autoLogout = true;
    export let userType;
    export let session;

    import { listen, idle } from "svelte-idle";
    import { logout } from "$lib/logout.js";

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

    $: {
        if (autoLogout && $idle && $session.token !== "") {
            console.log(`User is idle! logging out ${JSON.stringify($session)}`);
            logout($session.token, session);
        }
    }
</script>