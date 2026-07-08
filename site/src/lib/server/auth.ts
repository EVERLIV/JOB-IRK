import type { Cookies } from '@sveltejs/kit';

export function setAuthCookies(
	cookies: Cookies,
	tokens: { access?: string; refresh?: string },
	secure: boolean
) {
	if (tokens.access) {
		cookies.set('access_token', tokens.access, {
			httpOnly: true,
			secure,
			sameSite: 'lax',
			path: '/',
			maxAge: 60 * 60
		});
	}

	if (tokens.refresh) {
		cookies.set('refresh_token', tokens.refresh, {
			httpOnly: true,
			secure,
			sameSite: 'lax',
			path: '/',
			maxAge: 60 * 60 * 24 * 7
		});
	}
}

export function clearAuthCookies(cookies: Cookies) {
	cookies.delete('access_token', { path: '/' });
	cookies.delete('refresh_token', { path: '/' });
}
