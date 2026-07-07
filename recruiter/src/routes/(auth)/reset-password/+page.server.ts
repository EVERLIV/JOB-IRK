import { redirect, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getApiBaseUrl } from '$lib/config/env';

export const load: PageServerLoad = async ({ url }) => {
	// Get token from URL query params
	const token = url.searchParams.get('token') || '';

	return {
		token
	};
};

export const actions: Actions = {
	default: async ({ request, fetch }) => {
		const formData = await request.formData();

		const token = formData.get('token')?.toString() || '';
		const password = formData.get('password')?.toString() || '';
		const confirmPassword = formData.get('confirm_password')?.toString() || '';

		// Validation
		if (!token) {
			return fail(400, {
				error: 'Недействительный или отсутствующий токен сброса'
			});
		}

		if (!password) {
			return fail(400, {
				error: 'Укажите пароль'
			});
		}

		if (password !== confirmPassword) {
			return fail(400, {
				error: 'Пароли не совпадают'
			});
		}

		if (password.length < 8) {
			return fail(400, {
				error: 'Пароль должен содержать не менее 8 символов'
			});
		}

		try {
			const response = await fetch(`${getApiBaseUrl()}/recruiter/auth/reset-password/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					token,
					password,
					confirm_password: confirmPassword
				})
			});

			if (!response.ok) {
				const data = await response.json();
				let errorMessage = 'Не удалось сбросить пароль';
				if (data.detail) {
					errorMessage = data.detail;
				} else if (data.token) {
					errorMessage = 'Ссылка для сброса недействительна или истекла';
				} else if (data.password) {
					errorMessage = Array.isArray(data.password) ? data.password.join(', ') : data.password;
				}

				return fail(400, {
					error: errorMessage
				});
			}

			// Return success state to show confirmation UI
			return {
				success: true
			};
		} catch (error) {
			console.error('Reset password error:', error);
			return fail(500, {
				error: 'Произошла непредвиденная ошибка. Попробуйте ещё раз.'
			});
		}
	}
};
