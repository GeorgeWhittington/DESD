import { json } from "@sveltejs/kit";

export async function POST() {
    return json({ detail: "Ok" }, {
        status: 200,
        headers: { "set-cookie": "token=''; path=/; HttpOnly; expires=Thu, 01 Jan 1970 00:00:00 GMT" }
    })
}