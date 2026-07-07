import type { LayoutServerLoad } from './$types';
import { API_BASE_URL } from '$lib/config/env';

export const load: LayoutServerLoad = async ({ cookies, fetch }) => {
	let accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');
	const secureCookies = API_BASE_URL.startsWith('https://');
	const clearAuthCookies = () => {
		cookies.delete('access_token', { path: '/' });
		cookies.delete('refresh_token', { path: '/' });
	};

	if (!accessToken && refreshToken) {
		try {
			const refreshResponse = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
				method: 'POST',
				headers: {
					Cookie: `refresh_token=${refreshToken}`
				}
			});

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
			clearAuthCookies();
		}
	}

	if (!accessToken) {
		return {
			user: null,
			isAuthenticated: false
		};
	}

	try {
		const response = await fetch(`${API_BASE_URL}/auth/me/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

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
		clearAuthCookies();
		return {
			user: null,
			isAuthenticated: false
		};
	}
};
