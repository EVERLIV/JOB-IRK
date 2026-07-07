/**
 * Server-side load function for jobs page
 * Handles data fetching with proper authentication
 */
import type { PageServerLoad, Actions } from './$types';
import { error, redirect } from '@sveltejs/kit';
import type { JobsListResponse } from '$lib/types';
import { getApiBaseUrl } from '$lib/config/env';
import { clearAuthCookies } from '$lib/server/auth';

export const load: PageServerLoad = async ({ fetch, url, cookies }) => {
	// Check authentication
	const accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');

	if (!accessToken && !refreshToken) {
		throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
	}

	// Get query parameters
	const page = url.searchParams.get('page') || '1';
	const status = url.searchParams.get('status') || '';
	const search = url.searchParams.get('search') || '';
	const page_size = url.searchParams.get('page_size') || '20';

	try {
		// Build API URL with query parameters
		const params = new URLSearchParams({
			page,
			page_size,
			ordering: '-created_on'
		});

		if (status && status !== 'all') {
			params.append('status', status);
		}

		if (search) {
			params.append('search', search);
		}

		// Make API request - fetch will use hooks.server.ts to add Authorization header
		const apiUrl = `${getApiBaseUrl()}/recruiter/jobs/?${params.toString()}`;
		const response = await fetch(apiUrl);

		if (!response.ok) {
			if (response.status === 401) {
				// Clear invalid tokens and redirect to login
				clearAuthCookies(cookies);
				throw redirect(302, '/login?redirect=' + encodeURIComponent(url.pathname));
			}
			throw error(response.status, `Не удалось загрузить вакансии: ${response.statusText}`);
		}

		const data: JobsListResponse = await response.json();

		return {
			jobs: data.results,
			count: data.count,
			next: data.next,
			previous: data.previous,
			currentPage: parseInt(page),
			filters: {
				status: status || 'all',
				search: search || ''
			}
		};
	} catch (err: any) {
		console.error('Error loading jobs:', err);

		// If it's already a redirect, re-throw it
		if (err.status === 302) {
			throw err;
		}

		throw error(500, err.message || 'Не удалось загрузить вакансии');
	}
};

export const actions: Actions = {
	/**
	 * Publish a draft job
	 */
	publish: async ({ request, fetch, cookies }) => {
		const formData = await request.formData();
		const jobId = formData.get('jobId');

		if (!jobId) {
			return { success: false, error: 'Не указан ID вакансии' };
		}

		try {
			const response = await fetch(`${getApiBaseUrl()}/recruiter/jobs/${jobId}/publish/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				return {
					success: false,
					error: errorData.error || 'Не удалось опубликовать вакансию'
				};
			}

			return { success: true };
		} catch (err: any) {
			return { success: false, error: err.message || 'Не удалось опубликовать вакансию' };
		}
	},

	/**
	 * Close an active job
	 */
	close: async ({ request, fetch }) => {
		const formData = await request.formData();
		const jobId = formData.get('jobId');

		if (!jobId) {
			return { success: false, error: 'Не указан ID вакансии' };
		}

		try {
			const response = await fetch(`${getApiBaseUrl()}/recruiter/jobs/${jobId}/close/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				return {
					success: false,
					error: errorData.error || 'Не удалось закрыть вакансию'
				};
			}

			return { success: true };
		} catch (err: any) {
			return { success: false, error: err.message || 'Не удалось закрыть вакансию' };
		}
	},

	/**
	 * Delete a job
	 */
	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const jobId = formData.get('jobId');

		if (!jobId) {
			return { success: false, error: 'Не указан ID вакансии' };
		}

		try {
			const response = await fetch(`${getApiBaseUrl()}/recruiter/jobs/${jobId}/delete/?force=true`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				return {
					success: false,
					error: errorData.error || 'Не удалось удалить вакансию'
				};
			}

			return { success: true };
		} catch (err: any) {
			return { success: false, error: err.message || 'Не удалось удалить вакансию' };
		}
	}
};
