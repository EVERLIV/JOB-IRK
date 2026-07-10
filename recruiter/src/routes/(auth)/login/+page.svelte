<script lang="ts">
	import { untrack } from 'svelte';
	import { Mail, Lock, Eye, EyeOff, Briefcase, Users, BarChart3, MessageSquare, Shield, Clock, CheckCircle } from '@lucide/svelte';
	import { getContext } from 'svelte';
	import { enhance } from '$app/forms';
	import { Button, Input, Card, FormField } from '$lib/components/ui';
	import { JOBSEEKER_URL } from '$lib/config/brand';

	type AuthLayoutContext = {
		containerClass: string;
		mainClass: string;
	};

	let { data, form } = $props();

	const layout = getContext<AuthLayoutContext>('authLayout');
	layout.containerClass = 'max-w-6xl';
	layout.mainClass = 'flex justify-center items-start py-8 px-4 sm:px-6 lg:px-8';

	let showPassword = $state(false);
	let rememberMe = $state(false);
	let loading = $state(false);

	let error = $derived(form?.error || '');
	let emailValue = $state(untrack(() => form?.email || ''));
</script>

<svelte:head>
	<title>Вход - Truddy.ru Recruiter</title>
	<meta name="description" content="Войдите в аккаунт работодателя Truddy.ru, чтобы управлять вакансиями и работать с кандидатами." />
</svelte:head>

<div class="w-full">
	<div class="grid lg:grid-cols-2 gap-12 items-start">
		<!-- Left Column: Marketing Content -->
		<div class="space-y-8 lg:sticky lg:top-8 hidden lg:block">
			<!-- Hero Section -->
			<div>
				<h1 class="text-3xl xl:text-4xl font-semibold text-black mb-4 leading-tight">
					С возвращением в Truddy.ru
				</h1>
				<p class="text-base xl:text-lg text-muted leading-relaxed">
					Продолжайте управлять вакансиями и находить сильных кандидатов.
				</p>
			</div>

			<!-- Key Statistics -->
			<div class="grid grid-cols-2 gap-4">
				<div class="bg-primary/5 border border-primary/20 rounded-lg p-5 text-center">
					<div class="text-2xl font-semibold text-primary mb-1">100k+</div>
					<p class="text-sm text-muted font-medium">Активных соискателей</p>
				</div>
				<div class="bg-success-light border border-success/20 rounded-lg p-5 text-center">
					<div class="text-2xl font-semibold text-success mb-1">1000+</div>
					<p class="text-sm text-muted font-medium">Откликов в день</p>
				</div>
				<div class="bg-primary/5 border border-primary/20 rounded-lg p-5 text-center">
					<div class="text-2xl font-semibold text-primary mb-1">500+</div>
					<p class="text-sm text-muted font-medium">Компаний доверяют нам</p>
				</div>
				<div class="bg-warning-light border border-warning/20 rounded-lg p-5 text-center">
					<div class="text-2xl font-semibold text-warning mb-1">24/7</div>
					<p class="text-sm text-muted font-medium">Поддержка экспертов</p>
				</div>
			</div>

			<!-- Dashboard Features -->
			<Card padding="lg" class="shadow-md">
				<h3 class="text-xl font-semibold text-black mb-6 flex items-center gap-2">
					<BarChart3 class="w-5 h-5 text-primary" />
					Ваш кабинет уже ждёт
				</h3>
				<div class="space-y-5">
					<div class="flex items-start gap-4">
						<div class="bg-primary/10 rounded-full p-2.5 flex-shrink-0">
							<Briefcase class="w-5 h-5 text-primary" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Управляйте вакансиями</h4>
							<p class="text-sm text-muted leading-relaxed">Просматривайте и редактируйте все активные публикации в одном месте</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<div class="bg-success-light rounded-full p-2.5 flex-shrink-0">
							<Users class="w-5 h-5 text-success" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Просматривайте кандидатов</h4>
							<p class="text-sm text-muted leading-relaxed">Оценивайте подходящих специалистов и их подробные профили</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<div class="bg-primary/10 rounded-full p-2.5 flex-shrink-0">
							<BarChart3 class="w-5 h-5 text-primary" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Следите за результатами</h4>
							<p class="text-sm text-muted leading-relaxed">Контролируйте просмотры, отклики и метрики найма</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<div class="bg-warning-light rounded-full p-2.5 flex-shrink-0">
							<MessageSquare class="w-5 h-5 text-warning" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Общайтесь с кандидатами</h4>
							<p class="text-sm text-muted leading-relaxed">Пишите кандидатам и назначайте интервью</p>
						</div>
					</div>
				</div>
			</Card>
		</div>

		<!-- Right Column: Login Form -->
		<Card padding="lg" class="shadow-lg">
			<!-- Header -->
			<div class="text-center mb-8">
				<h2 class="text-2xl font-semibold text-black">С возвращением</h2>
				<p class="text-muted mt-2">Войдите в аккаунт работодателя</p>
			</div>

			<!-- Login Form -->
			<form method="POST" use:enhance={() => {
				loading = true;
				return async ({ update }) => {
					loading = false;
					await update();
				};
			}} class="space-y-5">
				<!-- Hidden field for redirect URL -->
				<input type="hidden" name="redirect_to" value={data.redirectTo} />

				<!-- Error Message -->
				{#if error}
					<div class="bg-error-light border border-error/20 text-error px-4 py-3 rounded-lg text-sm whitespace-pre-line">
						{error}
					</div>
				{/if}

				<FormField label="Email">
					<Input
						type="email"
						id="email"
						name="email"
						value={emailValue}
						required
						disabled={loading}
						placeholder="name@company.com"
						size="lg"
					>
						{#snippet iconLeft()}
							<Mail class="w-5 h-5" />
						{/snippet}
					</Input>
				</FormField>

				<FormField label="Пароль">
					<div class="relative">
						<Input
							type={showPassword ? 'text' : 'password'}
							id="password"
							name="password"
							required
							disabled={loading}
							placeholder="Введите пароль"
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
							disabled={loading}
							class="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-black transition-colors disabled:opacity-50"
							aria-label={showPassword ? 'Скрыть пароль' : 'Показать пароль'}
						>
							{#if showPassword}
								<EyeOff class="w-5 h-5" />
							{:else}
								<Eye class="w-5 h-5" />
							{/if}
						</button>
					</div>
				</FormField>

				<div class="flex items-center justify-between">
					<label class="flex items-center gap-2 cursor-pointer group">
						<input
							type="checkbox"
							name="remember_me"
							bind:checked={rememberMe}
							class="w-4 h-4 text-primary border-border rounded focus:ring-primary/20 focus:ring-2"
						/>
						<span class="text-sm text-muted group-hover:text-black transition-colors">Запомнить меня</span>
					</label>

					<a href="/forgot-password/" class="text-sm font-medium text-primary hover:text-primary-hover transition-colors">
						Забыли пароль?
					</a>
				</div>

				<Button type="submit" size="lg" {loading} class="w-full">
					{#if loading}
						Вход...
					{:else}
						Войти
					{/if}
				</Button>
			</form>

			<!-- Sign Up Link -->
			<p class="mt-6 text-center text-sm text-muted">
				Нет аккаунта?
				<a href="/signup/" class="font-medium text-primary hover:text-primary-hover transition-colors">Зарегистрироваться бесплатно</a>
			</p>

			<!-- Job Seeker Link -->
			<div class="mt-5 pt-5 border-t border-border">
				<p class="text-center text-sm text-muted">
					Ищете работу?
					<a href="{JOBSEEKER_URL}/login/" class="font-medium text-primary hover:text-primary-hover transition-colors">
						Вход для соискателя
					</a>
				</p>
			</div>

			<!-- Trust Indicators -->
			<div class="mt-5 pt-5 border-t border-border">
				<div class="flex justify-center flex-wrap gap-4 text-xs text-muted">
					<div class="flex items-center gap-1.5">
						<Shield class="w-3.5 h-3.5" />
						<span>SSL-шифрование</span>
					</div>
					<div class="flex items-center gap-1.5">
						<CheckCircle class="w-3.5 h-3.5" />
						<span>Соответствие GDPR</span>
					</div>
					<div class="flex items-center gap-1.5">
						<Clock class="w-3.5 h-3.5" />
						<span>Поддержка 24/7</span>
					</div>
				</div>
			</div>
		</Card>
	</div>
</div>
