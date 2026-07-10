<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { Loader2, AlertCircle, CheckCircle2 } from '@lucide/svelte';
	import { googleAuthCallback } from '$lib/api/auth';
	import { authStore } from '$lib/stores/auth';

	let status: 'loading' | 'success' | 'error' = 'loading';
	let errorMessage = '';
	let redirectPath = '/';

	onMount(async () => {
		const code = $page.url.searchParams.get('code');
		const error = $page.url.searchParams.get('error');

		// Handle OAuth errors from Google
		if (error) {
			status = 'error';
			errorMessage = getOAuthErrorMessage(error);
			setTimeout(() => {
				goto('/login?error=' + error);
			}, 3000);
			return;
		}

		// No authorization code
		if (!code) {
			status = 'error';
			errorMessage = 'Код авторизации от Google не получен.';
			setTimeout(() => {
				goto('/login?error=no_code');
			}, 3000);
			return;
		}

		// Exchange code for tokens (tokens set in HttpOnly cookies by server)
		try {
			const redirectUri = window.location.origin + '/auth/google/callback';

			const state = $page.url.searchParams.get('state');
			if (!state) {
				throw new Error('Отсутствует параметр состояния OAuth.');
			}
			const response = await googleAuthCallback(code, redirectUri, state);

			authStore.login(response.user);

			status = 'success';
			redirectPath = response.redirect_to || '/';

			// Show success message briefly then redirect
			setTimeout(() => {
				goto(redirectPath);
			}, 1500);
		} catch (err) {
			status = 'error';
			errorMessage = err instanceof Error ? err.message : 'Ошибка авторизации. Попробуйте снова.';

			setTimeout(() => {
				goto('/login?error=auth_failed');
			}, 3000);
		}
	});

	function getOAuthErrorMessage(error: string): string {
		const errorMessages: Record<string, string> = {
			access_denied: 'Вы отказали в доступе. Попробуйте снова и авторизуйте приложение.',
			invalid_request: 'Недействительный запрос. Попробуйте снова.',
			unauthorized_client: 'Приложение не авторизовано. Обратитесь в поддержку.',
			unsupported_response_type: 'Ошибка конфигурации. Обратитесь в поддержку.',
			invalid_scope: 'Запрошены недействительные разрешения. Обратитесь в поддержку.',
			server_error: 'Ошибка сервера Google. Попробуйте позже.',
			temporarily_unavailable: 'Сервис временно недоступен. Попробуйте позже.'
		};

		return errorMessages[error] || 'Произошла ошибка авторизации. Попробуйте снова.';
	}
</script>

<svelte:head>
	<title>Авторизация - Truddy.ru</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
	<div class="max-w-md w-full">
		<div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
			{#if status === 'loading'}
				<!-- Loading State -->
				<div class="text-center">
					<div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-6">
						<Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
					</div>
					<h2 class="text-2xl font-semibold text-gray-900 mb-2">Авторизация...</h2>
					<p class="text-gray-600">
						Пожалуйста, подождите, пока мы безопасно выполняем вход через Google.
					</p>
					<div class="mt-6 flex justify-center">
						<div class="flex space-x-2">
							<div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
							<div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
							<div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
						</div>
					</div>
				</div>
			{:else if status === 'success'}
				<!-- Success State -->
				<div class="text-center">
					<div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
						<CheckCircle2 class="w-8 h-8 text-green-600" />
					</div>
					<h2 class="text-2xl font-semibold text-gray-900 mb-2">Успешно!</h2>
					<p class="text-gray-600">
						Авторизация прошла успешно.
					</p>
					<p class="text-sm text-gray-500 mt-4">
						Перенаправление...
					</p>
				</div>
			{:else}
				<!-- Error State -->
				<div class="text-center">
					<div class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-6">
						<AlertCircle class="w-8 h-8 text-red-600" />
					</div>
					<h2 class="text-2xl font-semibold text-gray-900 mb-2">Ошибка авторизации</h2>
					<p class="text-gray-600 mb-4">
						{errorMessage}
					</p>
					<p class="text-sm text-gray-500">
						Перенаправление на страницу входа...
					</p>
				</div>
			{/if}
		</div>

		<!-- Security Note -->
		<div class="mt-6 text-center text-sm text-gray-500">
			<p>Защищено шифрованием корпоративного уровня</p>
		</div>
	</div>
</div>

<style>
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.bg-white {
		animation: fadeIn 0.6s ease-out;
	}
</style>
