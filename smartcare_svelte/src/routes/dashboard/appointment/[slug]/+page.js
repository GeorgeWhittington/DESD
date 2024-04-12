import { error } from "@sveltejs/kit";

export function load({ params }) {
    const slug = params.slug;
    if (isNaN(slug)) { throw error(404);}
    return {slug};
}