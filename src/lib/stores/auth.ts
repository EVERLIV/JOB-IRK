/**
 * Authentication Store for Recruiters
 * Manages user authentication state across the app
 *
 * SECURITY NOTE:
 * - JWT tokens are stored in HttpOnly cookies (NOT accessible to JavaScript)
 * - User state should come from SSR/layout loads, not browser storage.
 */

import { writable } from 'svelte/store';
import { goto } from '$app/navigation';
import type { User } from '$lib/types';
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

		setAuthState: (user: User | null) => {
			set({
				user,
				isAuthenticated: Boolean(user),
				isLoading: false
			});
		},

		/**
		 * Sync store after a successful server-authenticated login.
		 */
		login: async (user: User) => {
			set({
				user,
				isAuthenticated: true,
				isLoading: false
			});
		},

		/**
		 * Logout and clear all data
		 * Clears HttpOnly cookies via SvelteKit server endpoint
		 */
		logout: async () => {
			set({
				user: null,
				isAuthenticated: false,
				isLoading: false
			});

			try {
				await apiLogout();
			} catch (error) {
				console.log('Logout API call failed:', error);
			}

			// Redirect to login page
			goto('/login');
		},

		/**
		 * Update user data
		 */
		updateUser: (user: User) => {
			update((state) => ({
				...state,
				user
			}));
		},

		/**
		 * Check if user is authenticated
		 */
		checkAuth: () => {
			update((state) => ({ ...state, isLoading: false }));
		},

		/**
		 * Clear authentication state (for errors)
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
