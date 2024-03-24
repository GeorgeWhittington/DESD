import { goto } from "$app/navigation";
import { API_ENDPOINT, BLANK_SESSION } from "$lib/constants";

export async function logout(token, session) {
    let response;
    try {
        response = await fetch(`${API_ENDPOINT}/auth/logout/`, {
            method: "POST",
            headers: {
                "Authorization": `Token ${token}`
            }
        });
    } catch (error) {
        return "Server error, please try again later!";
    }

    if (response.status < 500) {
        session.set(BLANK_SESSION);
        goto("/");
    } else {
        return "Server error, please try again later!";
    }
}