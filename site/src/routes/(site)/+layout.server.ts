import type { LayoutServerLoad } from './$types';
import { API_BASE_URL } from '$lib/config/env';

async function fetchWithTimeout(url: string, init: RequestInit, timeoutMs = 2500) {
	const controller = new AbortController();
	const timer = setTimeout(() => controller.abort(), timeoutMs);
	try {
		return await fetch(url, { ...init, signal: controller.signal });
	} finally {
		clearTimeout(timer);
	}
}

export const load: LayoutServerLoad = async ({ cookies }) => {
	let accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');
	const secureCookies = API_BASE_URL.startsWith('https://');
	const clearAuthCookies = () => {
		cookies.delete('access_token', { path: '/' });
		cookies.delete('refresh_token', { path: '/' });
	};

	// Never block the whole page on a cold Railway/Neon wake for auth
	if (!accessToken && refreshToken) {
		try {
			const refreshResponse = await fetchWithTimeout(
				`${API_BASE_URL}/auth/token/refresh/`,
				{
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ refresh: refreshToken })
				},
				2500
			);

			if (refreshResponse.ok) {
				const refreshData = await refreshResponse.json();
				accessToken = refreshData.access;
				cookies.set('access_token', refreshData.access, {
					path: '/',
					httpOnly: true,
					secure: secureCookies,
					sameSite: 'lax',
					maxAge: 60 * 60
				});
				cookies.set('refresh_token', refreshData.refresh, {
					path: '/',
					httpOnly: true,
					secure: secureCookies,
					sameSite: 'lax',
					maxAge: 60 * 60 * 24 * 7
				});
			}
		} catch {
			// Keep refresh cookie; page still renders as guest if API is cold
		}
	}

	if (!accessToken) {
		return {
			user: null,
			isAuthenticated: false
		};
	}

	try {
		const response = await fetchWithTimeout(
			`${API_BASE_URL}/auth/me/`,
			{ headers: { Authorization: `Bearer ${accessToken}` } },
			2500
		);

		if (!response.ok) {
			clearAuthCookies();
			return {
				user: null,
				isAuthenticated: false
			};
		}

		const user = await response.json();
		return {
			user,
			isAuthenticated: true
		};
	} catch {
		return {
			user: null,
			isAuthenticated: false
		};
	}
};
