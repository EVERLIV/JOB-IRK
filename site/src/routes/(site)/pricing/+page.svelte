<script lang="ts">
	import { Check, X, Zap, Users, TrendingUp, Shield, Clock, Heart, Award, Target, Sparkles, ArrowRight, BadgeCheck, ChevronRight, ChevronDown } from '@lucide/svelte';

	// Features included in the free plan
	const includedFeatures = [
		{ name: 'Безлимитные публикации вакансий', icon: Zap },
		{ name: 'Доступ ко всей базе кандидатов', icon: Users },
		{ name: 'Расширенный поиск и фильтры', icon: Target },
		{ name: 'Система отслеживания заявок', icon: TrendingUp },
		{ name: 'Email-уведомления', icon: Clock },
		{ name: 'Страница профиля компании', icon: BadgeCheck },
		{ name: 'Доступ к базе резюме', icon: Users },
		{ name: 'Переписка с кандидатами', icon: Heart },
		{ name: 'Приоритетная поддержка', icon: Shield },
		{ name: 'Аналитика и инсайты', icon: Award }
	];

	// What competitors charge for
	const competitorFeatures = [
		{ name: 'Платные публикации вакансий', free: true, competitors: false },
		{ name: 'Доступ к базе резюме', free: true, competitors: false },
		{ name: 'Рекомендованные публикации', free: true, competitors: false },
		{ name: 'Безлимитные заявки', free: true, competitors: false },
		{ name: 'Расширенная аналитика', free: true, competitors: false }
	];

	// FAQs
	const faqs = [
		{
			question: 'PeelJobs действительно на 100% бесплатный?',
			answer: "Да! Мы никогда не берём плату за публикации вакансий, доступ к кандидатам или любые функции рекрутинга. Наша миссия — связывать работодателей с лучшими специалистами в India без каких-либо затрат."
		},
		{
			question: 'Есть ли скрытые платежи или премиум-тарифы?',
			answer: "Никаких скрытых платежей. У нас нет премиум-тарифов, потому что мы считаем, что все работодатели заслуживают равного доступа к лучшим специалистам, независимо от бюджета."
		},
		{
			question: 'Как вы зарабатываете, если всё бесплатно?',
			answer: "Нас поддерживают стратегические партнёрства и рекламные показы. Мы никогда не снижаем качество платформы и не берём с работодателей плату за основные функции рекрутинга."
		},
		{
			question: 'Вы начнёте брать плату в будущем?',
			answer: "Нет. Мы обязуемся сохранять PeelJobs бесплатным навсегда. Наша цель — сделать качественный найм доступным для каждого работодателя в India, от стартапов до крупных компаний."
		},
		{
			question: 'Сколько вакансий я могу опубликовать?',
			answer: "Без ограничений! Публикуйте столько вакансий, сколько нужно, в любое время. Мы хотим помочь вам собрать всю команду, не заботясь о расходах."
		},
		{
			question: 'Могу ли я бесплатно получить доступ к базе резюме?',
			answer: 'Конечно! Вы получаете полный доступ к нашей базе из более чем 1 миллиона соискателей, включая расширенные фильтры поиска, не заплатив ни рупии.'
		},
		{
			question: 'Как быстро я смогу начать публиковать вакансии?',
			answer: 'Вы можете создать аккаунт и опубликовать первую вакансию менее чем за 5 минут. Кредитная карта не требуется, время ожидания одобрения — нулевое.'
		},
		{
			question: 'Какую поддержку я получу?',
			answer: "Все работодатели получают доступ к нашей выделенной команде поддержки по email и чату. Мы здесь, чтобы помочь вам найти подходящих специалистов."
		}
	];

	let openFaqIndex = $state<number | null>(null);

	function toggleFaq(index: number) {
		openFaqIndex = openFaqIndex === index ? null : index;
	}
</script>

<svelte:head>
	<title>Тарифы - 100% бесплатно навсегда | PeelJobs - Бесплатная платформа вакансий в India</title>
	<meta name="description" content="Публикуйте неограниченное количество вакансий БЕСПЛАТНО. Без скрытых платежей, без премиум-тарифов. Доступ к 1М+ кандидатам, продвинутые инструменты найма и безлимитные публикации вакансий бесплатно. Присоединяйтесь к 50К+ работодателям на PeelJobs." />
	<meta property="og:title" content="100% бесплатная платформа вакансий - Тарифы PeelJobs" />
	<meta property="og:description" content="Больше никогда не платите за публикации вакансий. Безлимитный бесплатный доступ к крупнейшему пулу талантов в India. Публикуйте вакансии, ищите резюме и нанимайте лучших кандидатов — всё бесплатно." />
	<meta property="og:type" content="website" />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="100% бесплатная платформа вакансий - Тарифы PeelJobs" />
	<meta name="twitter:description" content="Безлимитные публикации вакансий, доступ к базе резюме и инструменты найма — всё БЕСПЛАТНО навсегда." />
</svelte:head>

<!-- Hero Section -->
<section class="bg-[#1D2226] text-white py-16 lg:py-24 relative overflow-hidden">
	<!-- Decorative Elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-0 left-1/4 w-96 h-96 bg-success/20 rounded-full blur-3xl"></div>
		<div class="absolute bottom-0 right-1/4 w-80 h-80 bg-primary/10 rounded-full blur-3xl"></div>
	</div>

	<div class="max-w-7xl mx-auto px-4 lg:px-8 relative">
		<!-- Breadcrumb -->
		<nav class="mb-8" aria-label="Breadcrumb">
			<ol class="flex items-center gap-2 text-sm text-muted">
				<li>
					<a href="/" class="hover:text-white transition-colors">Главная</a>
				</li>
				<li class="flex items-center gap-2">
					<ChevronRight size={14} />
					<span class="text-white font-medium">Тарифы</span>
				</li>
			</ol>
		</nav>

		<div class="max-w-4xl mx-auto text-center">
			<!-- Free Badge -->
			<div class="inline-flex items-center gap-2 px-4 py-2 bg-success/20 text-success rounded-full text-sm font-medium mb-6 animate-fade-in-down" style="opacity: 0;">
				<Sparkles size={16} />
				<span>100% бесплатно навсегда</span>
			</div>

			<h1 class="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms;">
				Нанимайте лучших специалистов в India
				<span class="block text-success mt-2">Не потратив ни рупии</span>
			</h1>

			<p class="text-lg md:text-xl text-gray-300 leading-relaxed mb-10 max-w-3xl mx-auto animate-fade-in-up" style="opacity: 0; animation-delay: 200ms;">
				Присоединяйтесь к 50 000+ работодателей, которые доверяют PeelJobs свои задачи найма. Публикуйте безлимитные вакансии, получите доступ к 1 миллиону+ кандидатов и создайте команду мечты — всё <strong class="text-white">БЕСПЛАТНО</strong>.
			</p>

			<!-- CTA Buttons -->
			<div class="flex flex-col sm:flex-row gap-4 justify-center mb-10 animate-fade-in-up" style="opacity: 0; animation-delay: 300ms;">
				<a href="/employer/" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-black font-medium rounded-full hover:bg-gray-100 transition-colors shadow-sm">
					Начните нанимать бесплатно
					<ArrowRight size={18} />
				</a>
				<a href="#features" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/10 text-white font-medium rounded-full hover:bg-white/20 transition-colors border border-white/20">
					Посмотрите, что включено
				</a>
			</div>

			<!-- Trust Indicators -->
			<div class="flex flex-wrap justify-center gap-6 text-sm text-muted animate-fade-in-up" style="opacity: 0; animation-delay: 400ms;">
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Кредитная карта не требуется</span>
				</div>
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Без скрытых платежей</span>
				</div>
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Настройка за 5 минут</span>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- Pricing Card Section -->
<section id="features" class="py-16 lg:py-24 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Один простой тариф. Всё включено.</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Без уровней, без допродаж, без сложных тарифов. Одна мощная платформа со всем необходимым для найма.
			</p>
		</div>

		<!-- Main Pricing Card -->
		<div class="max-w-2xl mx-auto">
			<div class="bg-white rounded-lg shadow-lg overflow-hidden border-2 border-primary relative">
				<!-- Popular Badge -->
				<div class="absolute top-0 right-0 bg-primary text-white px-5 py-2 text-sm font-medium rounded-bl-lg">
					Популярный
				</div>

				<div class="p-8 lg:p-10">
					<!-- Plan Header -->
					<div class="text-center mb-8">
						<h3 class="text-2xl lg:text-3xl font-semibold text-black mb-4">Бесплатный тариф навсегда</h3>
						<div class="mb-4">
							<span class="text-6xl lg:text-7xl font-semibold text-primary">₹0</span>
							<span class="text-2xl text-muted ml-2">навсегда</span>
						</div>
						<p class="text-muted text-lg">Всё, что нужно для создания команды. Без подвоха.</p>
					</div>

					<!-- Features List -->
					<div class="space-y-4 mb-8">
						{#each includedFeatures as feature, i}
							{@const FeatureIcon = feature.icon}
							<div class="flex items-start gap-3 animate-fade-in-up" style="opacity: 0; animation-delay: {i * 50}ms;">
								<div class="w-6 h-6 rounded-full bg-success-light flex items-center justify-center flex-shrink-0 mt-0.5">
									<Check size={14} class="text-success" />
								</div>
								<div class="flex items-center gap-3 flex-1">
									<FeatureIcon size={18} class="text-primary flex-shrink-0" />
									<span class="text-muted font-medium">{feature.name}</span>
								</div>
							</div>
						{/each}
					</div>

					<!-- CTA Button -->
					<a href="/employer/" class="w-full flex items-center justify-center gap-2 px-8 py-4 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-colors shadow-sm hover:shadow-md">
						Начать бесплатно
						<ArrowRight size={18} />
					</a>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- Comparison Section -->
<section class="py-16 lg:py-24 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Сравнение с конкурентами</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Узнайте, за что другие платформы берут тысячи — и что мы даём бесплатно.
			</p>
		</div>

		<div class="max-w-4xl mx-auto">
			<div class="bg-white rounded-lg shadow-sm overflow-hidden border border-border">
				<!-- Header Row -->
				<div class="grid grid-cols-3 bg-surface border-b border-border">
					<div class="p-4 lg:p-6"></div>
					<div class="p-4 lg:p-6 text-center border-l border-border">
						<div class="font-semibold text-primary text-lg lg:text-xl">PeelJobs</div>
						<div class="text-xs lg:text-sm text-muted mt-1">Бесплатно навсегда</div>
					</div>
					<div class="p-4 lg:p-6 text-center border-l border-border">
						<div class="font-semibold text-black text-lg lg:text-xl">Конкуренты</div>
						<div class="text-xs lg:text-sm text-muted mt-1">₹10K-50K/month</div>
					</div>
				</div>

				<!-- Feature Rows -->
				{#each competitorFeatures as feature}
					<div class="grid grid-cols-3 border-b border-border last:border-b-0 hover:bg-surface transition-colors">
						<div class="p-4 lg:p-6 font-medium text-muted text-sm lg:text-base">{feature.name}</div>
						<div class="p-4 lg:p-6 text-center border-l border-border">
							{#if feature.free}
								<div class="inline-flex items-center justify-center w-8 h-8 bg-success-light rounded-full">
									<Check size={16} class="text-success" />
								</div>
							{:else}
								<div class="inline-flex items-center justify-center w-8 h-8 bg-error-light rounded-full">
									<X size={16} class="text-error" />
								</div>
							{/if}
						</div>
						<div class="p-4 lg:p-6 text-center border-l border-border">
							{#if feature.competitors}
								<div class="inline-flex items-center justify-center w-8 h-8 bg-success-light rounded-full">
									<Check size={16} class="text-success" />
								</div>
							{:else}
								<div class="inline-flex items-center justify-center w-8 h-8 bg-error-light rounded-full">
									<X size={16} class="text-error" />
								</div>
								<div class="text-xs text-muted mt-1 hidden lg:block">Доп. оплата</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</section>

<!-- Why Free Section -->
<section class="py-16 lg:py-24 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Почему PeelJobs бесплатный?</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Наша миссия проста: связывать работодателей с лучшими специалистами в India без финансовых барьеров.
			</p>
		</div>

		<div class="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
			<div class="bg-white rounded-lg p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="w-14 h-14 bg-primary/10 rounded-lg flex items-center justify-center mb-6">
					<Heart size={28} class="text-primary" />
				</div>
				<h3 class="text-xl font-semibold text-black mb-4">Наша миссия</h3>
				<p class="text-muted leading-relaxed">
					Мы считаем, что каждая компания — от стартапа до корпорации — заслуживает доступа к лучшим специалистам без ограничений бюджета, тормозящих рост.
				</p>
			</div>

			<div class="bg-white rounded-lg p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="w-14 h-14 bg-success-light rounded-lg flex items-center justify-center mb-6">
					<Users size={28} class="text-success" />
				</div>
				<h3 class="text-xl font-semibold text-black mb-4">Больше возможностей</h3>
				<p class="text-muted leading-relaxed">
					Устраняя плату за публикации, мы создаём больше возможностей для соискателей и помогаем работодателям находить кандидатов, до которых иначе не добрались бы из-за стоимости.
				</p>
			</div>

			<div class="bg-white rounded-lg p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="w-14 h-14 bg-primary/10 rounded-lg flex items-center justify-center mb-6">
					<TrendingUp size={28} class="text-primary" />
				</div>
				<h3 class="text-xl font-semibold text-black mb-4">Лучшие результаты</h3>
				<p class="text-muted leading-relaxed">
					Когда больше работодателей могут публиковать вакансии, а больше кандидатов откликаются, выигрывают все. Мы измеряем успех успешными наймами, а не выручкой.
				</p>
			</div>
		</div>
	</div>
</section>

<!-- FAQ Section -->
<section class="py-16 lg:py-24 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Частые вопросы</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Всё, что нужно знать о нашей бесплатной платформе
			</p>
		</div>

		<div class="max-w-3xl mx-auto space-y-3">
			{#each faqs as faq, index}
				<div class="bg-surface rounded-lg border border-border hover:border-primary/30 transition-colors overflow-hidden">
					<button onclick={() => toggleFaq(index)} class="w-full px-6 py-5 text-left flex justify-between items-center gap-4">
						<span class="font-semibold text-black text-base lg:text-lg">{faq.question}</span>
						<div class="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
							<ChevronDown size={18} class="text-primary transform transition-transform {openFaqIndex === index ? 'rotate-180' : ''}" />
						</div>
					</button>
					{#if openFaqIndex === index}
						<div class="px-6 pb-5 text-muted leading-relaxed animate-fade-in">
							{faq.answer}
						</div>
					{/if}
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- Final CTA Section -->
<section class="py-16 lg:py-24 bg-[#1D2226] text-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8 text-center">
		<div class="max-w-3xl mx-auto">
			<h2 class="text-2xl lg:text-3xl font-semibold tracking-tight mb-6">Готовы начать нанимать?</h2>
			<p class="text-lg text-gray-300 mb-10 leading-relaxed">
				Присоединяйтесь к тысячам работодателей, которые создают отличные команды, не потратив ни рупии. Создайте бесплатный аккаунт за несколько минут и опубликуйте первую вакансию уже сегодня.
			</p>

			<div class="flex flex-col sm:flex-row gap-4 justify-center mb-10">
				<a href="/employer/" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-black font-medium rounded-full hover:bg-gray-100 transition-colors shadow-sm">
					Создать бесплатный аккаунт
					<ArrowRight size={18} />
				</a>
				<a href="/contact/" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/10 text-white font-medium rounded-full hover:bg-white/20 transition-colors border border-white/20">
					Поговорить с командой
				</a>
			</div>

			<div class="flex flex-wrap justify-center gap-6 text-sm text-muted">
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Бесплатно навсегда</span>
				</div>
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Без кредитной карты</span>
				</div>
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Настройка за 5 минут</span>
				</div>
				<div class="flex items-center gap-2">
					<Check size={16} class="text-success" />
					<span>Безлимитные публикации</span>
				</div>
			</div>
		</div>
	</div>
</section>
