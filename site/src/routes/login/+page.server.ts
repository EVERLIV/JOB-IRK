import { redirect, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getApiBaseUrl } from '$lib/config/env';
import { setAuthCookies } from '$lib/server/auth';

export const load: PageServerLoad = async ({ url }) => {
	return {
		redirectTo: url.searchParams.get('redirect') || '/'
	};
};

export const actions: Actions = {
	default: async ({ request, cookies, fetch, url }) => {
		const formData = await request.formData();

		const email = formData.get('email')?.toString() || '';
		const password = formData.get('password')?.toString() || '';
		const redirectTo = formData.get('redirect_to')?.toString() || '/';

		if (!email || !password) {
			return fail(400, {
				error: 'Введите email и пароль.',
				email
			});
		}

		try {
			const response = await fetch(`${getApiBaseUrl()}/auth/login/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email, password })
			});

			const data = await response.json();

			if (!response.ok) {
				let errorMessage = 'Не удалось войти. Пожалуйста, попробуйте снова.';
				if (data.detail) {
					errorMessage = data.detail;
				} else if (data.non_field_errors) {
					errorMessage = data.non_field_errors.join(', ');
				} else if (data.email) {
					errorMessage = `Email: ${data.email.join(', ')}`;
				} else if (data.password) {
					errorMessage = `Пароль: ${data.password.join(', ')}`;
				}

				return fail(400, {
					error: errorMessage,
					email
				});
			}

			const secureCookies = url.protocol === 'https:';
			setAuthCookies(
				cookies,
				{ access: data.access, refresh: data.refresh },
				secureCookies
			);

			throw redirect(302, redirectTo);
		} catch (error) {
			if (error instanceof Response || (error as { status?: number })?.status === 302) {
				throw error;
			}

			console.error('Login error:', error);
			return fail(500, {
				error: 'Произошла непредвиденная ошибка. Попробуйте снова.',
				email
			});
		}
	}
};
