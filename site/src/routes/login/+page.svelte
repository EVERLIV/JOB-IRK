<script>
  import '../../app.css';

  import { onMount, untrack } from 'svelte';
  import { page } from '$app/stores';
  import { enhance } from '$app/forms';
  import { AlertCircle, Loader2, Briefcase, Shield, Zap, Mail, Lock } from '@lucide/svelte';
  import BrandLogo from '$lib/components/BrandLogo.svelte';

  let { data, form } = $props();

  let isLoading = $state(false);
  let loadingProvider = $state('');
  let socialError = $state('');
  let urlError = $state('');
  let email = $state(untrack(() => form?.email || ''));
  let password = $state('');

  let error = $derived(form?.error || socialError || urlError || '');

  onMount(() => {
    const errorCode = $page.url.searchParams.get('error');
    if (errorCode) {
      urlError = getErrorMessage(errorCode);
    }
  });

  /** @param {string} errorCode */
  function getErrorMessage(errorCode) {
    const errorMessages = {
      'access_denied': 'Вход отменён. Пожалуйста, попробуйте снова.',
      'invalid_request': 'Что-то пошло не так. Пожалуйста, попробуйте снова.',
      'server_error': 'Произошла ошибка сервера. Пожалуйста, попробуйте позже.',
      'temporarily_unavailable': 'Сервис временно недоступен. Пожалуйста, попробуйте позже.'
    };
    return errorMessages[/** @type {keyof typeof errorMessages} */ (errorCode)] || 'Произошла ошибка при входе. Пожалуйста, попробуйте снова.';
  }

  /** @param {string} provider */
  async function handleSocialLogin(provider) {
    if (isLoading) return;
    isLoading = true;
    loadingProvider = provider;
    socialError = '';
    try {
      if (provider === 'google') {
        const { getGoogleAuthUrl } = await import('$lib/api/auth');
        const redirectUri = window.location.origin + '/auth/google/callback';
        const response = await getGoogleAuthUrl(redirectUri);
        window.location.href = response.auth_url;
      } else if (provider === 'facebook') {
        socialError = 'Вход через Facebook скоро появится!';
        isLoading = false;
        loadingProvider = '';
      }
    } catch (err) {
      socialError = err instanceof Error ? err.message : 'Не удалось начать вход. Пожалуйста, попробуйте снова.';
      isLoading = false;
      loadingProvider = '';
    }
  }

  function clearError() {
    socialError = '';
    urlError = '';
  }

  const features = [
    { icon: Briefcase, title: 'Найдите работу мечты', description: 'Доступ к тысячам возможностей' },
    { icon: Shield, title: 'Безопасно и конфиденциально', description: 'Ваши данные всегда защищены' },
    { icon: Zap, title: 'Быстро и легко', description: 'Подача заявки в один клик' }
  ];
</script>

<svelte:head>
  <title>Вход - Truddy.ru</title>
  <meta name="description" content="Войдите в Truddy.ru - Ваш путь к карьерным возможностям" />
</svelte:head>

<div class="min-h-screen bg-white flex">
  <div class="hidden lg:flex lg:w-1/2 bg-[#1D2226] relative overflow-hidden">
    <div class="absolute inset-0">
      <div class="absolute top-0 right-0 w-96 h-96 bg-primary-600/20 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl"></div>
    </div>
    <div class="relative z-10 flex flex-col justify-center px-12 xl:px-16 w-full">
      <div class="mb-10 animate-fade-in-up" style="opacity: 0; animation-fill-mode: forwards;">
        <BrandLogo href="/" size="lg" textClass="text-white" />
      </div>
      <div class="mb-10">
        <h1 class="text-3xl xl:text-4xl font-semibold text-white tracking-tight mb-4 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms; animation-fill-mode: forwards;">
          С возвращением
        </h1>
        <p class="text-lg text-gray-400 max-w-md animate-fade-in-up" style="opacity: 0; animation-delay: 150ms; animation-fill-mode: forwards;">
          Войдите, чтобы продолжить поиск работы и связаться с лучшими работодателями.
        </p>
      </div>
      <div class="space-y-5">
        {#each features as feature, i}
          <div class="flex items-start gap-4 animate-fade-in-up" style="opacity: 0; animation-delay: {200 + i * 50}ms; animation-fill-mode: forwards;">
            <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center flex-shrink-0">
              <feature.icon size={20} class="text-primary-400" />
            </div>
            <div>
              <h3 class="font-medium text-white mb-0.5">{feature.title}</h3>
              <p class="text-sm text-gray-400">{feature.description}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
  <div class="flex-1 flex items-center justify-center p-6 lg:p-12">
    <div class="w-full max-w-sm">
      <div class="lg:hidden text-center mb-8 animate-fade-in-down" style="opacity: 0; animation-fill-mode: forwards;">
        <BrandLogo href="/" size="lg" class="justify-center" />
      </div>
      <div class="animate-fade-in-up" style="opacity: 0; animation-delay: 100ms; animation-fill-mode: forwards;">
        <div class="text-center mb-8">
          <h2 class="text-2xl font-semibold text-black mb-2">Войти</h2>
          <p class="text-muted">Будьте в курсе своего профессионального мира</p>
        </div>
        {#if error}
          <div class="mb-6 p-4 bg-error-light border border-error-500/20 rounded-lg flex items-start gap-3 animate-scale-in">
            <AlertCircle size={20} class="text-error-600 mt-0.5 flex-shrink-0" />
            <div class="flex-1">
              <p class="text-error-600 text-sm">{error}</p>
              <button onclick={clearError} class="text-error-600 hover:text-error-700 text-xs font-medium mt-1 hover:underline">
                Закрыть
              </button>
            </div>
          </div>
        {/if}
        <div class="space-y-3">
          <button onclick={() => handleSocialLogin('google')} disabled={isLoading} class="w-full flex items-center justify-center gap-3 h-12 px-5 border border-border rounded-full bg-white text-black font-semibold hover:bg-surface hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
            {#if loadingProvider === 'google'}
              <Loader2 size={20} class="animate-spin" />
            {:else}
              <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            {/if}
            <span>Войти через Google</span>
          </button>
          <button onclick={() => handleSocialLogin('facebook')} disabled={isLoading} class="w-full flex items-center justify-center gap-3 h-12 px-5 bg-[#1877F2] hover:bg-[#166fe5] text-white font-semibold rounded-full transition-all disabled:opacity-50 disabled:cursor-not-allowed">
            {#if loadingProvider === 'facebook'}
              <Loader2 size={20} class="animate-spin" />
            {:else}
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            {/if}
            <span>Войти через Facebook</span>
          </button>
        </div>
        <div class="my-6 relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-border"></div>
          </div>
          <div class="relative flex justify-center">
            <span class="px-4 bg-white text-sm text-muted">или</span>
          </div>
        </div>
        <form
          method="POST"
          use:enhance={() => {
            isLoading = true;
            loadingProvider = 'password';
            return async ({ update }) => {
              await update();
              isLoading = false;
              loadingProvider = '';
            };
          }}
          class="space-y-3 mb-6"
        >
          <input type="hidden" name="redirect_to" value={data.redirectTo} />
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail size={18} class="text-muted" />
            </span>
            <input
              type="email"
              name="email"
              bind:value={email}
              placeholder="email@example.com"
              class="w-full h-12 pl-10 pr-4 border border-border rounded-lg bg-white text-black placeholder-muted focus:border-primary focus:ring-2 focus:ring-primary-500/20 outline-none"
            />
          </div>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock size={18} class="text-muted" />
            </span>
            <input
              type="password"
              name="password"
              bind:value={password}
              placeholder="Пароль"
              class="w-full h-12 pl-10 pr-4 border border-border rounded-lg bg-white text-black placeholder-muted focus:border-primary focus:ring-2 focus:ring-primary-500/20 outline-none"
            />
          </div>
          <button type="submit" disabled={isLoading} class="w-full h-12 px-5 bg-primary-600 text-white font-semibold rounded-full hover:bg-primary-700 transition-all disabled:opacity-50">
            {#if loadingProvider === 'password'}
              Вход...
            {:else}
              Войти по email
            {/if}
          </button>
          <div class="text-center">
            <a href="/forgot-password/" class="text-sm text-primary-600 hover:text-primary-700 font-semibold hover:underline">
              Забыли пароль?
            </a>
          </div>
        </form>
        <div class="flex items-center justify-center gap-2 text-sm text-muted">
          <Shield size={16} class="text-success-500" />
          <span>Защищено безопасностью корпоративного уровня</span>
        </div>
      </div>
      <div class="mt-8 text-center space-y-4 animate-fade-in-up" style="opacity: 0; animation-delay: 200ms; animation-fill-mode: forwards;">
        <p class="text-sm text-muted">
          Входя в систему, вы соглашаетесь с нашими
          <a href="/terms/" class="text-primary-600 hover:text-primary-700 font-semibold hover:underline">Условиями</a>
          и
          <a href="/privacy/" class="text-primary-600 hover:text-primary-700 font-semibold hover:underline">Политикой конфиденциальности</a>
        </p>
        <p class="text-sm text-muted">
          Впервые в Truddy.ru?
          <a href="/register/" class="text-primary-600 hover:text-primary-700 font-semibold hover:underline">Зарегистрироваться</a>
        </p>
      </div>
      <div class="mt-8 flex justify-center gap-6 text-sm text-muted animate-fade-in" style="opacity: 0; animation-delay: 300ms; animation-fill-mode: forwards;">
        <a href="/about/" class="hover:text-black transition-colors">О нас</a>
        <a href="/help/" class="hover:text-black transition-colors">Помощь</a>
        <a href="/contact/" class="hover:text-black transition-colors">Контакты</a>
      </div>
    </div>
  </div>
</div>
