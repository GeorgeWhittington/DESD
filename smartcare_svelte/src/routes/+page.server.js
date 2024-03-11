import { redirect } from "@sveltejs/kit";
import { bootstrapThemes } from "$lib/constants.js";

export const actions = {
    theme: async ({ cookies, request }) => {
        const data = await request.formData();
        let theme = data.get("id");
        if (!(theme in bootstrapThemes)) {
            theme = cookies.theme || "default";
        }

        cookies.set("theme", theme, { path: "/" });

        throw redirect(303, request.url.replace("?/theme", ""));
    },
};