import type { Handle } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib/config/env';

const protectedRoutes = ['/profile', '/applications', '/saved', '/messages', '/resume'];
const guestOnlyRoutes = ['/login', '/register', '/forgot-password', '/reset-password'];

const cookieOptions = {
	path: '/',
	httpOnly: true,
	sameSite: 'lax' as const
};

async function ensureValidAuth(event: Parameters<Handle>[0]['event']) {
	const accessToken = event.cookies.get('access_token');
	const refreshToken = event.cookies.get('refresh_token');
	const secureCookies = API_BASE_URL.startsWith('https://');

	if (accessToken) {
		const meResponse = await event.fetch(`${API_BASE_URL}/auth/me/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		}).catch(() => null);

		if (meResponse?.ok) {
			return true;
		}
	}

	if (!refreshToken) {
		event.cookies.delete('access_token', { path: '/' });
		event.cookies.delete('refresh_token', { path: '/' });
		return false;
	}

	const refreshResponse = await event.fetch(`${API_BASE_URL}/auth/token/refresh/`, {
		method: 'POST',
		headers: {
			Cookie: `refresh_token=${refreshToken}`
		}
	}).catch(() => null);

	if (!refreshResponse?.ok) {
		event.cookies.delete('access_token', { path: '/' });
		event.cookies.delete('refresh_token', { path: '/' });
		return false;
	}

	const refreshData = await refreshResponse.json();
	event.cookies.set('access_token', refreshData.access, {
		...cookieOptions,
		secure: secureCookies,
		maxAge: 60 * 60
	});
	event.cookies.set('refresh_token', refreshData.refresh, {
		...cookieOptions,
		secure: secureCookies,
		maxAge: 60 * 60 * 24 * 7
	});

	return true;
}

export const handle: Handle = async ({ event, resolve }) => {
	const accessToken = event.cookies.get('access_token');
	const refreshToken = event.cookies.get('refresh_token');
	let hasAuth = Boolean(accessToken || refreshToken);
	const pathname = event.url.pathname;

	if (protectedRoutes.some((route) => pathname.startsWith(route))) {
		if (!hasAuth) {
			return new Response(null, {
				status: 302,
				headers: {
					location: `/login?redirect=${encodeURIComponent(pathname)}`
				}
			});
		}

		hasAuth = await ensureValidAuth(event);
		if (!hasAuth) {
			return new Response(null, {
				status: 302,
				headers: {
					location: `/login?redirect=${encodeURIComponent(pathname)}`
				}
			});
		}
	}

	if (guestOnlyRoutes.some((route) => pathname.startsWith(route)) && hasAuth) {
		hasAuth = await ensureValidAuth(event);
		if (hasAuth) {
			return new Response(null, {
				status: 302,
				headers: {
					location: '/'
				}
			});
		}
	}

	return resolve(event);
};
