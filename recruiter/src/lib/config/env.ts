/**
 * Environment Configuration
 * Centralized access to environment variables
 *
 * Uses dynamic public env so Vercel builds succeed before env vars are configured.
 * Set PUBLIC_* in Vercel Project → Settings → Environment Variables to override.
 */

import { env } from '$env/dynamic/public';
import { dev } from '$app/environment';

const localDefaults = {
	PUBLIC_API_BASE_URL: 'http://localhost:8000/api/v1',
	PUBLIC_SITE_URL: 'http://localhost:5174',
	PUBLIC_JOBSEEKER_URL: 'http://localhost:5173'
} as const;

const productionDefaults = {
	PUBLIC_API_BASE_URL: 'https://api-production-e35c.up.railway.app/api/v1',
	PUBLIC_SITE_URL: 'https://job-irk-recruiter.vercel.app',
	PUBLIC_JOBSEEKER_URL: 'https://job-irk.vercel.app'
} as const;

const defaults = dev ? localDefaults : productionDefaults;

function clean(value: string | undefined, fallback: string): string {
	// Vercel env paste on Windows sometimes stores trailing \r\n
	return (value ?? fallback).replace(/[\r\n]+/g, '').trim();
}

export const API_BASE_URL = clean(env.PUBLIC_API_BASE_URL, defaults.PUBLIC_API_BASE_URL);

export const SITE_URL = clean(env.PUBLIC_SITE_URL, defaults.PUBLIC_SITE_URL);

export const JOBSEEKER_URL = clean(env.PUBLIC_JOBSEEKER_URL, defaults.PUBLIC_JOBSEEKER_URL);

export const isDevelopment = dev;

export const isProduction = !dev;

export function getApiBasePath(): string {
	if (typeof window !== 'undefined') {
		return '/api/v1';
	}
	return API_BASE_URL;
}

export function getApiBaseUrl(): string {
	return API_BASE_URL;
}
