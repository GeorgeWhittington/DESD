<script>
    export let userTypesPermitted;
    export let userType;

    import { goto } from "$app/navigation";
    import { page } from '$app/stores';
    import { browser } from '$app/environment';

    $: {
        if (browser && userType !== undefined) {
            if (!userTypesPermitted.includes(userType)) {
                let pathname = $page.url.pathname;
                if (pathname == "/dashboard") {
                    console.log(`User unauthorized for path ${pathname}, redirecting to home`);
                    goto("/");
                } else {
                    console.log(`User unauthorized for path ${pathname}, redirecting to dashboard`);
                    goto("/dashboard");
                }
            }
        }
    }
</script>