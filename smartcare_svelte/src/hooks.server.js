import cookie from "cookie";
import { writable } from "svelte/store";

/** @type {import("@sveltejs/kit").Handle} */
export async function handle({ event, resolve }) {
    const cookies = cookie.parse(event.request.headers.get("cookie") || "");
    event.locals.token = cookies.token;
    return await resolve(event);
}