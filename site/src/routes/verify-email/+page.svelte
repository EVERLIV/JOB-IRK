<script>
  import { untrack } from 'svelte';
  import { goto } from '$app/navigation';
  import { Mail, CheckCircle, XCircle, Loader2, RefreshCw, Clock } from '@lucide/svelte';
  import { enhance } from '$app/forms';
  import BrandLogo from '$lib/components/BrandLogo.svelte';

  /** @type {{ data?: { status?: string; message?: string; email?: string }; form?: { success?: boolean; message?: string } }} */
  let { data, form } = $props();

  // Initial state (will be updated by $effect when data changes)
  let verificationStatus = $state(untrack(() => data?.status || 'pending'));
  let email = $state(untrack(() => data?.email || ''));
  let isResending = $state(false);
  let resendSuccess = $state(false);
  let errorMessage = $state(untrack(() => data?.message || ''));

  // Update state when data changes
  $effect(() => {
    if (data?.status) {
      verificationStatus = data.status;
    }
    if (data?.email) {
      email = data.email;
    }
    if (data?.message && data.status !== 'success') {
      errorMessage = data.message;
    }
  });

  // Handle resend form result
  $effect(() => {
    if (form?.success) {
      resendSuccess = true;
      errorMessage = '';
    } else if (form?.message) {
      errorMessage = form.message;
    }
    isResending = false;
  });

  // Redirect on success after delay
  $effect(() => {
    if (verificationStatus === 'success') {
      setTimeout(() => {
        goto('/');
      }, 3000);
    }
  });
</script>

<svelte:head>
  <title>Подтверждение email - Truddy.ru</title>
  <meta name="description" content="Подтвердите ваш email на Truddy.ru" />
</svelte:head>

<div class="min-h-screen bg-surface flex items-center justify-center p-6">
  <div class="w-full max-w-md">
    <!-- Logo -->
    <div class="text-center mb-8 animate-fade-in-down" style="opacity: 0; animation-fill-mode: forwards;">
      <BrandLogo href="/" size="lg" class="justify-center" />
    </div>

    <!-- Card -->
    <div class="bg-white rounded-lg p-8 shadow-sm animate-fade-in-up" style="opacity: 0; animation-delay: 100ms; animation-fill-mode: forwards;">
      {#if verificationStatus === 'verifying'}
        <!-- Verifying State -->
        <div class="text-center">
          <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6">
            <Loader2 size={32} class="text-primary animate-spin" />
          </div>

          <h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-3">
            Подтверждение email
          </h2>

          <p class="text-muted mb-6">
            Пожалуйста, подождите, пока мы подтверждаем ваш email...
          </p>

          <div class="flex justify-center gap-1">
            {#each [0, 1, 2] as i}
              <div
                class="w-2 h-2 bg-primary rounded-full animate-pulse"
                style="animation-delay: {i * 200}ms"
              ></div>
            {/each}
          </div>
        </div>

      {:else if verificationStatus === 'pending'}
        <!-- Pending - Waiting for user to check email -->
        <div class="text-center">
          <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6">
            <Mail size={32} class="text-primary" />
          </div>

          <h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-3">
            Проверьте почту
          </h2>

          <p class="text-muted mb-6">
            Мы отправили ссылку для подтверждения на ваш email. Нажмите на ссылку, чтобы подтвердить аккаунт.
          </p>

          {#if email}
            <div class="bg-primary/10 rounded-xl p-4 mb-6">
              <p class="text-sm text-muted mb-1">
                Письмо для подтверждения отправлено на:
              </p>
              <p class="text-primary font-medium">
                {email}
              </p>
            </div>
          {/if}

          {#if resendSuccess}
            <div class="p-4 bg-success-light border border-success/20 rounded-lg mb-4 animate-scale-in">
              <div class="flex items-center gap-2 text-success">
                <CheckCircle size={16} />
                <span class="text-sm font-medium">Письмо для подтверждения отправлено! Проверьте почту.</span>
              </div>
            </div>
          {/if}

          {#if errorMessage}
            <div class="p-4 bg-error-light border border-error/20 rounded-lg mb-4">
              <p class="text-sm text-error">{errorMessage}</p>
            </div>
          {/if}

          <form
            method="POST"
            action="?/resend"
            use:enhance={() => {
              isResending = true;
              resendSuccess = false;
              return async ({ update }) => {
                await update();
              };
            }}
          >
            <input type="hidden" name="email" value={email} />
            <button
              type="submit"
              disabled={isResending || !email}
              class="w-full px-5 py-3 border border-primary text-primary font-medium rounded-full hover:bg-primary/10 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mb-4"
            >
              {#if isResending}
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Отправка...
              {:else}
                <RefreshCw size={18} />
                Отправить повторно
              {/if}
            </button>
          </form>

          <p class="text-sm text-muted">
            Не получили письмо? Проверьте папку со спамом или запросите новую ссылку для подтверждения выше.
          </p>
        </div>

      {:else if verificationStatus === 'success'}
        <!-- Success State -->
        <div class="text-center animate-scale-in">
          <div class="w-16 h-16 rounded-full bg-success-light flex items-center justify-center mx-auto mb-6">
            <CheckCircle size={32} class="text-success" />
          </div>

          <h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-3">
            Электронная почта подтверждена!
          </h2>

          <p class="text-muted mb-6">
            Ваш email подтверждён. Теперь вам доступен весь функционал Truddy.ru.
          </p>

          <div class="bg-success-light rounded-lg p-4 mb-6">
            <p class="text-sm font-medium text-success mb-1">
              Добро пожаловать!
            </p>
            <p class="text-sm text-muted">
              Перенаправление на главную страницу...
            </p>
          </div>

          <a
            href="/"
            class="inline-block w-full px-5 py-3.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-all shadow-sm hover:shadow-md text-center"
          >
            На главную
          </a>
        </div>

      {:else if verificationStatus === 'expired'}
        <!-- Expired State -->
        <div class="text-center">
          <div class="w-16 h-16 rounded-full bg-warning-light flex items-center justify-center mx-auto mb-6">
            <Clock size={32} class="text-warning" />
          </div>

          <h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-3">
            Ссылка устарела
          </h2>

          <p class="text-muted mb-6">
            Ссылка для подтверждения устарела. Не волнуйтесь, мы можем отправить новую!
          </p>

          {#if email}
            <div class="bg-primary/10 rounded-xl p-4 mb-6 text-left">
              <p class="text-sm text-muted mb-1">
                Отправка письма для подтверждения на:
              </p>
              <p class="text-primary font-medium">
                {email}
              </p>
            </div>
          {/if}

          {#if resendSuccess}
            <div class="p-4 bg-success-light border border-success/20 rounded-lg mb-4 animate-scale-in">
              <div class="flex items-center gap-2 text-success">
                <CheckCircle size={16} />
                <span class="text-sm font-medium">Письмо для подтверждения отправлено! Проверьте почту.</span>
              </div>
            </div>
          {/if}

          {#if errorMessage && !resendSuccess}
            <div class="p-4 bg-error-light border border-error/20 rounded-lg mb-4">
              <p class="text-sm text-error">{errorMessage}</p>
            </div>
          {/if}

          <form
            method="POST"
            action="?/resend"
            use:enhance={() => {
              isResending = true;
              resendSuccess = false;
              return async ({ update }) => {
                await update();
              };
            }}
          >
            <input type="hidden" name="email" value={email} />
            <button
              type="submit"
              disabled={isResending || !email}
              class="w-full px-5 py-3.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-all shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mb-4"
            >
              {#if isResending}
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Отправка...
              {:else}
                <RefreshCw size={18} />
                Отправить повторно
              {/if}
            </button>
          </form>

          <a href="/login/" class="text-muted hover:text-primary font-medium text-sm transition-colors">
            Вернуться к входу
          </a>
        </div>

      {:else}
        <!-- Error State -->
        <div class="text-center">
          <div class="w-16 h-16 rounded-full bg-error-light flex items-center justify-center mx-auto mb-6">
            <XCircle size={32} class="text-error" />
          </div>

          <h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-3">
            Ошибка подтверждения
          </h2>

          <p class="text-muted mb-2">
            Не удалось подтвердить ваш email.
          </p>

          {#if errorMessage}
            <div class="p-4 bg-error-light border border-error/20 rounded-lg mb-6">
              <p class="text-sm text-error">{errorMessage}</p>
            </div>
          {/if}

          <div class="bg-primary/10 rounded-lg p-4 mb-6 text-left">
            <p class="text-sm font-medium text-black mb-2">
              Что вы можете сделать:
            </p>
            <ul class="text-sm text-muted space-y-1">
              <li class="flex items-start gap-2">
                <span class="text-primary">•</span>
                Запросить новое письмо для подтверждения
              </li>
              <li class="flex items-start gap-2">
                <span class="text-primary">•</span>
                Проверьте, возможно вы уже подтвердили email
              </li>
              <li class="flex items-start gap-2">
                <span class="text-primary">•</span>
                Обратитесь в поддержку, если проблема не устранена
              </li>
            </ul>
          </div>

          {#if resendSuccess}
            <div class="p-4 bg-success-light border border-success/20 rounded-lg mb-4 animate-scale-in">
              <div class="flex items-center gap-2 text-success">
                <CheckCircle size={16} />
                <span class="text-sm font-medium">Письмо для подтверждения отправлено! Проверьте почту.</span>
              </div>
            </div>
          {/if}

          {#if email}
            <form
              method="POST"
              action="?/resend"
              use:enhance={() => {
                isResending = true;
                resendSuccess = false;
                return async ({ update }) => {
                  await update();
                };
              }}
            >
              <input type="hidden" name="email" value={email} />
              <button
                type="submit"
                disabled={isResending}
                class="w-full px-5 py-3 border border-primary text-primary font-medium rounded-full hover:bg-primary/10 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mb-4"
              >
                {#if isResending}
                  <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Отправка...
                {:else}
                  <RefreshCw size={18} />
                  Запросить новое письмо для подтверждения
                {/if}
              </button>
            </form>
          {/if}

          <div class="flex flex-col gap-2">
            <a
              href="/login/"
              class="text-primary hover:text-primary font-medium text-sm transition-colors"
            >
              Попробовать войти
            </a>
            <a
              href="/contact/"
              class="text-muted hover:text-primary font-medium text-sm transition-colors"
            >
              Связаться с поддержкой
            </a>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>
