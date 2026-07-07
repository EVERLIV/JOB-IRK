/**
 * Account Page Server Load & Actions
 * Handles profile viewing and updating
 */

import type { PageServerLoad, Actions } from './$types';
import { fail } from '@sveltejs/kit';
import { getApiBaseUrl } from '$lib/config/env';

export const load: PageServerLoad = async ({ parent }) => {
	// Get user data from parent layout
	const { user } = await parent();

	return {
		user
	};
};

export const actions: Actions = {
	/**
	 * Update profile information
	 */
	updateProfile: async ({ request, cookies, fetch }) => {
		const formData = await request.formData();

		// Build update payload
		const updates: Record<string, string> = {};
		const firstName = formData.get('first_name');
		const lastName = formData.get('last_name');
		const jobTitle = formData.get('job_title');
		const mobile = formData.get('mobile');

		if (firstName) updates.first_name = firstName.toString();
		if (lastName) updates.last_name = lastName.toString();
		if (jobTitle) updates.job_title = jobTitle.toString();
		if (mobile) updates.mobile = mobile.toString();

		try {
			// Call Django API using enhanced fetch (adds Authorization header automatically)
			const response = await fetch(`${getApiBaseUrl()}/recruiter/profile/update/`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(updates)
			});

			const result = await response.json();

			if (!response.ok) {
				return fail(response.status, {
					error: result.error || result.detail || 'Не удалось обновить профиль',
					values: updates
				});
			}

			return {
				success: true,
				message: result.message || 'Профиль успешно обновлён',
				user: result.user
			};
		} catch (error: any) {
			return fail(500, {
				error: error.message || 'Произошла сетевая ошибка',
				values: updates
			});
		}
	},

	/**
	 * Upload profile picture
	 */
	uploadPicture: async ({ request, cookies, fetch }) => {
		const formData = await request.formData();
		const file = formData.get('profile_pic');

		if (!file || !(file instanceof File)) {
			return fail(400, {
				error: 'Загрузите фото профиля'
			});
		}

		// Validate file type
		const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
		if (!allowedTypes.includes(file.type)) {
			return fail(400, {
				error: 'Недопустимый тип файла. Загрузите изображение JPEG или PNG'
			});
		}

		// Validate file size (max 2MB)
		const maxSize = 2 * 1024 * 1024;
		if (file.size > maxSize) {
			return fail(400, {
				error: 'Файл слишком большой. Максимальный размер — 2 МБ'
			});
		}

		try {
			// Forward the FormData to Django
			const response = await fetch(`${getApiBaseUrl()}/recruiter/profile/picture/`, {
				method: 'POST',
				body: formData
			});

			const result = await response.json();

			if (!response.ok) {
				return fail(response.status, {
					error: result.error || result.detail || 'Не удалось загрузить фото профиля'
				});
			}

			return {
				success: true,
				message: result.message || 'Фото профиля успешно загружено',
				user: result.user
			};
		} catch (error: any) {
			return fail(500, {
				error: error.message || 'Произошла сетевая ошибка'
			});
		}
	}
};
