<script>
    import { getContext } from "svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";

    const session = getContext("session");
</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1, 2, 3, 5]} />

<!--

    if staff:
        staff dashboard homepage
    else:
        all patient components

-->
