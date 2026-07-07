/**
 * Authentication Store
 * Cookie-first auth state for candidate site.
 */

import { writable } from 'svelte/store';
import { goto } from '$app/navigation';
import type { User } from '$lib/api/auth';
import { logout as apiLogout } from '$lib/api/auth';

interface AuthState {
	user: User | null;
	isAuthenticated: boolean;
	isLoading: boolean;
}

function createAuthStore() {
	const initialState: AuthState = {
		user: null,
		isAuthenticated: false,
		isLoading: false
	};

	const { subscribe, set, update } = writable<AuthState>(initialState);

	return {
		subscribe,

		/**
		 * Sync store with server-derived auth state
		 */
		setAuthState: (user: User | null) => {
			set({
				user,
				isAuthenticated: Boolean(user),
				isLoading: false
			});
		},

		login: (user: User) => {
			set({
				user,
				isAuthenticated: true,
				isLoading: false
			});
		},

		/**
		 * Logout and clear all data
		 */
		logout: async () => {
			// Call API to blacklist token
			try {
				await apiLogout();
			} catch (error) {
				console.error('Logout API error:', error);
			}

			set({
				user: null,
				isAuthenticated: false,
				isLoading: false
			});

			// Redirect to home page
			goto('/');
		},

		/**
		 * Update user data
		 */
		updateUser: (user: User) => {
			update(state => ({
				...state,
				user
			}));
		},

		/**
		 * Check if user is authenticated
		 */
		checkAuth: () => {
			update(state => ({ ...state, isLoading: false }));
		},

		/**
		 * Clear auth state (used when token refresh fails)
		 */
		clearAuth: () => {
			set({
				user: null,
				isAuthenticated: false,
				isLoading: false
			});
		}
	};
}

export const authStore = createAuthStore();
