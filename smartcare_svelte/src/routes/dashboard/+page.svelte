<script>
    import { getContext } from "svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";

    const session = getContext("session");
</script>

<IdleDetection userType={$session.userType} session={session} />

<!--

    if staff:
        staff dashboard homepage
    else:
        all patient components

-->
