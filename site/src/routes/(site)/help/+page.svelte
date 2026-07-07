<script lang="ts">
	import { HelpCircle, Search, ChevronDown, ChevronUp, Book, UserCircle, Briefcase, Settings, MessageCircle, Shield, ChevronRight, ArrowRight } from '@lucide/svelte';

	type IconComponent = typeof HelpCircle;

	interface Category {
		id: 'all' | 'getting_started' | 'account' | 'job_search' | 'applications' | 'privacy' | 'technical';
		name: string;
		icon: IconComponent;
	}

	type CategoryId = Category['id'];

	interface FaqItem {
		id: number;
		category: Exclude<CategoryId, 'all'>;
		question: string;
		answer: string;
	}

	interface Article {
		title: string;
		description: string;
		category: string;
		readTime: string;
	}

	let searchQuery = $state('');
	let selectedCategory = $state<CategoryId>('all');
	let expandedFaqId = $state<number | null>(null);

	const categories: Category[] = [
		{ id: 'all', name: 'Все темы', icon: HelpCircle },
		{ id: 'getting_started', name: 'Начало работы', icon: Book },
		{ id: 'account', name: 'Аккаунт и профиль', icon: UserCircle },
		{ id: 'job_search', name: 'Поиск вакансий', icon: Search },
		{ id: 'applications', name: 'Отклики', icon: Briefcase },
		{ id: 'privacy', name: 'Приватность и безопасность', icon: Shield },
		{ id: 'technical', name: 'Технические проблемы', icon: Settings }
	];

	const faqs: FaqItem[] = [
		// Getting Started
		{
			id: 1,
			category: 'getting_started',
			question: 'Как создать аккаунт на PeelJobs?',
			answer: 'Чтобы создать аккаунт, нажмите «Регистрация» в правом верхнем углу главной страницы. Вы можете зарегистрироваться используя свой email или Google/Facebook для быстрой регистрации. Заполните основные данные, подтвердите свой email, и вы готовы начать поиск вакансий!'
		},
		{
			id: 2,
			category: 'getting_started',
			question: 'Бесплатно ли PeelJobs для соискателей?',
			answer: 'Да! PeelJobs полностью бесплатен для соискателей. Вы можете создать аккаунт, искать вакансии, откликаться на неограниченное количество позиций и использовать все наши функции без каких-либо платежей.'
		},
		{
			id: 3,
			category: 'getting_started',
			question: 'Какие преимущества даёт создание профиля?',
			answer: 'Создание профиля позволяет вам сохранять вакансии, быстро откликаться с сохранённым резюме, отслеживать статус откликов, получать персонализированные рекомендации вакансий и уведомления о новых вакансиях, соответствующих вашим предпочтениям.'
		},

		// Account & Profile
		{
			id: 4,
			category: 'account',
			question: 'Как обновить информацию в профиле?',
			answer: 'Перейдите в свой профиль, нажав на своё имя в правом верхнем углу, затем выберите «Профиль». Вы можете изменить личную информацию, добавить опыт работы, образование, навыки и загрузить резюме. Обязательно сохраните изменения!'
		},
		{
			id: 5,
			category: 'account',
			question: 'Как изменить пароль?',
			answer: 'Перейдите в Настройки > Пароль из меню аккаунта. Введите текущий пароль, затем новый пароль дважды для подтверждения. Пароль должен содержать не менее 8 символов и включать заглавные и строчные буквы, а также цифры.'
		},
		{
			id: 6,
			category: 'account',
			question: 'Можно ли удалить аккаунт?',
			answer: 'Да, вы можете удалить аккаунт, перейдя в Настройки > Приватность и прокрутив вниз. Обратите внимание, что удаление аккаунта необратимо, и все ваши данные, отклики и сохранённые вакансии будут удалены навсегда.'
		},
		{
			id: 7,
			category: 'account',
			question: 'Как загрузить или обновить резюме?',
			answer: 'Перейдите на страницу Профиля и прокрутите до раздела Резюме. Нажмите «Загрузить резюме», чтобы добавить новое PDF-резюме (максимум 5 МБ). Вы можете загрузить несколько резюме и установить одно как основное для быстрых откликов.'
		},

		// Job Search
		{
			id: 8,
			category: 'job_search',
			question: 'Как искать вакансии?',
			answer: 'Используйте строку поиска на главной странице или перейдите на страницу Вакансий. Вы можете искать по ключевым словам (название должности, навыки, компания), местоположению и применять фильтры по типу вакансии, уровню зарплаты, опыту и другим параметрам. Расширенные фильтры помогут найти именно то, что вы ищете.'
		},
		{
			id: 9,
			category: 'job_search',
			question: 'Как сохранить вакансию для отклика позже?',
			answer: 'Нажмите на значок закладки/звезды в любом списке вакансий, чтобы сохранить её на потом. Доступ ко всем сохранённым вакансиям можно получить из панели управления или со страницы «Сохранённые вакансии» в меню аккаунта.'
		},
		{
			id: 10,
			category: 'job_search',
			question: 'Что такое уведомления о вакансиях и как их настроить?',
			answer: 'Уведомления о вакансиях оповещают вас, когда публикуются новые вакансии, соответствующие вашим критериям. Перейдите в Настройки > Уведомления о вакансиях, чтобы создать пользовательские уведомления по ключевым словам, местоположению, типу вакансии и зарплате. Выберите частоту получения уведомлений (мгновенно, ежедневно или еженедельно).'
		},
		{
			id: 11,
			category: 'job_search',
			question: 'Как работает алгоритм подбора вакансий?',
			answer: 'Наша система подбора на базе ИИ анализирует ваш профиль, навыки, опыт и предпочтения, чтобы рекомендовать вакансии, наиболее подходящие вашей квалификации. Чем полнее ваш профиль, тем точнее рекомендации!'
		},

		// Applications
		{
			id: 12,
			category: 'applications',
			question: 'Как откликнуться на вакансию?',
			answer: 'Нажмите на любую вакансию, чтобы увидеть подробности, затем нажмите «Откликнуться». Вам нужно выбрать резюме и при необходимости добавить сопроводительное письмо. Проверьте свой отклик и отправьте. Вы можете отслеживать все отклики из панели управления.'
		},
		{
			id: 13,
			category: 'applications',
			question: 'Можно ли отозвать отклик?',
			answer: 'В настоящее время после отправки отклика его нельзя отозвать через платформу. Однако вы можете связаться с рекрутером напрямую через нашу систему сообщений, чтобы отозвать свой отклик.'
		},
		{
			id: 14,
			category: 'applications',
			question: 'Как отследить статус моего отклика?',
			answer: 'Перейдите на страницу «Отклики» из панели управления, чтобы увидеть все отправленные отклики. Каждый отклик показывает текущий статус (На рассмотрении, В шортлисте, Назначено интервью и т.д.) и хронологию.'
		},
		{
			id: 15,
			category: 'applications',
			question: 'Почему мой отклик был отклонён?',
			answer: 'Решения по откликам принимаются работодателями на основе их конкретных требований. Хотя у нас нет доступа к их критериям отбора, вы можете написать рекрутеру для получения обратной связи или продолжить откликаться на другие позиции, соответствующие вашему профилю.'
		},

		// Privacy & Security
		{
			id: 16,
			category: 'privacy',
			question: 'Как защищены мои персональные данные?',
			answer: 'Мы используем отраслевые стандарты шифрования и меры безопасности для защиты ваших данных. Ваша информация никогда не передаётся третьим лицам без вашего явного согласия. Прочитайте нашу Политику конфиденциальности для подробной информации.'
		},
		{
			id: 17,
			category: 'privacy',
			question: 'Могу ли я контролировать, кто видит мой профиль?',
			answer: 'Да! Перейдите в Настройки > Приватность, чтобы управлять видимостью профиля. Вы можете сделать его публичным, видимым только для проверенных рекрутеров или полностью приватным. Вы также можете управлять отдельными элементами, такими как видимость контактной информации.'
		},
		{
			id: 18,
			category: 'privacy',
			question: 'Как сообщить о подозрительной вакансии?',
			answer: 'Если вы обнаружили подозрительную вакансию, нажмите кнопку «Пожаловаться» на странице вакансии. Укажите подробности о том, почему вы считаете её подозрительной. Наша команда рассматривает все жалобы в течение 24 часов.'
		},

		// Technical Issues
		{
			id: 19,
			category: 'technical',
			question: 'Сайт загружается некорректно. Что делать?',
			answer: 'Попробуйте очистить кэш и файлы cookie браузера или используйте другой браузер. Убедитесь, что вы используете обновлённую версию браузера. Если проблема сохраняется, обратитесь в нашу службу поддержки с указанием вашего браузера и операционной системы.'
		},
		{
			id: 20,
			category: 'technical',
			question: 'Я не получаю email-уведомления. Как это исправить?',
			answer: 'Проверьте папку со спамом на наличие писем от PeelJobs. Добавьте support@peeljobs.com в контакты. Также убедитесь, что email-уведомления включены в Настройки > Уведомления. Если проблема сохраняется, обратитесь в поддержку.'
		},
		{
			id: 21,
			category: 'technical',
			question: 'Загрузка резюме не удаётся. Какие форматы поддерживаются?',
			answer: 'В настоящее время мы поддерживаем только формат PDF. Размер резюме не должен превышать 5 МБ. Убедитесь, что ваш PDF не защищён паролем. Если проблемы продолжаются, попробуйте конвертировать резюме в PDF с помощью другого инструмента.'
		}
	];

	const popularArticles: Article[] = [
		{
			title: 'Как создать успешное резюме',
			description: 'Советы и лучшие практики для создания выдающегося резюме',
			category: 'Начало работы',
			readTime: '5 мин чтения'
		},
		{
			title: 'Руководство по подготовке к интервью',
			description: 'Полное руководство по подготовке к собеседованиям',
			category: 'Поиск вакансий',
			readTime: '8 мин чтения'
		},
		{
			title: 'Понимание статуса отклика',
			description: 'Что означает каждый статус отклика и чего ожидать',
			category: 'Отклики',
			readTime: '3 мин чтения'
		}
	];

	// Filter FAQs
	const filteredFaqs = $derived((): FaqItem[] => {
		const query = searchQuery.toLowerCase().trim();
		return faqs.filter((faq) => {
			const matchesCategory = selectedCategory === 'all' || faq.category === selectedCategory;
			const matchesSearch = query === '' || faq.question.toLowerCase().includes(query) || faq.answer.toLowerCase().includes(query);

			return matchesCategory && matchesSearch;
		});
	});

	function toggleFaq(id: number): void {
		expandedFaqId = expandedFaqId === id ? null : id;
	}

	function selectCategory(categoryId: CategoryId): void {
		selectedCategory = categoryId;
		expandedFaqId = null;
	}
</script>

<svelte:head>
	<title>Помощь - PeelJobs | Найдите ответы на ваши вопросы</title>
	<meta name="description" content="Найдите ответы на частые вопросы об использовании PeelJobs. Узнайте, как искать вакансии, создавать профиль, откликаться на позиции и многое другое." />
	<link rel="canonical" href="https://peeljobs.com/help/" />
</svelte:head>

<!-- Hero Section -->
<section class="bg-[#1D2226] text-white py-16 lg:py-24 relative overflow-hidden">
	<!-- Decorative Elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-0 left-1/3 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
		<div class="absolute bottom-0 right-1/3 w-80 h-80 bg-primary/10 rounded-full blur-3xl"></div>
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
					<span class="text-white font-medium">Помощь</span>
				</li>
			</ol>
		</nav>

		<div class="max-w-3xl mx-auto text-center">
			<div class="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-8 animate-fade-in-up" style="opacity: 0;">
				<HelpCircle size={40} class="text-primary" />
			</div>
			<h1 class="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms;">Чем мы можем помочь?</h1>
			<p class="text-lg md:text-xl text-gray-300 mb-10 animate-fade-in-up" style="opacity: 0; animation-delay: 200ms;">Ищите в нашей базе знаний быстрые ответы на ваши вопросы</p>

			<!-- Search Bar -->
			<div class="relative max-w-2xl mx-auto animate-fade-in-up" style="opacity: 0; animation-delay: 300ms;">
				<div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
					<Search size={20} class="text-muted" />
				</div>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Поиск статей помощи, частых вопросов..."
					class="w-full pl-14 pr-5 py-4 bg-white text-black rounded-full focus:outline-none focus:ring-4 focus:ring-primary/30 text-base placeholder-muted shadow-md"
				/>
			</div>
		</div>
	</div>
</section>

<!-- Popular Articles -->
{#if searchQuery === ''}
	<section class="py-12 lg:py-16 bg-surface">
		<div class="max-w-7xl mx-auto px-4 lg:px-8">
			<div class="max-w-6xl mx-auto">
				<div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
					<div>
						<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight">Популярные статьи</h2>
						<p class="text-muted mt-2">Быстрые руководства для начала работы</p>
					</div>
				</div>

				<div class="grid md:grid-cols-3 gap-6">
					{#each popularArticles as article, i}
						<div
							class="group bg-white rounded-lg p-6 shadow-sm hover:shadow-lg transition-all border border-border cursor-pointer animate-fade-in-up"
							style="opacity: 0; animation-delay: {i * 100}ms;"
						>
							<div class="mb-4">
								<span class="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">{article.category}</span>
							</div>
							<h3 class="text-lg font-semibold text-black mb-2 group-hover:text-primary transition-colors">{article.title}</h3>
							<p class="text-sm text-muted mb-4">{article.description}</p>
							<p class="text-xs text-muted">{article.readTime}</p>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</section>
{/if}

<!-- Main Content -->
<section class="py-12 lg:py-20 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="max-w-6xl mx-auto">
			<!-- Category Filters -->
			<div class="mb-10">
				<h2 class="text-2xl lg:text-3xl font-semibold text-black tracking-tight mb-6">По категориям</h2>

				<div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
					{#each categories as category, i}
						<button
							onclick={() => selectCategory(category.id)}
							class="flex flex-col items-center gap-2 p-4 rounded-lg transition-all {selectedCategory === category.id
								? 'bg-primary text-white shadow-md'
								: 'bg-surface text-muted border border-border hover:border-primary/30 hover:bg-primary/10'}"
						>
							<category.icon size={22} />
							<span class="text-xs font-medium text-center">{category.name}</span>
						</button>
					{/each}
				</div>
			</div>

			<!-- Results Count -->
			{#if searchQuery !== ''}
				<div class="mb-6">
					<p class="text-muted">
						Найдено <span class="font-semibold text-black">{filteredFaqs().length}</span>
						результат{filteredFaqs().length !== 1 ? 'ов' : ''} для "{searchQuery}"
					</p>
				</div>
			{/if}

			<!-- FAQs -->
			{#if filteredFaqs().length > 0}
				<div class="bg-white rounded-lg shadow-sm border border-border overflow-hidden">
					{#each filteredFaqs() as faq, index (faq.id)}
						<div class="border-b border-border last:border-b-0">
							<button onclick={() => toggleFaq(faq.id)} class="w-full px-6 lg:px-8 py-5 lg:py-6 text-left hover:bg-surface transition-colors flex items-center justify-between gap-4">
								<div class="flex-1">
									<h3 class="text-base lg:text-lg font-semibold text-black pr-4">{faq.question}</h3>
								</div>
								<div class="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
									{#if expandedFaqId === faq.id}
										<ChevronUp size={18} class="text-primary" />
									{:else}
										<ChevronDown size={18} class="text-muted" />
									{/if}
								</div>
							</button>

							{#if expandedFaqId === faq.id}
								<div class="px-6 lg:px-8 pb-6 text-muted leading-relaxed animate-fade-in">
									{faq.answer}
								</div>
							{/if}
						</div>
					{/each}
				</div>
			{:else}
				<div class="bg-white rounded-lg shadow-sm p-12 text-center border border-border">
					<div class="w-16 h-16 bg-surface rounded-full flex items-center justify-center mx-auto mb-4">
						<Search size={32} class="text-muted" />
					</div>
					<h2 class="text-2xl font-semibold text-black mb-2">Ничего не найдено</h2>
					<p class="text-muted mb-6">Мы не нашли частых вопросов по вашему запросу. Попробуйте другие ключевые слова или выберите категорию.</p>
					<button
						onclick={() => {
							searchQuery = '';
							selectedCategory = 'all';
						}}
						class="px-6 py-2.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-colors"
					>
						Сбросить поиск
					</button>
				</div>
			{/if}
		</div>
	</div>
</section>

<!-- Still Need Help -->
<section class="py-12 lg:py-20 bg-[#1D2226] text-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="max-w-4xl mx-auto text-center">
			<div class="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-6">
				<MessageCircle size={32} class="text-primary" />
			</div>
			<h2 class="text-2xl lg:text-3xl font-semibold tracking-tight mb-4">Нужна ещё помощь?</h2>
			<p class="text-lg text-gray-300 mb-8">Не нашли, что искали? Наша команда поддержки готова помочь.</p>
			<div class="flex flex-col sm:flex-row gap-4 justify-center mb-8">
				<a href="/contact/" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-black font-medium rounded-full hover:bg-gray-100 transition-colors shadow-sm">
					Связаться с поддержкой
					<ArrowRight size={18} />
				</a>
				<a
					href="mailto:support@peeljobs.com"
					class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/10 text-white font-medium rounded-full hover:bg-white/20 transition-colors border border-white/20"
				>
					Написать нам
				</a>
			</div>

			<div class="pt-8 border-t border-white/10">
				<p class="text-muted">
					<span class="font-medium text-gray-300">Время ответа:</span> Обычно мы отвечаем в течение 24 часов в рабочие дни
				</p>
			</div>
		</div>
	</div>
</section>
