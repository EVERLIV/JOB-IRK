import type { RequestEvent } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib/config/env';
import { setAuthCookies } from '$lib/server/auth';

export async function proxyApiRequest(event: RequestEvent): Promise<Response> {
	const path = event.params.path ?? '';
	const apiPath = path.endsWith('/') ? path : `${path}/`;
	const targetUrl = new URL(`${API_BASE_URL}/${apiPath}`);
	targetUrl.search = event.url.search;

	const accessToken = event.cookies.get('access_token');
	const refreshToken = event.cookies.get('refresh_token');
	const secureCookies = event.url.protocol === 'https:';

	const headers = new Headers();
	const contentType = event.request.headers.get('content-type');
	if (contentType) {
		headers.set('Content-Type', contentType);
	}
	if (accessToken) {
		headers.set('Authorization', `Bearer ${accessToken}`);
	}

	const method = event.request.method;
	let body: BodyInit | undefined;

	if (method !== 'GET' && method !== 'HEAD') {
		body = await event.request.arrayBuffer();
	}

	if ((apiPath === 'auth/token/refresh/' || path === 'auth/token/refresh') && method === 'POST' && refreshToken) {
		body = JSON.stringify({ refresh: refreshToken });
		headers.set('Content-Type', 'application/json');
	}

	const apiResponse = await fetch(targetUrl, { method, headers, body });

	if ((apiPath === 'auth/token/refresh/' || path === 'auth/token/refresh') && method === 'POST' && apiResponse.ok) {
		const data = await apiResponse.json();
		const response = Response.json(data, { status: apiResponse.status });
		setAuthCookies(
			event.cookies,
			{ access: data.access, refresh: data.refresh },
			secureCookies
		);
		return response;
	}

	const responseHeaders = new Headers();
	const apiContentType = apiResponse.headers.get('Content-Type');
	if (apiContentType) {
		responseHeaders.set('Content-Type', apiContentType);
	}

	return new Response(apiResponse.body, {
		status: apiResponse.status,
		headers: responseHeaders
	});
}
