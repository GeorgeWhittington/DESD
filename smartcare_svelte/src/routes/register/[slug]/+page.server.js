import { error } from "@sveltejs/kit";

export function load({ params }) {
	const slug = params.slug;

	if (!["staff", "patient"].includes(slug)) throw error(404);

	return { slug };
}