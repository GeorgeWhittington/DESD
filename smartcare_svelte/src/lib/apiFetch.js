import { goto } from "$app/navigation";
import { API_ENDPOINT, BLANK_SESSION } from "$lib/constants.js";


export async function apiGET(session, endpoint) {
    try {
        let response = await fetch(API_ENDPOINT + endpoint, {
            method: "GET",
            headers: {
                "Authorization": `Token ${session.token}`
            }
        });


        if (response.status == 401) {
            console.log("Token expired, clearing session.");
            session.set(BLANK_SESSION);
            goto("/");
        }

        return response;
    } catch (error) {
        console.error("Syntax or network error during api GET:");
        console.error(error, error.stack);
        return null;
    }
}

export async function apiPOST(session, endpoint, json_data) {
    try {
        let response = await fetch(API_ENDPOINT + endpoint, {
            method: "POST",
            body: json_data,
            headers: {
                "Authorization": `Token ${session.token}`,
                "content-type": "application/json"
            }
        });

        if (response.status == 401) {
            console.log("Token expired, clearing session.");
            session.set(BLANK_SESSION);
            goto("/");
        }

        return response;
    } catch (error) {
        console.error("Syntax or network error during api POST:");
        console.error(error, error.stack);
        return null;
    }
}