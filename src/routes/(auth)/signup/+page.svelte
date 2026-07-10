<script lang="ts">
	import { untrack } from 'svelte';
	import { Building2, Mail, Lock, Phone, Eye, EyeOff, UserCircle, Globe, Users, Zap, Target, UserCheck, Headphones, CheckCircle, Shield, Clock } from '@lucide/svelte';
	import { getContext } from 'svelte';
	import { enhance } from '$app/forms';
	import { Button, Input, Card, FormField, Badge } from '$lib/components/ui';

	type AuthLayoutContext = {
		containerClass: string;
		mainClass: string;
	};

	let { data, form } = $props();

	const layout = getContext<AuthLayoutContext>('authLayout');
	layout.containerClass = 'max-w-6xl';
	layout.mainClass = 'flex justify-center items-start py-8 px-4 sm:px-6 lg:px-8';

	let invitationToken = $derived(data.invitationToken || '');
	let isInvitationFlow = $derived(!!invitationToken);
	let error = $derived(form?.error || '');

	let step = $state(untrack(() => invitationToken ? 1 : 0));
	let userType = $state<'recruiter' | 'company' | null>(untrack(() => invitationToken ? 'company' : null));
	let showPassword = $state(false);
	let showConfirmPassword = $state(false);
	let loading = $state(false);
	let success = $state(false);

	let formData = $state({
		accountType: '' as 'recruiter' | 'company',
		companyName: '',
		industry: '',
		companySize: '',
		website: '',
		firstName: '',
		lastName: '',
		email: '',
		phone: '',
		jobTitle: '',
		password: '',
		confirmPassword: '',
		agreeToTerms: false,
		subscribeNewsletter: true
	});

	const industries = [
		'Технологии', 'Финансы', 'Здравоохранение', 'Образование', 'Розничная торговля',
		'Производство', 'Консалтинг', 'Медиа', 'Недвижимость', 'Другое'
	];

	const companySizes = [
		'1–10 сотрудников', '11–50 сотрудников', '51–200 сотрудников',
		'201–500 сотрудников', '501–1000 сотрудников', '1001–5000 сотрудников', '5000+ сотрудников'
	];

	function selectAccountType(type: 'recruiter' | 'company') {
		userType = type;
		formData.accountType = type;
		step = 1;
	}

	function nextStep() {
		if (isInvitationFlow) {
			if (step < 2) step++;
		} else if (userType === 'company') {
			if (step < 3) step++;
		} else {
			if (step < 2) step++;
		}
	}

	function prevStep() {
		if (step > 1) {
			step--;
		} else {
			step = 0;
			userType = null;
		}
	}

	const sizeMap: Record<string, string> = {
		'1–10 сотрудников': '1-10',
		'11–50 сотрудников': '11-20',
		'51–200 сотрудников': '50-200',
		'201–500 сотрудников': '200+',
		'501–1000 сотрудников': '200+',
		'1001–5000 сотрудников': '200+',
		'5000+ сотрудников': '200+'
	};

	function getTotalSteps(): number {
		return userType === 'company' ? 3 : 2;
	}
</script>

<svelte:head>
	<title>Регистрация — Truddy.ru для рекрутеров</title>
	<meta name="description" content="Создайте аккаунт работодателя Truddy.ru и начните нанимать лучших специалистов уже сегодня." />
</svelte:head>

<div class="w-full">
	<div class="grid lg:grid-cols-2 gap-12 items-start">
		<!-- Left Column: Marketing Content -->
		<div class="space-y-8 lg:sticky lg:top-8 hidden lg:block">
			<div>
				<h1 class="text-3xl xl:text-4xl font-semibold text-black mb-4 leading-tight">
					Присоединяйтесь к 10 000+ компаний, нанимающих через Truddy.ru
				</h1>
				<p class="text-base xl:text-lg text-muted leading-relaxed">
					Получите доступ к крупнейшей базе талантов Индии с 100k+ активных соискателей. Размещайте неограниченное количество вакансий бесплатно и находите идеальных кандидатов быстрее.
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
					<p class="text-sm text-muted font-medium">Заявок в день</p>
				</div>
				<div class="bg-primary/5 border border-primary/20 rounded-lg p-5 text-center">
					<div class="text-2xl font-semibold text-primary mb-1">500+</div>
					<p class="text-sm text-muted font-medium">Компаний доверяют нам</p>
				</div>
				<div class="bg-warning-light border border-warning/20 rounded-lg p-5 text-center">
					<div class="text-2xl font-semibold text-warning mb-1">24/7</div>
					<p class="text-sm text-muted font-medium">Экспертная поддержка</p>
				</div>
			</div>

			<!-- Key Benefits -->
			<Card padding="lg" class="shadow-md">
				<h3 class="text-xl font-semibold text-black mb-6 flex items-center gap-2">
					<Target class="w-5 h-5 text-warning" />
					Почему рекрутеры выбирают Truddy.ru
				</h3>
				<div class="space-y-5">
					<div class="flex items-start gap-4">
						<div class="bg-primary/10 rounded-full p-2.5 flex-shrink-0">
							<Zap class="w-5 h-5 text-primary" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Мгновенная публикация вакансий</h4>
							<p class="text-sm text-muted leading-relaxed">Размещайте неограниченное количество вакансий бесплатно и получайте отклики в течение нескольких часов</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<div class="bg-success-light rounded-full p-2.5 flex-shrink-0">
							<CheckCircle class="w-5 h-5 text-success" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Умный подбор</h4>
							<p class="text-sm text-muted leading-relaxed">ИИ-система подбирает наиболее квалифицированных кандидатов</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<div class="bg-primary/10 rounded-full p-2.5 flex-shrink-0">
							<UserCheck class="w-5 h-5 text-primary" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Качественные кандидаты</h4>
							<p class="text-sm text-muted leading-relaxed">Доступ к проверенным профилям с подробными навыками и опытом</p>
						</div>
					</div>
					<div class="flex items-start gap-4">
						<div class="bg-warning-light rounded-full p-2.5 flex-shrink-0">
							<Headphones class="w-5 h-5 text-warning" />
						</div>
						<div>
							<h4 class="font-medium text-black text-sm mb-0.5">Персональная поддержка</h4>
							<p class="text-sm text-muted leading-relaxed">Круглосуточная поддержка для оптимизации процесса найма</p>
						</div>
					</div>
				</div>
			</Card>
		</div>

		<!-- Right Column: Registration Form -->
		<Card padding="lg" class="shadow-lg">
			<!-- Header -->
			<div class="text-center mb-6">
				{#if isInvitationFlow}
					<Badge variant="primary" class="mb-4">
						<Users class="w-4 h-4 mr-1" />
						Приглашение в команду
					</Badge>
					<h2 class="text-2xl font-semibold text-black">Присоединиться к команде</h2>
					<p class="text-muted mt-2">Заполните профиль, чтобы присоединиться к команде компании</p>
				{:else}
					<h2 class="text-2xl font-semibold text-black">Создать аккаунт работодателя</h2>
					<p class="text-muted mt-2">Начните нанимать лучших специалистов уже сегодня</p>
				{/if}
			</div>

			{#if step > 0}
				<!-- Progress Indicator -->
				<div class="flex items-center justify-center mb-6">
					<div class="flex items-center">
						{#if userType === 'company' && !isInvitationFlow}
							<div class="w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm {step >= 1 ? 'bg-primary text-white' : 'bg-surface text-muted'}">1</div>
							<div class="w-16 h-1 {step >= 2 ? 'bg-primary' : 'bg-surface'}"></div>
							<div class="w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm {step >= 2 ? 'bg-primary text-white' : 'bg-surface text-muted'}">2</div>
							<div class="w-16 h-1 {step >= 3 ? 'bg-primary' : 'bg-surface'}"></div>
							<div class="w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm {step === 3 ? 'bg-primary text-white' : 'bg-surface text-muted'}">3</div>
						{:else}
							<div class="w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm {step >= 1 ? 'bg-primary text-white' : 'bg-surface text-muted'}">1</div>
							<div class="w-16 h-1 {step >= 2 ? 'bg-primary' : 'bg-surface'}"></div>
							<div class="w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm {step === 2 ? 'bg-primary text-white' : 'bg-surface text-muted'}">2</div>
						{/if}
					</div>
				</div>
			{/if}

			{#if success}
				<div class="bg-success-light border border-success/20 rounded-lg p-6 text-center">
					<div class="mx-auto w-12 h-12 rounded-full bg-success/20 flex items-center justify-center mb-4">
						<CheckCircle class="w-6 h-6 text-success" />
					</div>
					{#if isInvitationFlow}
						<h3 class="text-xl font-semibold text-black mb-2">Добро пожаловать в команду!</h3>
						<p class="text-muted mb-4">Ваш аккаунт успешно создан.</p>
						<p class="text-sm text-muted">Перенаправление на панель управления...</p>
					{:else}
						<h3 class="text-xl font-semibold text-black mb-2">Регистрация успешно завершена!</h3>
						<p class="text-muted mb-4">Проверьте электронную почту ({formData.email}) — мы отправили ссылку для подтверждения.</p>
						<p class="text-sm text-muted">Перенаправление на страницу подтверждения...</p>
					{/if}
				</div>
			{:else}
				<form method="POST" action={isInvitationFlow ? '?/acceptInvitation' : '?/register'} use:enhance={({ cancel, formData: submitData }) => {
					const isFinalStep = (userType === 'company' && step === 3) || (userType === 'recruiter' && step === 2) || (isInvitationFlow && step === 2);
					if (!isFinalStep) {
						cancel();
						nextStep();
						return;
					}

					submitData.set('account_type', formData.accountType);
					submitData.set('token', invitationToken);
					submitData.set('first_name', formData.firstName);
					submitData.set('last_name', formData.lastName);
					submitData.set('email', formData.email);
					submitData.set('phone', formData.phone);
					submitData.set('job_title', formData.jobTitle);
					submitData.set('password', formData.password);
					submitData.set('confirm_password', formData.confirmPassword);
					submitData.set('agree_to_terms', formData.agreeToTerms ? 'true' : '');

					if (formData.accountType === 'company') {
						submitData.set('company_name', formData.companyName);
						submitData.set('company_website', formData.website);
						submitData.set('company_industry', formData.industry);
						submitData.set('company_size', sizeMap[formData.companySize] || '');
					}

					loading = true;
					return async ({ result, update }) => {
						loading = false;
						if (result.type === 'redirect') {
							success = true;
						}
						await update();
					};
				}} class="space-y-5">
					{#if error}
						<div class="bg-error-light border border-error/20 text-error px-4 py-3 rounded-lg text-sm whitespace-pre-line">
							{error}
						</div>
					{/if}

					{#if step === 0 && !isInvitationFlow}
						<!-- Step 0: Account Type Selection -->
						<div class="space-y-4">
							<h3 class="text-lg font-semibold text-black text-center mb-4">Выберите тип аккаунта</h3>

							<div class="grid grid-cols-1 gap-3">
								<button
									type="button"
									onclick={() => selectAccountType('company')}
									class="p-5 border-2 border-border rounded-lg hover:border-primary hover:bg-primary/5 transition-all text-left group"
								>
									<div class="flex items-start gap-4">
										<div class="w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary flex items-center justify-center transition-colors">
											<Building2 class="w-6 h-6 text-primary group-hover:text-white transition-colors" />
										</div>
										<div class="flex-1">
											<h4 class="text-lg font-semibold text-black mb-1">Аккаунт компании</h4>
											<p class="text-sm text-muted">
												Я регистрируюсь от имени компании, чтобы размещать вакансии и нанимать сотрудников.
											</p>
											<ul class="mt-2 space-y-1 text-sm text-muted">
												<li class="flex items-center gap-2">
													<CheckCircle class="w-4 h-4 text-success" />
													Неограниченное количество вакансий
												</li>
												<li class="flex items-center gap-2">
													<CheckCircle class="w-4 h-4 text-success" />
													Управление участниками команды
												</li>
												<li class="flex items-center gap-2">
													<CheckCircle class="w-4 h-4 text-success" />
													Брендинг и профиль компании
												</li>
											</ul>
										</div>
									</div>
								</button>

								<button
									type="button"
									onclick={() => selectAccountType('recruiter')}
									class="p-5 border-2 border-border rounded-lg hover:border-primary hover:bg-primary/5 transition-all text-left group"
								>
									<div class="flex items-start gap-4">
										<div class="w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary flex items-center justify-center transition-colors">
											<UserCircle class="w-6 h-6 text-primary group-hover:text-white transition-colors" />
										</div>
										<div class="flex-1">
											<h4 class="text-lg font-semibold text-black mb-1">Независимый рекрутер</h4>
											<p class="text-sm text-muted">
												Я независимый рекрутер или консультант, работающий с несколькими компаниями.
											</p>
											<ul class="mt-2 space-y-1 text-sm text-muted">
												<li class="flex items-center gap-2">
													<CheckCircle class="w-4 h-4 text-success" />
													Размещение вакансий для клиентов
												</li>
												<li class="flex items-center gap-2">
													<CheckCircle class="w-4 h-4 text-success" />
													Управление кандидатами
												</li>
												<li class="flex items-center gap-2">
													<CheckCircle class="w-4 h-4 text-success" />
													Личный профиль рекрутера
												</li>
											</ul>
										</div>
									</div>
								</button>
							</div>
						</div>
					{:else if userType === 'company' && step === 1}
						<!-- Company Step 1: Company Information -->
						<div class="space-y-4">
							<h3 class="text-lg font-semibold text-black mb-3">Информация о компании</h3>

							<FormField label="Название компании" required>
								<Input
									type="text"
									id="companyName"
									bind:value={formData.companyName}
									required
									placeholder="Название вашей компании"
									size="lg"
								>
									{#snippet iconLeft()}
										<Building2 class="w-5 h-5" />
									{/snippet}
								</Input>
							</FormField>

							<FormField label="Сайт компании" required hint="Мы проверим сайт вашей компании">
								<Input
									type="url"
									id="website"
									bind:value={formData.website}
									required
									placeholder="https://yourcompany.com"
									size="lg"
								>
									{#snippet iconLeft()}
										<Globe class="w-5 h-5" />
									{/snippet}
								</Input>
							</FormField>

							<FormField label="Отрасль" required>
								<select
									id="industry"
									bind:value={formData.industry}
									required
									class="w-full h-12 px-4 text-base border border-border rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 focus:outline-none"
								>
									<option value="">Выберите отрасль</option>
									{#each industries as industry}
										<option value={industry}>{industry}</option>
									{/each}
								</select>
							</FormField>

							<FormField label="Размер компании" required>
								<select
									id="companySize"
									bind:value={formData.companySize}
									required
									class="w-full h-12 px-4 text-base border border-border rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 focus:outline-none"
								>
									<option value="">Выберите размер компании</option>
									{#each companySizes as size}
										<option value={size}>{size}</option>
									{/each}
								</select>
							</FormField>
						</div>
					{:else if (userType === 'company' && step === 2) || (userType === 'recruiter' && step === 1) || (isInvitationFlow && step === 1)}
						<!-- Personal Information Step -->
						<div class="space-y-4">
							<h3 class="text-lg font-semibold text-black mb-3">Ваши данные</h3>

							<div class="grid grid-cols-2 gap-3">
								<FormField label="Имя" required>
									<Input
										type="text"
										id="firstName"
										bind:value={formData.firstName}
										required
										placeholder="Иван"
										size="lg"
									/>
								</FormField>

								<FormField label="Фамилия" required>
									<Input
										type="text"
										id="lastName"
										bind:value={formData.lastName}
										required
										placeholder="Иванов"
										size="lg"
									/>
								</FormField>
							</div>

							{#if !isInvitationFlow}
								<FormField label={userType === 'company' ? 'Рабочая электронная почта' : 'Электронная почта'} required hint={userType === 'company' ? 'Используйте корпоративную почту для подтверждения связи с компанией' : undefined}>
									<Input
										type="email"
										id="email"
										bind:value={formData.email}
										required
										placeholder={userType === 'company' ? 'ivan@company.com' : 'ivan@example.com'}
										size="lg"
									>
										{#snippet iconLeft()}
											<Mail class="w-5 h-5" />
										{/snippet}
									</Input>
								</FormField>

								<FormField label="Номер телефона" required>
									<Input
										type="tel"
										id="phone"
										bind:value={formData.phone}
										required
										placeholder="+7 (999) 123-45-67"
										size="lg"
									>
										{#snippet iconLeft()}
											<Phone class="w-5 h-5" />
										{/snippet}
									</Input>
								</FormField>

								<FormField label={userType === 'company' ? 'Ваша должность' : 'Профессиональная должность'} required>
									<Input
										type="text"
										id="jobTitle"
										bind:value={formData.jobTitle}
										required
										placeholder={userType === 'company' ? 'HR-менеджер, рекрутер и т. д.' : 'Старший рекрутер, специалист по подбору персонала и т. д.'}
										size="lg"
									/>
								</FormField>
							{/if}
						</div>
					{:else if (userType === 'company' && step === 3) || (userType === 'recruiter' && step === 2) || (isInvitationFlow && step === 2)}
						<!-- Final Step: Account Setup -->
						<div class="space-y-4">
							<h3 class="text-lg font-semibold text-black mb-3">{isInvitationFlow ? 'Установите пароль' : 'Создайте аккаунт'}</h3>

							<FormField label="Пароль" required hint="Минимум 8 символов">
								<div class="relative">
									<Input
										type={showPassword ? 'text' : 'password'}
										id="password"
										name="password"
										bind:value={formData.password}
										required
										placeholder="Придумайте надёжный пароль"
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
							</FormField>

							<FormField label="Подтверждение пароля" required>
								<div class="relative">
									<Input
										type={showConfirmPassword ? 'text' : 'password'}
										id="confirmPassword"
										name="confirm_password"
										bind:value={formData.confirmPassword}
										required
										placeholder="Повторите пароль"
										size="lg"
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

							{#if !isInvitationFlow}
								<div class="space-y-3 pt-3">
									<label class="flex items-start gap-3 cursor-pointer group">
										<input
											type="checkbox"
											bind:checked={formData.agreeToTerms}
											required
											class="w-4 h-4 text-primary border-border rounded mt-0.5 focus:ring-primary/20"
										/>
										<span class="text-sm text-muted group-hover:text-black transition-colors">
											Я принимаю <a href="/terms/" class="text-primary hover:text-primary-hover">Условия использования</a>
											и <a href="/privacy/" class="text-primary hover:text-primary-hover">Политику конфиденциальности</a>
										</span>
									</label>

									<label class="flex items-start gap-3 cursor-pointer group">
										<input
											type="checkbox"
											bind:checked={formData.subscribeNewsletter}
											class="w-4 h-4 text-primary border-border rounded mt-0.5 focus:ring-primary/20"
										/>
										<span class="text-sm text-muted group-hover:text-black transition-colors">
											Присылайте мне новости о трендах найма и возможностях платформы
										</span>
									</label>
								</div>
							{/if}
						</div>
					{/if}

					{#if step > 0}
						<!-- Navigation Buttons -->
						<div class="flex items-center justify-between mt-6 pt-6 border-t border-border">
							<Button type="button" variant="secondary" onclick={prevStep}>
								Назад
							</Button>

							{#if (userType === 'company' && step < 3) || (userType === 'recruiter' && step < 2) || (isInvitationFlow && step < 2)}
								<Button type="submit">
									Продолжить
								</Button>
							{:else}
								<Button type="submit" disabled={(!isInvitationFlow && !formData.agreeToTerms) || loading} {loading}>
									{#if loading}
										{isInvitationFlow ? 'Присоединение к команде...' : 'Создание аккаунта...'}
									{:else}
										{isInvitationFlow ? 'Присоединиться к команде' : 'Создать аккаунт'}
									{/if}
								</Button>
							{/if}
						</div>
					{/if}
				</form>
			{/if}

			<!-- Sign In Link -->
			<p class="mt-6 text-center text-sm text-muted">
				Уже есть аккаунт?
				<a href="/login/" class="font-medium text-primary hover:text-primary-hover transition-colors">Войти</a>
			</p>

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
