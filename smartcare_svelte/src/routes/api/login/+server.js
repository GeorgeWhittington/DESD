import { json } from "@sveltejs/kit";
import { SSR_API_ENDPOINT } from "$lib/constants.js";

export async function POST({ request }) {
    const { credentials } = await request.json();

    let response;
    let response_json;

    try {
        response = await fetch(`${SSR_API_ENDPOINT}/auth/login/`, {
            method: "POST",
            headers: {
                "Authorization": `Basic ${credentials}`
            }
        });
        response_json = await response.json();
    } catch (error) {
        console.log(error);
        return json({ detail: "Server Error" }, { status: 500 })
    }

    if (!response.ok) {
        return json(response_json, { status: response.status })
    }

    let expiry_date = new Date(response_json.expiry)

    return json({ detail: "Logged in" }, {
        status: response.status,
        headers: { "set-cookie": `token=${response_json.token}; path=/; HttpOnly; expires=${expiry_date.toUTCString()}` }
    })
}