<script lang="ts">
	import {
		Zap,
		Users,
		Building2,
		Target,
		Shield,
		Award,
		CheckCircle2,
		ChevronRight,
		Heart,
		DollarSign,
		Lightbulb,
		Globe,
		Rocket,
		ArrowRight,
		Sparkles
	} from '@lucide/svelte';

	const coreValues = [
		{
			icon: Shield,
			title: 'Справедливость',
			description: 'Каждая компания заслуживает доступа к отличным талантам, и каждый соискатель заслуживает доступа к отличным возможностям — без платных стен или искусственных барьеров.'
		},
		{
			icon: Shield,
			title: 'Прозрачность',
			description: 'Мы способствуем открытому, честному общению между работодателями и кандидатами с чёткими ожиданиями и понятными процессами.'
		},
		{
			icon: Users,
			title: 'Ориентированность на пользователя',
			description: 'Наша платформа разработана с глубоким пониманием как рекрутеров, так и соискателей и непрерывно совершенствуется на основе реальных отзывов пользователей.'
		},
		{
			icon: Award,
			title: 'Совершенство',
			description: 'Мы стремимся к техническому совершенству, операционной эффективности и выдающемуся пользовательскому опыту во всём, что мы создаём.'
		},
		{
			icon: Heart,
			title: 'Влияние на общество',
			description: 'Мы стремимся оказывать позитивное социальное влияние, связывая людей со значимой работой и помогая бизнесу процветать.'
		}
	];

	const features = [
		{
			icon: DollarSign,
			title: 'Полностью бесплатно',
			description: 'Нулевая стоимость размещения вакансий и доступа к кандидатам. Никаких скрытых платежей, никаких платных стен — только бесплатный, доступный найм для всех.'
		},
		{
			icon: Zap,
			title: 'Быстро и эффективно',
			description: 'Оптимизированный процесс найма с интуитивными инструментами, интеллектуальным поиском и автоматизированными рабочими процессами, экономящими часы работы.'
		},
		{
			icon: Target,
			title: 'Умный подбор',
			description: 'Расширенные фильтры и рекомендации на основе ИИ помогают быстрее найти идеальное совпадение.'
		}
	];

	const benefits = {
		jobSeekers: [
			'Доступ к разнообразным вакансиям во всех отраслях и регионах',
			'Расширенные фильтры по навыкам, местоположению, опыту и типу работы',
			'Полные профили для демонстрации ваших достижений',
			'Мгновенные уведомления о подходящих вакансиях',
			'Полностью бесплатно — никаких платежей за отклики или поиск'
		],
		companies: [
			'Размещайте неограниченное количество вакансий бесплатно',
			'Доступ к большой, постоянно обновляемой базе кандидатов',
			'Профессиональные профили компаний для привлечения лучших талантов',
			'Аналитика и отчётность для оптимизации стратегии найма',
			'Эффективные инструменты отслеживания и коммуникации с кандидатами'
		]
	};

	const missionPillars = [
		{ icon: DollarSign, title: 'Доступность', description: 'Бесплатная платформа, обеспечивающая бизнесам любого размера доступ к лучшим талантам без финансовых барьеров.' },
		{ icon: Zap, title: 'Эффективность', description: 'Оптимизированный найм с интуитивными инструментами для более быстрых и эффективных решений о приёме на работу.' },
		{ icon: Users, title: 'Расширение возможностей', description: 'Поддержка соискателей с равным доступом к возможностям и помощь компаниям в создании сильных команд.' },
		{ icon: Lightbulb, title: 'Инновации', description: 'Непрерывное совершенствование платформы с передовыми функциями для удовлетворения меняющихся потребностей рынка труда.' },
		{ icon: Shield, title: 'Качество и доверие', description: 'Поддержание высоких стандартов с проверенными профилями, подлинными вакансиями и прозрачным общением.' }
	];
</script>

<svelte:head>
	<title>О нас - PeelJobs | Бесплатный портал вакансий, демократизирующий найм</title>
	<meta
		name="description"
		content="PeelJobs — бесплатный портал вакансий, связывающий таланты с возможностями. Узнайте о нашей миссии демократизировать найм, делая исключительный рекрутинг доступным для бизнеса любого размера без финансовых барьеров."
	/>
	<link rel="canonical" href="https://peeljobs.com/about/" />

	<!-- Open Graph -->
	<meta property="og:title" content="О PeelJobs - Демократизация найма, одно соединение за раз" />
	<meta property="og:description" content="Узнайте, как PeelJobs преображает рекрутинг с нашей бесплатной, доступной платформой, которая помогает как компаниям, так и соискателям." />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://peeljobs.com/about/" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="О PeelJobs - Бесплатный портал вакансий" />
	<meta name="twitter:description" content="Узнайте о нашей миссии демократизировать найм для всех." />
</svelte:head>

<!-- Hero Section -->
<section class="bg-[#1D2226] text-white py-16 lg:py-24 relative overflow-hidden">
	<!-- Decorative Elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
		<div class="absolute bottom-0 right-1/4 w-80 h-80 bg-primary/10 rounded-full blur-3xl"></div>
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
					<span class="text-white font-medium">О нас</span>
				</li>
			</ol>
		</nav>

		<!-- Hero Content -->
		<div class="text-center max-w-4xl mx-auto">
			<div class="inline-flex items-center gap-2 px-4 py-2 bg-primary/20 text-white/80 rounded-full text-sm font-medium mb-6 animate-fade-in-down" style="opacity: 0;">
				<Sparkles size={16} />
				<span>100% бесплатно навсегда</span>
			</div>

			<div class="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-8 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms;">
				<Rocket size={40} class="text-primary" />
			</div>

			<h1 class="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 animate-fade-in-up" style="opacity: 0; animation-delay: 200ms;">
				Демократизация найма,<br class="hidden md:block" />
				одно соединение за раз
			</h1>

			<p class="text-lg md:text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed animate-fade-in-up" style="opacity: 0; animation-delay: 300ms;">
				Наша миссия — сделать исключительный найм доступным для каждой организации,
				независимо от размера и бюджета, помогая соискателям находить значимую работу.
			</p>
		</div>
	</div>
</section>

<!-- Vision & Mission Cards -->
<section class="py-16 lg:py-24 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="grid md:grid-cols-2 gap-6 lg:gap-8">
			<!-- Vision -->
			<div class="bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="flex items-center gap-4 mb-5">
					<div class="w-14 h-14 rounded-lg bg-primary/20 flex items-center justify-center">
						<Globe size={28} class="text-primary" />
					</div>
					<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight">Наша визия</h2>
				</div>
				<p class="text-base lg:text-lg text-muted leading-relaxed">
					Стать ведущим бесплатным порталом вакансий, который преображает связь между компаниями и талантами,
					создавая будущее, где исключительный найм доступен каждой организации, независимо
					от размера и бюджета.
				</p>
			</div>

			<!-- Aim -->
			<div class="bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="flex items-center gap-4 mb-5">
					<div class="w-14 h-14 rounded-lg bg-success-light flex items-center justify-center">
						<Target size={28} class="text-success" />
					</div>
					<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight">Наша цель</h2>
				</div>
				<p class="text-base lg:text-lg text-muted leading-relaxed">
					Создать динамическую платформу, которая помогает компаниям связываться с исключительными талантами
					бесплатно, создавая возможности для значимой занятости и способствуя организационному
					росту через доступный, справедливый и эффективный найм.
				</p>
			</div>
		</div>
	</div>
</section>

<!-- Mission Section -->
<section class="py-16 lg:py-24 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="bg-primary/10 rounded-lg p-8 lg:p-12 border border-primary/20">
			<div class="text-center mb-10 lg:mb-12">
				<div class="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
					<Zap size={32} class="text-primary" />
				</div>
				<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Наша миссия</h2>
				<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
					Мы демократизируем процесс найма, предоставляя бесплатный, удобный портал вакансий, который
					устраняет разрыв между компаниями и талантливыми людьми.
				</p>
			</div>

			<div class="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 lg:gap-6">
				{#each missionPillars as pillar, i}
					<div
						class="bg-white rounded-lg p-5 lg:p-6 shadow-sm hover:shadow-lg transition-all animate-fade-in-up"
						style="opacity: 0; animation-delay: {i * 100}ms;"
					>
						<div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
							<svelte:component this={pillar.icon} size={20} class="text-primary" />
						</div>
						<h3 class="font-semibold text-black mb-2">{pillar.title}</h3>
						<p class="text-sm text-muted leading-relaxed">{pillar.description}</p>
					</div>
				{/each}
			</div>
		</div>
	</div>
</section>

<!-- Core Values -->
<section class="py-16 lg:py-24 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-10 lg:mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Наши ценности</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Эти фундаментальные принципы направляют всё, что мы делаем в PeelJobs
			</p>
		</div>

		<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each coreValues as value, i}
				<div
					class="group bg-white rounded-lg p-6 shadow-sm hover:shadow-lg transition-all border border-border animate-fade-in-up"
					style="opacity: 0; animation-delay: {i * 100}ms;"
				>
					<div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-5 group-hover:bg-primary/20 transition-colors">
						<svelte:component this={value.icon} size={24} class="text-primary" />
					</div>
					<h3 class="text-lg lg:text-xl font-semibold text-black mb-3">{value.title}</h3>
					<p class="text-sm lg:text-base text-muted leading-relaxed">{value.description}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- Key Features -->
<section class="py-16 lg:py-24 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-10 lg:mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Почему PeelJobs?</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Мы больше, чем просто доска вакансий — мы ваш партнёр в построении успешных карьер и команд
			</p>
		</div>

		<div class="grid md:grid-cols-3 gap-6 lg:gap-8">
			{#each features as feature, i}
				<div
					class="bg-surface rounded-lg p-6 lg:p-8 border border-border hover:border-primary/30 hover:bg-primary/10 transition-all animate-fade-in-up"
					style="opacity: 0; animation-delay: {i * 100}ms;"
				>
					<div class="w-14 h-14 bg-primary rounded-lg flex items-center justify-center mb-5 shadow-sm">
						<svelte:component this={feature.icon} size={28} class="text-white" />
					</div>
					<h3 class="text-lg lg:text-xl font-semibold text-black mb-3">{feature.title}</h3>
					<p class="text-sm lg:text-base text-muted leading-relaxed">{feature.description}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- How We Deliver Value -->
<section class="py-16 lg:py-24 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="text-center mb-10 lg:mb-12">
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Как мы создаём ценность</h2>
			<p class="text-base lg:text-lg text-muted max-w-3xl mx-auto">
				Конкретные преимущества для соискателей и компаний
			</p>
		</div>

		<div class="grid md:grid-cols-2 gap-6 lg:gap-8">
			<!-- For Job Seekers -->
			<div class="bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="flex items-center gap-4 mb-6">
					<div class="w-12 h-12 bg-success-light rounded-xl flex items-center justify-center">
						<Users size={24} class="text-success" />
					</div>
					<h3 class="text-xl lg:text-2xl font-semibold text-black">Для соискателей</h3>
				</div>
				<ul class="space-y-4">
					{#each benefits.jobSeekers as benefit}
						<li class="flex items-start gap-3">
							<div class="w-5 h-5 rounded-full bg-success-light flex items-center justify-center flex-shrink-0 mt-0.5">
								<CheckCircle2 size={14} class="text-success" />
							</div>
							<span class="text-sm lg:text-base text-muted">{benefit}</span>
						</li>
					{/each}
				</ul>
			</div>

			<!-- For Companies -->
			<div class="bg-white rounded-lg p-6 lg:p-8 shadow-sm hover:shadow-lg transition-all border border-border">
				<div class="flex items-center gap-4 mb-6">
					<div class="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center">
						<Building2 size={24} class="text-primary" />
					</div>
					<h3 class="text-xl lg:text-2xl font-semibold text-black">Для компаний</h3>
				</div>
				<ul class="space-y-4">
					{#each benefits.companies as benefit}
						<li class="flex items-start gap-3">
							<div class="w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
								<CheckCircle2 size={14} class="text-primary" />
							</div>
							<span class="text-sm lg:text-base text-muted">{benefit}</span>
						</li>
					{/each}
				</ul>
			</div>
		</div>
	</div>
</section>

<!-- Our Commitment -->
<section class="py-16 lg:py-24 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="bg-surface rounded-lg p-8 lg:p-12 border border-border text-center max-w-4xl mx-auto">
			<div class="w-14 h-14 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
				<Heart size={28} class="text-primary" />
			</div>
			<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-4">Наши обязательства</h2>
			<p class="text-base lg:text-lg text-muted leading-relaxed mb-6">
				Способствуя прозрачным и совместным связям, мы стремимся преобразовать ландшафт
				рекрутинга, сделав его более справедливым, ориентированным на возможности и эффективным для всех участников.
			</p>
			<p class="text-sm lg:text-base text-muted italic">
				Мы измеряем наш успех не только в цифрах, но и в значимых карьерах, запущенных и
				успешных командах, созданных на нашей платформе.
			</p>
		</div>
	</div>
</section>

<!-- Call to Action -->
<section class="py-16 lg:py-24 bg-[#1D2226] text-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8 text-center">
		<div class="max-w-3xl mx-auto">
			<h2 class="text-2xl lg:text-3xl font-semibold tracking-tight mb-4">
				Готовы ощутить разницу с PeelJobs?
			</h2>
			<p class="text-base lg:text-lg text-gray-300 mb-8 lg:mb-10">
				Присоединяйтесь к тысячам соискателей и компаний, которые открыли лучший способ связи.
				Это полностью бесплатно и всегда будет.
			</p>
			<div class="flex flex-col sm:flex-row gap-4 justify-center">
				<a
					href="/jobs/"
					class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-black font-medium rounded-full hover:bg-gray-100 transition-colors shadow-sm"
				>
					Искать вакансии
					<ArrowRight size={18} />
				</a>
				<a
					href="/contact/"
					class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/10 text-white font-medium rounded-full hover:bg-white/20 transition-colors border border-white/20"
				>
					Связаться с нами
				</a>
			</div>
		</div>
	</div>
</section>
