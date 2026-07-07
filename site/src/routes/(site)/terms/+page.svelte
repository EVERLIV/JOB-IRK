<script lang="ts">
	import { FileText, ChevronRight, AlertCircle, Building2, Users, Shield, Key, UserCircle, Ban, Scale, RefreshCw, ArrowRight, MessageCircle } from '@lucide/svelte';

	const lastUpdated = 'October 19, 2025';

	interface Section {
		id: string;
		title: string;
		icon: typeof FileText;
	}

	const sections: Section[] = [
		{ id: 'introduction', title: 'Введение', icon: FileText },
		{ id: 'employer-eligibility', title: 'Право работодателя', icon: Building2 },
		{ id: 'subscription-terms', title: 'Условия подписки', icon: Scale },
		{ id: 'employer-conduct', title: 'Поведение работодателя', icon: Building2 },
		{ id: 'prohibited-employer', title: 'Запрещённое поведение работодателя', icon: Ban },
		{ id: 'user-conduct', title: 'Поведение пользователя', icon: Users },
		{ id: 'registration', title: 'Регистрация и пароль', icon: Key },
		{ id: 'profile', title: 'Управление профилем', icon: UserCircle },
		{ id: 'prohibited-users', title: 'Запрещённое поведение пользователя', icon: Ban },
		{ id: 'rights', title: 'Ограничение прав', icon: Shield },
		{ id: 'revisions', title: 'Изменения', icon: RefreshCw }
	];

	function scrollToSection(id: string): void {
		const element = document.getElementById(id);
		if (element) {
			element.scrollIntoView({ behavior: 'smooth', block: 'start' });
		}
	}
</script>

<svelte:head>
	<title>Условия использования - PeelJobs | Пользовательское соглашение и правила использования</title>
	<meta
		name="description"
		content="Ознакомьтесь с Условиями использования PeelJobs, пользовательским соглашением и правилами использования. Понимайте свои права и обязанности при использовании нашей бесплатной платформы для поиска работы для соискателей и работодателей."
	/>
	<link rel="canonical" href="https://peeljobs.com/terms/" />

	<!-- Open Graph -->
	<meta property="og:title" content="Условия использования - PeelJobs" />
	<meta property="og:description" content="Пользовательское соглашение и условия использования платформы PeelJobs." />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://peeljobs.com/terms/" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="Условия использования - PeelJobs" />
	<meta name="twitter:description" content="Наши условия использования и пользовательское соглашение." />
</svelte:head>

<!-- Hero Section -->
<section class="bg-[#1D2226] text-white py-16 lg:py-20 relative overflow-hidden">
	<!-- Decorative Elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
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
					<span class="text-white font-medium">Условия использования</span>
				</li>
			</ol>
		</nav>

		<div class="max-w-4xl mx-auto text-center">
			<div class="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-8 animate-fade-in-up" style="opacity: 0;">
				<FileText size={40} class="text-primary" />
			</div>
			<h1 class="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms;">
				Условия использования
			</h1>
			<p class="text-lg md:text-xl text-gray-300 mb-4 animate-fade-in-up" style="opacity: 0; animation-delay: 200ms;">
				Пользовательское соглашение и правила использования
			</p>
			<p class="text-sm text-muted animate-fade-in-up" style="opacity: 0; animation-delay: 300ms;">Обновлено: {lastUpdated}</p>
		</div>
	</div>
</section>

<!-- Important Notice -->
<section class="py-12 lg:py-16 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="max-w-4xl mx-auto">
			<div class="bg-warning-light rounded-lg p-6 lg:p-8 border border-warning/20">
				<div class="flex items-start gap-4">
					<div class="w-12 h-12 bg-warning-light rounded-xl flex items-center justify-center flex-shrink-0">
						<AlertCircle size={24} class="text-warning" />
					</div>
					<div>
						<h2 class="text-xl font-semibold text-black mb-3">Важное уведомление</h2>
						<div class="space-y-4 text-muted leading-relaxed">
							<p>
								Данное Соглашение об использовании и подписке является юридически обязывающим соглашением между
								Peeljobs.com, Работодателем (включая работодателей, кадровые агентства, агентства по подбору персонала и
								рекрутерами) и Кандидатом/Пользователем данного сайта, включая всю информацию,
								продукты, услуги, программное обеспечение, базы данных и сайт, доступные на Peeljobs.com.
							</p>
							<p>
								Получая доступ к информации на Peeljobs.com, Пользователь подтверждает, что он/она прочитал,
								понял и соглашается соблюдать условия данного Соглашения. Используя
								Peeljobs.com в качестве Кандидата, Работодателя и/или отправляя какой-либо контент, Пользователь
								соглашается соблюдать и выполнять данное Соглашение. Вы понимаете и соглашаетесь с тем, что
								Peeljobs.com предоставляется вам на условиях <span class="font-semibold">«КАК ЕСТЬ»</span> и
								<span class="font-semibold">«КАК ДОСТУПНО»</span>. Peeljobs.com оставляет за собой
								право изменять, приостанавливать или прекращать работу Системы с уведомлением или без него в любое время
								без какой-либо ответственности перед вами.
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- Main Content -->
<section class="py-12 lg:py-20 bg-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="grid lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
			<!-- Sticky Sidebar -->
			<div class="lg:col-span-1 hidden lg:block">
				<div class="bg-surface rounded-lg p-6 border border-border sticky top-6">
					<h2 class="text-lg font-semibold text-black mb-5">Содержание</h2>
					<nav class="space-y-1">
						{#each sections as section}
							<button
								onclick={() => scrollToSection(section.id)}
								class="w-full text-left text-sm text-muted hover:text-primary hover:bg-primary/10 px-3 py-2.5 rounded-xl transition-colors flex items-center gap-3"
							>
								<svelte:component this={section.icon} size={14} class="text-muted" />
								<span>{section.title}</span>
							</button>
						{/each}
					</nav>
				</div>
			</div>

			<!-- Terms Content -->
			<div class="lg:col-span-3">
				<div class="bg-white rounded-lg shadow-sm border border-border p-6 lg:p-10">

					<!-- EMPLOYER TERMS HEADER -->
					<div class="bg-primary/10 rounded-lg p-6 border border-primary/20 mb-10">
						<div class="flex items-center gap-3">
							<div class="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-sm">
								<Building2 size={20} class="text-white" />
							</div>
							<h2 class="text-xl lg:text-2xl font-semibold text-black">Условия для работодателей</h2>
						</div>
					</div>

					<!-- Employer Eligibility -->
					<article id="employer-eligibility" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Building2 size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Допустимые подписчики PeelJobs</h2>
						</div>
						<p class="text-muted leading-relaxed">
							PeelJobs оставляет за собой право по своему усмотрению определять, соответствует ли фирма
							требованиям для подписки. PeelJobs запрашивает информацию о социальных страницах компании
							для отображения вашей вакансии на ваших социальных страницах, что, по нашему мнению,
							замечательно, так как это максимизирует охват вашей публикации вакансий.
						</p>
					</article>

					<!-- Subscription Terms -->
					<article id="subscription-terms" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Scale size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Условия подписки</h2>
						</div>
						<p class="text-muted leading-relaxed">
							Все предложения подписки предоставляются правомочным, квалифицированным Работодателям. По мере приближения
							даты окончания срока подписки Работодателя, Работодателю может быть выставлен счёт на
							новый срок подписки. Если счёт оплачивается, подписка и связанные с ней
							преимущества продолжатся; в противном случае подписка станет неактивной по истечении
							её срока действия. Когда подписка становится неактивной, все функции, услуги и
							преимущества подписки прекращаются. Они могут включать, помимо прочего: вакансии,
							внесённые в Систему, распространение вакансий, веб-страницы, поддерживаемые Системой,
							услуги пересылки резюме.
						</p>
					</article>

					<!-- Employer Conduct -->
					<article id="employer-conduct" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Building2 size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Поведение работодателя</h2>
						</div>
						<div class="space-y-4 text-muted leading-relaxed">
							<p>
								Работодатель соглашается с тем, что вся информация, к которой Работодатель получает доступ, будет использоваться только
								для того, чтобы позволить Работодателю использовать услуги, предлагаемые PeelJobs. Работодатели, стремящиеся
								заполнить открытые, проверяемые должности от имени своих клиентских или поставщик компаний, могут
								использовать Систему только в законных целях.
							</p>
							<p>
								Работодатели должны загружать в Систему только подлинные, проверяемые объявления
								о вакансиях от компании Работодателя или от проверяемых компаний, с которыми
								у Работодателя есть прямые, явные агентские отношения. Каждый Работодатель несёт
								ответственность за точность, актуальность и полноту любых объявлений
								о вакансиях или профилей кандидатов, которые его пользователи размещают в Системе.
							</p>
							<p>
								Работодатель заявляет, гарантирует и обязуется, что любая информация или материалы,
								загруженные в Систему Работодателем для использования в связи с Системой, не будут
								нарушать какие-либо законы или правила или права третьих лиц на интеллектуальную собственность, включая,
								без ограничений, авторское право, товарные знаки, непристойность, права на известность
								или неприкосновенность частной жизни и законы о клевете. Работодатель настоящим предоставляет PeelJobs
								неисключительную, всемирную, безвозмездную лицензию на использование этих материалов и создание
								гиперссылок на сайт Работодателя.
							</p>
						</div>
					</article>

					<!-- Prohibited Employer Conduct -->
					<article id="prohibited-employer" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-error-light rounded-xl flex items-center justify-center">
								<Ban size={24} class="text-error" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Запрещённое поведение работодателей</h2>
						</div>
						<p class="text-muted mb-6">Запрещённое использование Системы включает:</p>

						<div class="space-y-4">
							<div class="bg-surface rounded-lg p-5 border border-border">
								<h4 class="font-semibold text-black mb-2 flex items-center gap-2">
									<Key size={16} class="text-error" />
									Передача пароля
								</h4>
								<p class="text-sm text-muted leading-relaxed">
									Использование Системы ограничено зарегистрированными и авторизованными владельцами учётных записей.
									Работодатели могут изменить профиль и сменить авторизованное лицо в любое время в течение
									действительного периода подписки. Передача паролей или логин-информации запрещена.
									Нарушение данного запрета приведёт к немедленной отмене,
									без возврата средств, любой оставшейся части суммы подписки.
								</p>
							</div>

							<div class="bg-surface rounded-lg p-5 border border-border">
								<h4 class="font-semibold text-black mb-2 flex items-center gap-2">
									<Scale size={16} class="text-error" />
									Коммерческое использование системы
								</h4>
								<p class="text-sm text-muted leading-relaxed">
									Перепродажа любой части Системы или услуг или преимуществ, предоставляемых
									Системой, строго запрещена. Все использование Системы должно быть заключено
									напрямую через PeelJobs или одного из наших авторизованных партнёров. Перепродажа Системы
									PeelJobs или любого из её компонентов без предварительного письменного разрешения от PeelJobs
									приведёт к немедленной отмене без возврата средств любой оставшейся части суммы подписки.
								</p>
							</div>

							<div class="bg-surface rounded-lg p-5 border border-border">
								<h4 class="font-semibold text-black mb-2 flex items-center gap-2">
									<Shield size={16} class="text-error" />
									Автоматический поиск и роботы
								</h4>
								<p class="text-sm text-muted leading-relaxed">
									Работодатель не должен использовать или пытаться использовать какой-либо движок, программное обеспечение, инструмент, агент
									или иное устройство или механизм (включая браузеры, пауки, роботы, аватары или
									интеллектуальные агенты) для навигации или поиска в Системе.
								</p>
							</div>

							<div class="bg-surface rounded-lg p-5 border border-border">
								<h4 class="font-semibold text-black mb-2 flex items-center gap-2">
									<Ban size={16} class="text-error" />
									Множественные или дублирующиеся публикации
								</h4>
								<p class="text-sm text-muted leading-relaxed">
									Работодатель не должен публиковать дублирующиеся должности, несколько должностей в одном
									объявлении или копировать (плагиатить) другие объявления о вакансиях или профили
									кандидатов.
								</p>
							</div>
						</div>
					</article>

					<!-- ALL USERS TERMS HEADER -->
					<div class="bg-success-light rounded-lg p-6 border border-success/20 mb-10 mt-16">
						<div class="flex items-center gap-3">
							<div class="w-10 h-10 bg-success rounded-xl flex items-center justify-center shadow-sm">
								<Users size={20} class="text-white" />
							</div>
							<h2 class="text-xl lg:text-2xl font-semibold text-black">Условия для всех пользователей</h2>
						</div>
					</div>

					<!-- User Conduct -->
					<article id="user-conduct" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Users size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Поведение пользователя</h2>
						</div>
						<p class="text-muted leading-relaxed">
							Вам должно быть не менее 18 лет, чтобы посещать или использовать PeelJobs каким-либо образом. Посещая
							PeelJobs или принимая данные Условия использования, Вы заявляете и гарантируете
							Компании, что Вам не менее 18 лет, и что Вы имеете право, полномочия
							и дееспособность использовать Веб-сайт и соглашаться соблюдать данные Условия использования. Вы также
							заявляете и гарантируете Компании, что будете использовать PeelJobs способом,
							соответствующим всем применимым законам и правилам.
						</p>
					</article>

					<!-- Registration and Password -->
					<article id="registration" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Key size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Регистрация и пароль</h2>
						</div>
						<p class="text-muted leading-relaxed">
							Вы несёте ответственность за сохранение конфиденциальности информации о доступе к вашей учётной записи
							и паролей. Вы несёте ответственность за любое использование ваших регистраций
							на Веб-сайте и паролей, авторизованы ли они Вами или нет. Вы не имеете права
							передавать свой пароль или иную информацию о доступе к учётной записи какой-либо другой стороне, временно
							или постоянно, и нарушение данного обязательства может привести к отключению
							учётной записи PeelJobs и сервисов PeelJobs. Вы соглашаетесь немедленно уведомить Компанию
							о любом несанкционированном использовании вашей Учётной записи и паролей. При регистрации на PeelJobs
							вы будете получать рассылки о вакансиях и другие рекламные письма на ваш почтовый ящик.
						</p>
					</article>

					<!-- Profile -->
					<article id="profile" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<UserCircle size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Управление профилем</h2>
						</div>
						<div class="space-y-4 text-muted leading-relaxed">
							<p>
								Любой Профиль/Резюме, которое Вы отправляете, должен быть точным и описывать Вас, как конкретное лицо.
								Профиль требует заполнения стандартных полей.
							</p>
							<p>
								Вы подтверждаете и соглашаетесь с тем, что Вы несёте единоличную ответственность за форму, содержание и
								точность любого резюме или материала, содержащегося в нём, размещённого Вами на PeelJobs.
							</p>
							<p>
								PeelJobs оставляет за собой право предлагать Вам сторонние услуги и продукты
								на основе предпочтений, которые Вы указываете при регистрации, и в любое время
								после неё, или на которые Вы согласились получать; такие предложения могут быть сделаны PeelJobs
								или третьими лицами.
							</p>
							<p>
								Вы понимаете и подтверждаете, что не имеете никаких прав собственности на Вашу учётную запись и
								что если Вы отмените/прекратите свою учётную запись PeelJobs, вся Ваша информация
								из PeelJobs, включая резюме, Профили, сопроводительные письма, сохранённые вакансии, анкеты,
								будет отмечена как удалённая и может быть удалена из наших баз данных. Информация может
								продолжать быть доступной в течение некоторого времени из-за задержек в распространении
								такого удаления через веб-серверы PeelJobs. Кроме того, третьи лица могут сохранять
								копии Вашей Информации.
							</p>
							<p>
								PeelJobs оставляет за собой право удалить Вашу учётную запись и всю Вашу Информацию
								после значительного периода неактивности.
							</p>
						</div>
					</article>

					<!-- Prohibited User Conduct -->
					<article id="prohibited-users" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-error-light rounded-xl flex items-center justify-center">
								<Ban size={24} class="text-error" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Запрещённое поведение пользователей</h2>
						</div>
						<p class="text-muted mb-4">Запрещённое использование Системы включает:</p>
						<div class="bg-error-light rounded-lg p-6 border border-error/20">
							<ul class="space-y-3 text-muted">
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-error rounded-full mt-2 flex-shrink-0"></div>
									<span>Размещать чьё-либо резюме или подавать заявку на вакансию от имени другого лица</span>
								</li>
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-error rounded-full mt-2 flex-shrink-0"></div>
									<span>Устанавливать более одной копии одного и того же резюме в публичный доступ одновременно</span>
								</li>
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-error rounded-full mt-2 flex-shrink-0"></div>
									<span>Публиковать или отправлять на PeelJobs неполную, ложную или неточную биографическую
									информацию или информацию, не являющуюся вашей</span>
								</li>
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-error rounded-full mt-2 flex-shrink-0"></div>
									<span>Удалять или изменять любой материал, опубликованный другим лицом или организацией</span>
								</li>
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-error rounded-full mt-2 flex-shrink-0"></div>
									<span>Предпринимать действия, создающие неразумную или непропорционально большую нагрузку на
									инфраструктуру PeelJobs</span>
								</li>
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-error rounded-full mt-2 flex-shrink-0"></div>
									<span>Использовать сервисы PeelJobs для незаконных целей или любой незаконной деятельности, или публиковать
									или отправлять любой контент, резюме, которые являются клеветническими, диффамационными, неявно или явно
									оскорбительными, вульгарными, непристойными, угрожающими, оскорбительными, разжигающими ненависть, расистскими,
									дискриминационными, имеющими угрожающий характер или способными вызвать раздражение, неудобство, смущение,
									тревогу или способные причинить преследование любому лицу, а также включать ссылки на порнографический,
									непристойный или сексуально откровенный материал любого рода</span>
								</li>
							</ul>
						</div>
					</article>

					<!-- Reservation of Rights -->
					<article id="rights" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Shield size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Ограничение прав</h2>
						</div>
						<p class="text-muted leading-relaxed">
							Все права, прямо не предоставленные здесь, защищены.
						</p>
					</article>

					<!-- Revisions -->
					<article id="revisions" class="mb-10 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<RefreshCw size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">Изменения</h2>
						</div>
						<p class="text-muted leading-relaxed">
							PeelJobs может изменять данные Условия в любое время, публикуя обновлённую версию на
							https://www.peeljobs.com. Вам следует периодически посещать эту страницу, чтобы ознакомиться с
							действующим Соглашением, так как оно является обязательным для Пользователей.
						</p>
					</article>

					<!-- Contact CTA -->
					<div class="bg-primary/10 rounded-lg p-6 border border-primary/20">
						<div class="flex items-start gap-4">
							<div class="w-12 h-12 bg-primary rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm">
								<MessageCircle size={24} class="text-white" />
							</div>
							<div>
								<h3 class="text-lg font-semibold text-black mb-2">Вопросы?</h3>
								<p class="text-muted mb-4">
									По любым вопросам или юридическим опасениям, пожалуйста, напишите в службу поддержки PeelJobs.
								</p>
								<a
									href="/contact/"
									class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-full transition-colors shadow-sm"
								>
									Связаться с поддержкой
									<ArrowRight size={16} />
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- CTA Section -->
<section class="py-12 lg:py-16 bg-[#1D2226] text-white">
	<div class="max-w-7xl mx-auto px-4 lg:px-8 text-center">
		<div class="max-w-2xl mx-auto">
			<h2 class="text-2xl font-semibold tracking-tight mb-4">Есть вопросы об условиях?</h2>
			<p class="text-gray-300 mb-8">
				Мы здесь, чтобы помочь. Обратитесь к нашей команде с любыми вопросами или уточнениями об условиях использования.
			</p>
			<a
				href="/contact/"
				class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-black font-medium rounded-full hover:bg-gray-100 transition-colors shadow-sm"
			>
				Связаться с поддержкой
				<ArrowRight size={18} />
			</a>
		</div>
	</div>
</section>
