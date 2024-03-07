/** @type {import("./$types").LayoutServerLoad} */
export const load = async ({ locals }) => {
    return locals.token
    ? {
        session: {
            token: locals.token
        }
      }
    : {};
}