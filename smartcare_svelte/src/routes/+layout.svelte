<script>
    import { browser } from '$app/environment';
    import { writable } from "svelte/store";
    import { getContext, setContext, onDestroy } from "svelte";
    import { BLANK_SESSION } from "$lib/constants.js";

    // Try to fetch existing session from localstorage.
    const storedSession = browser ? JSON.parse(window.localStorage.getItem("session")) : BLANK_SESSION;
    // Add a writeable store containing session data to context,
    // a blank object is used if session couldn't be fetched
    setContext("session", writable(storedSession || BLANK_SESSION))

    // Fetch the store that was just stored from context and ensure
    // that any changes made to it are written to localstorage
    const session = getContext("session");
    const unsubscribe = session.subscribe((value) => {
        if (value && browser)
            window.localStorage.setItem("session", JSON.stringify(value));
    });

    onDestroy(unsubscribe);
</script>

<slot/>