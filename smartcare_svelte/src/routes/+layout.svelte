<script>
    import { page } from "$app/stores";
    import { writable } from "svelte/store";
    import { getContext, setContext } from "svelte";

    setContext("session", writable($page.data.session));
    const session = getContext("session");
</script>

<slot/>