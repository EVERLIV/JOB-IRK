<script lang="ts">
	import { Mail, MapPin, Send, Clock, MessageCircle, HelpCircle, CheckCircle, AlertCircle, ChevronRight, ArrowRight } from '@lucide/svelte';
	import { submitContactForm, type ContactFormData } from '$lib/api/contact';
	import { toast } from '$lib/stores/toast';

	interface FormData {
		firstName: string;
		lastName: string;
		email: string;
		phone: string;
		subject: string;
		category: string;
		message: string;
	}

	interface FormErrors {
		firstName?: string;
		email?: string;
		subject?: string;
		message?: string;
		phone?: string;
		submit?: string;
	}

	const initialFormData: FormData = {
		firstName: '',
		lastName: '',
		email: '',
		phone: '',
		subject: '',
		category: 'general',
		message: ''
	};

	let formData = $state<FormData>({ ...initialFormData });

	let errors = $state<FormErrors>({});
	let isSubmitting = $state(false);
	let submitSuccess = $state(false);

	const categories = [
		{ value: 'general', label: 'Общий вопрос' },
		{ value: 'support', label: 'Техническая поддержка' },
		{ value: 'job_seeker', label: 'Помощь соискателям' },
		{ value: 'employer', label: 'Работодателям/Рекрутерам' },
		{ value: 'partnership', label: 'Партнёрство' },
		{ value: 'feedback', label: 'Обратная связь и предложения' }
	];

	const contactInfo = [
		{
			icon: Mail,
			title: 'Эл. почта',
			details: 'peeljobs@micropyramid.com',
			link: 'mailto:peeljobs@micropyramid.com',
			description: 'Напишите нам в любое время'
		},
		{
			icon: MapPin,
			title: 'Офис',
			details: 'Хайдарабад, Телангана, Индия',
			link: null,
			description: 'Главный офис'
		}
	];

	const faqs = [
		{
			question: 'Как быстро я получу ответ?',
			answer: 'Обычно мы отвечаем на все обращения в течение 24 часов в рабочие дни.'
		},
		{
			question: 'PeelJobs действительно бесплатный?',
			answer: 'Да! PeelJobs полностью бесплатен как для соискателей, так и для работодателей. Никаких скрытых платежей.'
		},
		{
			question: 'Могу ли я посетить ваш офис?',
			answer: 'Да, но рекомендуем заранее записаться на приём, связавшись с нами.'
		}
	];

	function validateForm(): boolean {
		errors = {};
		let isValid = true;

		if (!formData.firstName.trim()) {
			errors.firstName = 'Укажите имя';
			isValid = false;
		}

		if (!formData.email.trim()) {
			errors.email = 'Укажите email';
			isValid = false;
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
			errors.email = 'Введите корректный email';
			isValid = false;
		}

		if (formData.phone && !/^\d{10,12}$/.test(formData.phone.replace(/\s/g, ''))) {
			errors.phone = 'Введите корректный номер телефона (10-12 цифр)';
			isValid = false;
		}

		if (!formData.subject.trim()) {
			errors.subject = 'Укажите тему';
			isValid = false;
		}

		if (!formData.message.trim()) {
			errors.message = 'Введите сообщение';
			isValid = false;
		} else if (formData.message.trim().length < 10) {
			errors.message = 'Сообщение должно содержать не менее 10 символов';
			isValid = false;
		}

		return isValid;
	}

	async function handleSubmit(event: SubmitEvent): Promise<void> {
		event.preventDefault();

		if (!validateForm()) {
			return;
		}

		isSubmitting = true;
		submitSuccess = false;
		errors.submit = undefined;

		try {
			const requestData: ContactFormData = {
				first_name: formData.firstName.trim(),
				last_name: formData.lastName.trim() || undefined,
				email: formData.email.trim(),
				phone: formData.phone ? parseInt(formData.phone.replace(/\s/g, '')) : undefined,
				category: formData.category,
				subject: formData.subject.trim(),
				comment: formData.message.trim()
			};

			const response = await submitContactForm(requestData);

			submitSuccess = true;
			toast.success("Сообщение отправлено! Мы ответим в течение 24 часов.");

			formData = { ...initialFormData };

			setTimeout(() => {
				submitSuccess = false;
			}, 10000);
		} catch (error: any) {
			console.error('Contact form error:', error);

			if (error.details) {
				if (error.details.first_name) errors.firstName = error.details.first_name[0];
				if (error.details.email) errors.email = error.details.email[0];
				if (error.details.phone) errors.phone = error.details.phone[0];
				if (error.details.subject) errors.subject = error.details.subject[0];
				if (error.details.comment) errors.message = error.details.comment[0];

				errors.submit = 'Исправьте ошибки выше и попробуйте снова.';
				toast.error('Проверьте форму на наличие ошибок');
			} else {
				errors.submit = 'Не удалось отправить сообщение. Попробуйте снова или напишите нам на peeljobs@micropyramid.com';
				toast.error('Не удалось отправить сообщение. Попробуйте снова.');
			}
		} finally {
			isSubmitting = false;
		}
	}
</script>

<svelte:head>
	<title>Связаться с нами - PeelJobs | Свяжитесь с нашей командой поддержки</title>
	<meta name="description" content="Есть вопросы или нужна помощь? Свяжитесь с командой поддержки PeelJobs. Мы помогаем соискателям и работодателям на нашей бесплатной платформе." />
	<link rel="canonical" href="https://peeljobs.com/contact/" />

	<!-- Open Graph -->
	<meta property="og:title" content="Связаться с поддержкой PeelJobs - Мы готовы помочь" />
	<meta property="og:description" content="Свяжитесь с нашей командой по любым вопросам о нашей бесплатной платформе." />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://peeljobs.com/contact/" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="Связаться с PeelJobs" />
	<meta name="twitter:description" content="Обратитесь к нашей команде поддержки за помощью." />
</svelte:head>

<!-- Hero Section -->
<section class="bg-[#1D2226] text-white py-16 lg:py-20 relative overflow-hidden">
	<!-- Decorative Elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-0 right-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
		<div class="absolute bottom-0 left-1/4 w-80 h-80 bg-primary/10 rounded-full blur-3xl"></div>
	</div>

	<div class="max-w-7xl mx-auto px-4 lg:px-8 relative">
		<!-- Breadcrumb -->
		<nav class="mb-8" aria-label="Навигация">
			<ol class="flex items-center gap-2 text-sm text-muted">
				<li>
					<a href="/" class="hover:text-white transition-colors">Главная</a>
				</li>
				<li class="flex items-center gap-2">
					<ChevronRight size={14} />
					<span class="text-white font-medium">Связаться с нами</span>
				</li>
			</ol>
		</nav>

		<div class="max-w-4xl mx-auto text-center">
			<div class="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-8 animate-fade-in-up" style="opacity: 0;">
				<Mail size={40} class="text-primary" />
			</div>
			<h1 class="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms;">
				Свяжитесь с нами
			</h1>
			<p class="text-lg md:text-xl text-gray-300 max-w-2xl mx-auto animate-fade-in-up" style="opacity: 0; animation-delay: 200ms;">
				Есть вопросы или нужна помощь? Наша команда поддержки готова помочь. Обычно мы отвечаем в течение 24 часов.
			</p>
		</div>
	</div>
</section>

<!-- Contact Info Cards -->
<section class="py-12 lg:py-16 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
			{#each contactInfo as info, i}
				<div
					class="group bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border animate-fade-in-up"
					style="opacity: 0; animation-delay: {i * 100}ms;"
				>
					<div class="flex items-start gap-4">
						<div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary transition-colors">
							<info.icon size={24} class="text-primary group-hover:text-white transition-colors" />
						</div>
						<div class="flex-1 min-w-0">
							<h3 class="text-lg font-semibold text-black mb-2">{info.title}</h3>
							{#if info.link}
								<a href={info.link} class="text-primary hover:text-primary-hover font-medium text-base mb-1 block break-words">
									{info.details}
								</a>
							{:else}
								<p class="text-black font-medium text-base mb-1">{info.details}</p>
							{/if}
							<p class="text-sm text-muted">{info.description}</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- Main Content -->
<section class="py-12 lg:py-20 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">

			<!-- Contact Form -->
			<div class="lg:col-span-2">
				<div class="bg-white rounded-lg p-6 lg:p-8 shadow-sm border border-border">
					<div class="mb-8">
						<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-2">Отправить сообщение</h2>
						<p class="text-muted">Заполните форму ниже, и наша команда ответит в течение 24 часов</p>
					</div>

					{#if submitSuccess}
						<div class="mb-6 bg-success-light border border-success/20 rounded-lg p-4 flex items-start gap-3 animate-fade-in">
							<div class="w-6 h-6 rounded-full bg-success-light flex items-center justify-center flex-shrink-0">
								<CheckCircle size={16} class="text-success" />
							</div>
							<div>
								<p class="text-success font-medium">Сообщение успешно отправлено!</p>
								<p class="text-sm text-success/80 mt-1">Спасибо за обращение. Мы ответим в течение 24 часов.</p>
							</div>
						</div>
					{/if}

					<form onsubmit={handleSubmit} class="space-y-6">
						<!-- Name Fields -->
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<!-- First Name -->
							<div>
								<label for="firstName" class="block text-sm font-medium text-muted mb-2">
									Имя <span class="text-error">*</span>
								</label>
								<input
									id="firstName"
									type="text"
									bind:value={formData.firstName}
									placeholder="Иван"
									class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none {errors.firstName ? 'border-error' : 'border-border'}"
									disabled={isSubmitting}
								/>
								{#if errors.firstName}
									<p class="mt-1.5 text-sm text-error">{errors.firstName}</p>
								{/if}
							</div>

							<!-- Last Name -->
							<div>
								<label for="lastName" class="block text-sm font-medium text-muted mb-2">
									Фамилия
								</label>
								<input
									id="lastName"
									type="text"
									bind:value={formData.lastName}
									placeholder="Иванов"
									class="w-full px-4 py-3 border border-border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none"
									disabled={isSubmitting}
								/>
							</div>
						</div>

						<!-- Email & Phone -->
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<!-- Email -->
							<div>
								<label for="email" class="block text-sm font-medium text-muted mb-2">
									Эл. почта <span class="text-error">*</span>
								</label>
								<input
									id="email"
									type="email"
									bind:value={formData.email}
									placeholder="ivan@example.com"
									class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none {errors.email ? 'border-error' : 'border-border'}"
									disabled={isSubmitting}
								/>
								{#if errors.email}
									<p class="mt-1.5 text-sm text-error">{errors.email}</p>
								{/if}
							</div>

							<!-- Phone -->
							<div>
								<label for="phone" class="block text-sm font-medium text-muted mb-2">
									Телефон
								</label>
								<input
									id="phone"
									type="tel"
									bind:value={formData.phone}
									placeholder="9876543210"
									class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none {errors.phone ? 'border-error' : 'border-border'}"
									disabled={isSubmitting}
								/>
								{#if errors.phone}
									<p class="mt-1.5 text-sm text-error">{errors.phone}</p>
								{:else}
									<p class="mt-1.5 text-xs text-muted">Необязательно (10-12 цифр)</p>
								{/if}
							</div>
						</div>

						<!-- Category -->
						<div>
							<label for="category" class="block text-sm font-medium text-muted mb-2">
								Категория
							</label>
							<select
								id="category"
								bind:value={formData.category}
								class="w-full px-4 py-3 border border-border rounded-xl bg-gray-50 text-black focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none appearance-none"
								disabled={isSubmitting}
							>
								{#each categories as category}
									<option value={category.value}>{category.label}</option>
								{/each}
							</select>
						</div>

						<!-- Subject -->
						<div>
							<label for="subject" class="block text-sm font-medium text-muted mb-2">
								Тема <span class="text-error">*</span>
							</label>
							<input
								id="subject"
								type="text"
								bind:value={formData.subject}
								placeholder="О чём вы хотите написать?"
								class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none {errors.subject ? 'border-error' : 'border-border'}"
								disabled={isSubmitting}
							/>
							{#if errors.subject}
								<p class="mt-1.5 text-sm text-error">{errors.subject}</p>
							{/if}
						</div>

						<!-- Message -->
						<div>
							<label for="message" class="block text-sm font-medium text-muted mb-2">
								Сообщение <span class="text-error">*</span>
							</label>
							<textarea
								id="message"
								bind:value={formData.message}
								placeholder="Расскажите подробнее о вашем обращении..."
								rows="6"
								class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none resize-none {errors.message ? 'border-error' : 'border-border'}"
								disabled={isSubmitting}
							></textarea>
							{#if errors.message}
								<p class="mt-1.5 text-sm text-error">{errors.message}</p>
							{:else}
								<p class="mt-1.5 text-xs text-muted">Минимум 10 символов</p>
							{/if}
						</div>

						<!-- Submit Error -->
						{#if errors.submit}
							<div class="bg-error-light border border-error/20 rounded-xl p-4 flex items-start gap-3">
								<AlertCircle size={20} class="text-error flex-shrink-0" />
								<p class="text-sm text-error">{errors.submit}</p>
							</div>
						{/if}

						<!-- Submit Button -->
						<button
							type="submit"
							disabled={isSubmitting}
							class="w-full flex items-center justify-center gap-2 px-8 py-4 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-colors shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
						>
							{#if isSubmitting}
								<svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
								Отправка...
							{:else}
								<Send size={18} />
								Отправить сообщение
							{/if}
						</button>
					</form>
				</div>
			</div>

			<!-- Sidebar -->
			<div class="space-y-6">
				<!-- Business Hours -->
				<div class="bg-white rounded-lg p-6 shadow-sm border border-border">
					<div class="flex items-center gap-3 mb-5">
						<div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
							<Clock size={20} class="text-primary" />
						</div>
						<h3 class="text-lg font-semibold text-black">Часы работы</h3>
					</div>

					<div class="space-y-3">
						<div class="flex justify-between items-center py-2 border-b border-border">
							<span class="text-sm text-muted">Понедельник - Пятница</span>
							<span class="text-sm font-medium text-black">9:00 - 18:00</span>
						</div>
						<div class="flex justify-between items-center py-2">
							<span class="text-sm text-muted">Суббота и Воскресенье</span>
							<span class="text-sm font-medium text-error">Выходной</span>
						</div>
					</div>

					<div class="mt-4 pt-4 border-t border-border">
						<p class="text-xs text-muted flex items-center gap-2">
							<Clock size={12} />
							Индийское стандартное время (IST)
						</p>
					</div>
				</div>

				<!-- Quick Help -->
				<div class="bg-primary/10 rounded-lg p-6 border border-primary/20">
					<div class="flex items-center gap-3 mb-4">
						<div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-sm">
							<HelpCircle size={20} class="text-white" />
						</div>
						<h3 class="text-lg font-semibold text-black">Нужна быстрая помощь?</h3>
					</div>

					<p class="text-sm text-muted mb-5 leading-relaxed">
						Посетите наш центр помощи для мгновенных ответов на частые вопросы о вакансиях и откликах.
					</p>

					<a
						href="/help/"
						class="flex items-center justify-center gap-2 w-full px-5 py-2.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-colors shadow-sm"
					>
						Центр помощи
						<ArrowRight size={16} />
					</a>
				</div>

				<!-- FAQs Preview -->
				<div class="bg-white rounded-lg p-6 shadow-sm border border-border">
					<div class="flex items-center gap-3 mb-5">
						<div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
							<MessageCircle size={20} class="text-primary" />
						</div>
						<h3 class="text-lg font-semibold text-black">Быстрые вопросы</h3>
					</div>

					<div class="space-y-4">
						{#each faqs as faq}
							<div class="pb-4 border-b border-border last:border-0 last:pb-0">
								<h4 class="font-medium text-black text-sm mb-2">{faq.question}</h4>
								<p class="text-xs text-muted leading-relaxed">{faq.answer}</p>
							</div>
						{/each}
					</div>

					<a
						href="/help/"
						class="inline-flex items-center gap-1.5 text-primary hover:text-primary-hover font-medium text-sm mt-5 group"
					>
						Все вопросы
						<ArrowRight size={14} class="group-hover:translate-x-1 transition-transform" />
					</a>
				</div>
			</div>

		</div>
	</div>
</section>

<!-- Alternative Contact Methods -->
<section class="py-12 lg:py-20 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="max-w-5xl mx-auto">
			<div class="text-center mb-10 lg:mb-12">
				<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Другие способы связи</h2>
				<p class="text-base lg:text-lg text-muted">Выберите удобный для вас способ</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div class="group bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border">
					<div class="flex items-center gap-3 mb-4">
						<div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary transition-colors">
							<Mail size={24} class="text-primary group-hover:text-white transition-colors" />
						</div>
						<h3 class="text-xl font-semibold text-black">Для соискателей</h3>
					</div>
					<p class="text-muted mb-5 leading-relaxed">
						Возникли проблемы с аккаунтом, откликами или поиском работы? Наша команда поддержки готова помочь.
					</p>
					<a
						href="mailto:peeljobs@micropyramid.com"
						class="inline-flex items-center gap-2 text-primary hover:text-primary-hover font-medium group"
					>
						<Mail size={16} />
						<span class="break-all">peeljobs@micropyramid.com</span>
					</a>
				</div>

				<div class="group bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border">
					<div class="flex items-center gap-3 mb-4">
						<div class="w-12 h-12 rounded-xl bg-success-light flex items-center justify-center group-hover:bg-success transition-colors">
							<Mail size={24} class="text-success group-hover:text-white transition-colors" />
						</div>
						<h3 class="text-xl font-semibold text-black">Для работодателей</h3>
					</div>
					<p class="text-muted mb-5 leading-relaxed">
						Вопросы о публикации вакансий или управлении кандидатами? Мы поможем вам найти подходящих специалистов!
					</p>
					<a
						href="mailto:peeljobs@micropyramid.com"
						class="inline-flex items-center gap-2 text-success hover:text-success font-medium group"
					>
						<Mail size={16} />
						<span class="break-all">peeljobs@micropyramid.com</span>
					</a>
				</div>
			</div>
		</div>
	</div>
</section>
