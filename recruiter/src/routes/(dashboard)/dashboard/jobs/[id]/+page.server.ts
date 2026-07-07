import { error, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { API_BASE_URL } from '$lib/config/env';

export const load: PageServerLoad = async ({ params, cookies, fetch }) => {
	const jobId = params.id;

	// Get JWT token from cookies
	const accessToken = cookies.get('access_token');

	if (!accessToken) {
		throw error(401, 'Не авторизован');
	}

	try {
		// Fetch job details
		const jobResponse = await fetch(`${API_BASE_URL}/recruiter/jobs/${jobId}/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		if (!jobResponse.ok) {
			if (jobResponse.status === 404) {
				throw error(404, 'Вакансия не найдена');
			}
			throw error(jobResponse.status, 'Не удалось загрузить данные вакансии');
		}

		const job = await jobResponse.json();

		// Fetch applicants summary
		const applicantsResponse = await fetch(`${API_BASE_URL}/recruiter/jobs/${jobId}/applicants/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		let applicantsData = {
			total_applicants: 0,
			stats: {
				pending: 0,
				shortlisted: 0,
				selected: 0,
				rejected: 0
			}
		};

		if (applicantsResponse.ok) {
			applicantsData = await applicantsResponse.json();
		}

		// Fetch job analytics (30-day period)
		const analyticsResponse = await fetch(`${API_BASE_URL}/recruiter/jobs/${jobId}/analytics/?period=30d`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		let analytics = null;
		if (analyticsResponse.ok) {
			analytics = await analyticsResponse.json();
		}

		return {
			job,
			applicantsStats: applicantsData.stats,
			totalApplicants: applicantsData.total_applicants,
			analytics
		};
	} catch (err: any) {
		console.error('Error loading job details:', err);
		throw error(500, err.message || 'Не удалось загрузить данные вакансии');
	}
};

export const actions: Actions = {
	/**
	 * Toggle email notifications for job applicants
	 */
	toggleNotifications: async ({ params, cookies, fetch }) => {
		const jobId = params.id;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return fail(401, { error: 'Не авторизован' });
		}

		try {
			// First, get current job state
			const jobResponse = await fetch(`${API_BASE_URL}/recruiter/jobs/${jobId}/`, {
				headers: {
					Authorization: `Bearer ${accessToken}`
				}
			});

			if (!jobResponse.ok) {
				return fail(jobResponse.status, { error: 'Не удалось загрузить данные вакансии' });
			}

			const job = await jobResponse.json();

			// Toggle the notification setting
			const newNotificationState = !job.send_email_notifications;

			// Update the job
			const updateResponse = await fetch(`${API_BASE_URL}/recruiter/jobs/${jobId}/update/`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${accessToken}`
				},
				body: JSON.stringify({
					send_email_notifications: newNotificationState
				})
			});

			if (!updateResponse.ok) {
				const errorData = await updateResponse.json();
				return fail(updateResponse.status, {
					error: errorData.error || 'Не удалось обновить настройки уведомлений'
				});
			}

			return {
				success: true,
				message: newNotificationState
					? 'Email-уведомления включены'
					: 'Email-уведомления отключены'
			};
		} catch (err: any) {
			console.error('Error toggling notifications:', err);
			return fail(500, { error: err.message || 'Не удалось изменить настройки уведомлений' });
		}
	}
};
