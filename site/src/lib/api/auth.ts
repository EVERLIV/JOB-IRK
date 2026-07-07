/**
 * Authentication API
 * Candidate auth API with cookie-first session handling.
 */

import { ApiClient } from './client';

// Types (will be replaced with auto-generated types later)
export interface User {
	id: number;
	email: string;
	username: string;
	first_name: string;
	last_name: string;
	user_type: string;
	profile_completion_percentage: number;
	is_gp_connected: boolean;
	photo?: string;
	profile_pic?: string;
	mobile?: string;
	gender?: string;
	is_active: boolean;
	date_joined: string;
}

export interface AuthResponse {
	user: User;
	requires_profile_completion: boolean;
	redirect_to: string;
	is_new_user: boolean;
	message?: string;
}

export interface GoogleAuthUrlResponse {
	auth_url: string;
	user_type: string;
	state: string;
}

/**
 * Get Google OAuth URL for frontend to redirect to
 */
export async function getGoogleAuthUrl(redirectUri: string): Promise<GoogleAuthUrlResponse> {
	const endpoint = `/auth/google/url/?redirect_uri=${encodeURIComponent(redirectUri)}`;
	return ApiClient.get<GoogleAuthUrlResponse>(endpoint, true); // Skip auth - public endpoint
}

/**
 * Exchange Google authorization code for JWT tokens
 * Returns access and refresh tokens in response body
 */
export async function googleAuthCallback(
	code: string,
	redirectUri: string,
	state: string
): Promise<AuthResponse> {
	return ApiClient.post<AuthResponse>('/auth/google/callback/', {
		code,
		redirect_uri: redirectUri,
		state
	}, true); // Skip auth - public endpoint
}

export async function login(email: string, password: string): Promise<AuthResponse> {
	return ApiClient.post<AuthResponse>('/auth/login/', { email, password }, true);
}

/**
 * Get current authenticated user
 */
export async function getCurrentUser(): Promise<User> {
	return ApiClient.get<User>('/auth/me/');
}

/**
 * Logout - blacklist refresh token
 */
export async function logout(): Promise<void> {
	await ApiClient.post('/auth/logout/', {});
}

/**
 * Disconnect Google account
 */
export async function disconnectGoogle(): Promise<void> {
	await ApiClient.post('/auth/google/disconnect/', {});
}
