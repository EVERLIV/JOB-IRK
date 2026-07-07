import { fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getApiBaseUrl } from '$lib/config/env';
import { setAuthCookies } from '$lib/server/auth';

export const load: PageServerLoad = async ({ url, cookies, fetch }) => {
	const token = url.searchParams.get('token');
	const email = url.searchParams.get('email') || '';

	// If no token, just show the waiting for verification state
	if (!token) {
		return {
			status: 'waiting' as const,
			email,
			errorMessage: ''
		};
	}

	// Verify the email with the token
	try {
		const response = await fetch(`${getApiBaseUrl()}/recruiter/auth/verify-email/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ token })
		});

		const data = await response.json();

		if (!response.ok) {
			// Check if token is expired or invalid
			const errorMessage = data.detail || data.message || 'Не удалось подтвердить email';
			const normalizedMessage = errorMessage.toLowerCase();
			const isExpired =
				normalizedMessage.includes('expired') ||
				normalizedMessage.includes('invalid') ||
				normalizedMessage.includes('устар') ||
				normalizedMessage.includes('недейств');

			return {
				status: isExpired ? 'expired' as const : 'error' as const,
				email,
				errorMessage
			};
		}

		const secureCookies = url.protocol === 'https:';
		setAuthCookies(cookies, data, secureCookies);

		return {
			status: 'success' as const,
			email,
			errorMessage: ''
		};
	} catch (error) {
		console.error('Email verification error:', error);
		return {
			status: 'error' as const,
			email,
			errorMessage: 'Во время подтверждения произошла непредвиденная ошибка.'
		};
	}
};

export const actions: Actions = {
	resend: async ({ request, fetch }) => {
		const formData = await request.formData();
		const email = formData.get('email')?.toString() || '';

		if (!email) {
			return fail(400, {
				error: 'Укажите email',
				success: false
			});
		}

		try {
			const response = await fetch(`${getApiBaseUrl()}/recruiter/auth/resend-verification/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email })
			});

			if (!response.ok) {
				const data = await response.json();
				return fail(400, {
					error: data.detail || data.message || 'Не удалось повторно отправить письмо для подтверждения',
					success: false
				});
			}

			return {
				success: true,
				message: 'Письмо для подтверждения отправлено. Проверьте почту.'
			};
		} catch (error) {
			console.error('Resend verification error:', error);
			return fail(500, {
				error: 'Произошла непредвиденная ошибка. Попробуйте снова.',
				success: false
			});
		}
	}
};
