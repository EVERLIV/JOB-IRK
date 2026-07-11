<script lang="ts">
	import { Lock, Eye, EyeOff, CheckCircle } from '@lucide/svelte';
	import { getContext } from 'svelte';
	import { enhance } from '$app/forms';
	import { Button, Input, Card, FormField } from '$lib/components/ui';

	type AuthLayoutContext = {
		containerClass: string;
		mainClass: string;
	};

	let { data, form } = $props();

	const layout = getContext<AuthLayoutContext>('authLayout');
	layout.containerClass = 'max-w-lg';

	let showPassword = $state(false);
	let showConfirmPassword = $state(false);
	let loading = $state(false);

	let formData = $state({
		password: '',
		confirmPassword: ''
	});

	let isSubmitted = $derived(form?.success || false);
	let error = $derived(form?.error || '');

	function validatePassword(password: string) {
		return {
			minLength: password.length >= 8,
			hasUpper: /[A-Z]/.test(password),
			hasLower: /[a-z]/.test(password),
			hasNumber: /\d/.test(password)
		};
	}

	let validation = $derived(validatePassword(formData.password));
	let isValid = $derived(validation.minLength && validation.hasUpper && validation.hasLower && validation.hasNumber && formData.password === formData.confirmPassword);
</script>

<svelte:head>
	<title>Сброс пароля - Truddy.ru Recruiter</title>
	<meta name="description" content="Создайте новый пароль для аккаунта работодателя Truddy.ru." />
</svelte:head>

<Card padding="lg" class="shadow-lg">
	{#if !isSubmitted}
		<!-- Reset Password Form -->
		<div>
			<!-- Header -->
			<div class="mb-8">
				<h1 class="text-2xl font-semibold text-black">Сброс пароля</h1>
				<p class="text-muted mt-2">Создайте новый пароль для своего аккаунта</p>
			</div>

			<!-- Form -->
			<form method="POST" use:enhance={() => {
				loading = true;
				return async ({ update }) => {
					loading = false;
					await update();
				};
			}} class="space-y-6">
				<!-- Hidden field for token -->
				<input type="hidden" name="token" value={data.token} />

				{#if error}
					<div class="bg-error-light border border-error/20 text-error px-4 py-3 rounded-lg text-sm">
						{error}
					</div>
				{/if}

				<FormField label="Новый пароль">
					<div class="relative">
						<Input
							type={showPassword ? 'text' : 'password'}
							id="password"
							name="password"
							bind:value={formData.password}
							required
							disabled={loading}
							placeholder="Создайте надёжный пароль"
							size="lg"
							class="pr-12"
						>
							{#snippet iconLeft()}
								<Lock class="w-5 h-5" />
							{/snippet}
						</Input>
						<button
							type="button"
							onclick={() => (showPassword = !showPassword)}
							class="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-black transition-colors"
							aria-label={showPassword ? 'Скрыть пароль' : 'Показать пароль'}
						>
							{#if showPassword}
								<EyeOff class="w-5 h-5" />
							{:else}
								<Eye class="w-5 h-5" />
							{/if}
						</button>
					</div>

					<!-- Password Requirements -->
					{#if formData.password}
						<div class="mt-3 space-y-2">
							<p class="text-xs font-medium text-black">Пароль должен содержать:</p>
							<div class="space-y-1">
								<div class="flex items-center gap-2 text-xs {validation.minLength ? 'text-success' : 'text-muted'}">
									<div class="w-4 h-4 rounded-full border-2 {validation.minLength ? 'border-success bg-success' : 'border-border'} flex items-center justify-center">
										{#if validation.minLength}
											<CheckCircle class="w-3 h-3 text-white" />
										{/if}
									</div>
									Не менее 8 символов
								</div>
								<div class="flex items-center gap-2 text-xs {validation.hasUpper ? 'text-success' : 'text-muted'}">
									<div class="w-4 h-4 rounded-full border-2 {validation.hasUpper ? 'border-success bg-success' : 'border-border'} flex items-center justify-center">
										{#if validation.hasUpper}
											<CheckCircle class="w-3 h-3 text-white" />
										{/if}
									</div>
									Одну заглавную букву
								</div>
								<div class="flex items-center gap-2 text-xs {validation.hasLower ? 'text-success' : 'text-muted'}">
									<div class="w-4 h-4 rounded-full border-2 {validation.hasLower ? 'border-success bg-success' : 'border-border'} flex items-center justify-center">
										{#if validation.hasLower}
											<CheckCircle class="w-3 h-3 text-white" />
										{/if}
									</div>
									Одну строчную букву
								</div>
								<div class="flex items-center gap-2 text-xs {validation.hasNumber ? 'text-success' : 'text-muted'}">
									<div class="w-4 h-4 rounded-full border-2 {validation.hasNumber ? 'border-success bg-success' : 'border-border'} flex items-center justify-center">
										{#if validation.hasNumber}
											<CheckCircle class="w-3 h-3 text-white" />
										{/if}
									</div>
									Одну цифру
								</div>
							</div>
						</div>
					{/if}
				</FormField>

				<FormField label="Подтвердите пароль" error={formData.confirmPassword && formData.password !== formData.confirmPassword ? 'Пароли не совпадают' : undefined}>
					<div class="relative">
						<Input
							type={showConfirmPassword ? 'text' : 'password'}
							id="confirmPassword"
							name="confirm_password"
							bind:value={formData.confirmPassword}
							required
							disabled={loading}
							placeholder="Повторите пароль"
							size="lg"
							error={Boolean(formData.confirmPassword && formData.password !== formData.confirmPassword)}
							class="pr-12"
						>
							{#snippet iconLeft()}
								<Lock class="w-5 h-5" />
							{/snippet}
						</Input>
						<button
							type="button"
							onclick={() => (showConfirmPassword = !showConfirmPassword)}
							class="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-black transition-colors"
							aria-label={showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'}
						>
							{#if showConfirmPassword}
								<EyeOff class="w-5 h-5" />
							{:else}
								<Eye class="w-5 h-5" />
							{/if}
						</button>
					</div>
				</FormField>

				<Button type="submit" size="lg" {loading} disabled={loading || !isValid} class="w-full">
					{loading ? 'Сброс...' : 'Сбросить пароль'}
				</Button>
			</form>
		</div>
	{:else}
		<!-- Success Message -->
		<div class="text-center">
			<div class="w-16 h-16 bg-success-light rounded-full flex items-center justify-center mx-auto mb-6">
				<CheckCircle class="w-8 h-8 text-success" />
			</div>

			<h1 class="text-2xl font-semibold text-black mb-3">Пароль успешно изменён!</h1>
			<p class="text-muted mb-8">
				Ваш пароль успешно сброшен. Теперь вы можете войти с новым паролем.
			</p>

			<Button size="lg" class="w-full" onclick={() => window.location.href = '/login/'}>
				Войти
			</Button>
		</div>
	{/if}
</Card>
