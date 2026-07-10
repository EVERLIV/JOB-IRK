<script lang="ts">
	import { CheckCircle, XCircle, Mail } from '@lucide/svelte';
	import { getContext } from 'svelte';
	import { enhance } from '$app/forms';
	import { Button, Card } from '$lib/components/ui';

	type AuthLayoutContext = {
		containerClass: string;
		mainClass: string;
	};

	let { data, form } = $props();

	const layout = getContext<AuthLayoutContext>('authLayout');
	layout.containerClass = 'max-w-lg';

	let resending = $state(false);

	let status = $derived(data.status);
	let email = $derived(data.email);
	let errorMessage = $derived(data.errorMessage);

	let resendSuccess = $derived(form?.success || false);
	let resendError = $derived(form?.error || '');
</script>

<svelte:head>
	<title>Подтверждение email - Truddy.ru Recruiter</title>
	<meta name="description" content="Подтвердите email вашего аккаунта работодателя Truddy.ru." />
</svelte:head>

<Card padding="lg" class="shadow-lg">
	{#if status === 'waiting'}
		<!-- Waiting for verification State -->
		<div class="text-center">
			<div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
				<Mail class="w-8 h-8 text-primary" />
			</div>

			<h1 class="text-2xl font-semibold text-black mb-3">Проверьте почту</h1>
			<p class="text-muted mb-6">
				Мы отправили ссылку для подтверждения на {#if email}<strong class="text-black">{email}</strong>{:else}ваш email{/if}.
				Нажмите на ссылку, чтобы подтвердить аккаунт.
			</p>

			{#if resendSuccess}
				<div class="bg-success-light border border-success/20 text-success px-4 py-3 rounded-lg text-sm mb-4">
					Письмо для подтверждения отправлено. Проверьте почту.
				</div>
			{/if}

			{#if resendError}
				<div class="bg-error-light border border-error/20 text-error px-4 py-3 rounded-lg text-sm mb-4">
					{resendError}
				</div>
			{/if}

			{#if email}
				<form method="POST" action="?/resend" use:enhance={() => {
					resending = true;
					return async ({ update }) => {
						resending = false;
						await update();
					};
				}}>
					<input type="hidden" name="email" value={email} />
					<Button type="submit" size="lg" loading={resending} class="w-full mb-4">
						{resending ? 'Отправка...' : 'Отправить письмо повторно'}
					</Button>
				</form>
			{/if}

			<a
				href="/login/"
				class="inline-block text-sm text-muted hover:text-black transition-colors"
			>
				Вернуться ко входу
			</a>
		</div>
	{:else if status === 'success'}
		<!-- Success State -->
		<div class="text-center">
			<div class="w-16 h-16 bg-success-light rounded-full flex items-center justify-center mx-auto mb-6">
				<CheckCircle class="w-8 h-8 text-success" />
			</div>

			<h1 class="text-2xl font-semibold text-black mb-3">Email подтверждён!</h1>
			<p class="text-muted mb-8">
				Адрес электронной почты успешно подтверждён. Теперь вам доступны все функции аккаунта работодателя.
			</p>

			<Button size="lg" class="w-full mb-4" onclick={() => window.location.href = '/onboarding/'}>
				Заполнить профиль
			</Button>

			<a
				href="/dashboard/"
				class="inline-block text-sm text-muted hover:text-black transition-colors"
			>
				Пропустить и перейти в кабинет
			</a>
		</div>
	{:else if status === 'expired'}
		<!-- Expired Link State -->
		<div class="text-center">
			<div class="w-16 h-16 bg-warning-light rounded-full flex items-center justify-center mx-auto mb-6">
				<Mail class="w-8 h-8 text-warning" />
			</div>

			<h1 class="text-2xl font-semibold text-black mb-3">Срок действия ссылки истёк</h1>
			<p class="text-muted mb-8">
				{errorMessage || 'Ссылка для подтверждения устарела. Запросите новое письмо для подтверждения.'}
			</p>

			{#if email}
				<form method="POST" action="?/resend" use:enhance={() => {
					resending = true;
					return async ({ update }) => {
						resending = false;
						await update();
					};
				}}>
					<input type="hidden" name="email" value={email} />
					<Button type="submit" size="lg" loading={resending} class="w-full mb-4">
						{resending ? 'Отправка...' : 'Отправить письмо повторно'}
					</Button>
				</form>
			{/if}

			<a
				href="/login/"
				class="inline-block text-sm text-muted hover:text-black transition-colors"
			>
				Вернуться ко входу
			</a>
		</div>
	{:else}
		<!-- Error State -->
		<div class="text-center">
			<div class="w-16 h-16 bg-error-light rounded-full flex items-center justify-center mx-auto mb-6">
				<XCircle class="w-8 h-8 text-error" />
			</div>

			<h1 class="text-2xl font-semibold text-black mb-3">Подтвердить email не удалось</h1>
			<p class="text-muted mb-8">
				{errorMessage || 'Не удалось подтвердить email. Ссылка может быть недействительной или уже использованной.'}
			</p>

			{#if email}
				<form method="POST" action="?/resend" use:enhance={() => {
					resending = true;
					return async ({ update }) => {
						resending = false;
						await update();
					};
				}}>
					<input type="hidden" name="email" value={email} />
					<Button type="submit" size="lg" loading={resending} class="w-full mb-4">
						{resending ? 'Отправка...' : 'Отправить письмо повторно'}
					</Button>
				</form>
			{/if}

			<a
				href="/login/"
				class="inline-block text-sm text-muted hover:text-black transition-colors"
			>
				Вернуться ко входу
			</a>
		</div>
	{/if}
</Card>
