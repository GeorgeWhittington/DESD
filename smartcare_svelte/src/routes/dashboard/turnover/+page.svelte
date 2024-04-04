<script>
    import { getContext } from "svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";

    const session = getContext("session");
</script>

<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1]} />