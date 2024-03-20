import cookie from "cookie";
import { bootstrapThemes } from "$lib/constants.js";

/** @type {import("@sveltejs/kit").Handle} */
export async function handle({ event, resolve }) {
    const cookies = cookie.parse(event.request.headers.get("cookie") || "");
    event.locals.theme = cookies.theme || "default";

    let theme = bootstrapThemes[event.locals.theme];
    theme = theme === undefined ? bootstrapThemes["default"] : theme;

    return await resolve(event, {
        transformPageChunk: ({ html }) => html.replace("%sveltekit.bootstrap_stylesheet%", theme)
    });
}