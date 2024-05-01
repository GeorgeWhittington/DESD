<script>
    import { getContext } from "svelte";
    import NeedsAuthorisation from "$lib/components/NeedsAuthorisation.svelte";
    import IdleDetection from "$lib/components/IdleDetection.svelte";
    import UserTable from "$lib/components/UserTable.svelte";

    const session = getContext("session");
</script>

<IdleDetection userType={$session.userType} session={session} />
<NeedsAuthorisation userType={$session.userType} userTypesPermitted={[0, 1]} />

<UserTable userTypes={[2, 3]} title="Staff Account Management" />

<UserTable userTypes={[5]} title="Patient Account Management" />

<UserTable userTypes={[0, 1, 4]} title="Admin and External Account Management" />