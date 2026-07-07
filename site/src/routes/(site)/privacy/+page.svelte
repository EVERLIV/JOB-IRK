<script lang="ts">
	import { Shield, ChevronRight, Lock, Database, UserCheck, AlertTriangle, Eye, Cookie, Globe, Users, Bell, MessageCircle, ArrowRight } from '@lucide/svelte';

	const lastUpdated = '19 октября 2025';

	interface Section {
		id: string;
		title: string;
		icon: typeof Shield;
	}

	const sections: Section[] = [
		{ id: 'introduction', title: 'Введение', icon: Shield },
		{ id: 'cookies', title: 'Куки и отслеживание', icon: Cookie },
		{ id: 'third-party', title: 'Сторонние сервисы', icon: Globe },
		{ id: 'consent', title: 'Ваше согласие', icon: UserCheck },
		{ id: 'security', title: 'Информационная безопасность', icon: Lock },
		{ id: 'updating', title: 'Обновление информации', icon: Database },
		{ id: 'children', title: 'Дети', icon: Users },
		{ id: 'sharing', title: 'Передача информации', icon: Eye },
		{ id: 'confidentiality', title: 'Конфиденциальность', icon: Shield },
		{ id: 'changes', title: 'Изменения политики', icon: Bell },
		{ id: 'disclaimer', title: 'Отказ от ответственности', icon: AlertTriangle },
		{ id: 'contact', title: 'Контактная информация', icon: MessageCircle }
	];

	function scrollToSection(id: string): void {
		const element = document.getElementById(id);
		if (element) {
			element.scrollIntoView({ behavior: 'smooth', block: 'start' });
		}
	}
</script>

<svelte:head>
	<title>Политика конфиденциальности - PeelJobs | Как мы защищаем ваши данные</title>
	<meta
		name="description"
		content="Политика конфиденциальности PeelJobs объясняет, как мы собираем, используем и защищаем вашу личную информацию. Узнайте о нашей приверженности безопасности данных, куки, сторонних сервисах и ваших правах на конфиденциальность."
	/>
	<link rel="canonical" href="https://peeljobs.com/privacy/" />

	<!-- Open Graph -->
	<meta property="og:title" content="Политика конфиденциальности - PeelJobs" />
	<meta property="og:description" content="Узнайте, как PeelJobs защищает вашу конфиденциальность и личную информацию." />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://peeljobs.com/privacy/" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="Политика конфиденциальности - PeelJobs" />
	<meta name="twitter:description" content="Наша приверженность защите вашей конфиденциальности и данных." />
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
		<nav class="mb-8" aria-label="Навигация">
			<ol class="flex items-center gap-2 text-sm text-muted">
				<li>
					<a href="/" class="hover:text-white transition-colors">Главная</a>
				</li>
				<li class="flex items-center gap-2">
					<ChevronRight size={14} />
					<span class="text-white font-medium">Политика конфиденциальности</span>
				</li>
			</ol>
		</nav>

		<div class="max-w-4xl mx-auto text-center">
			<div class="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-8 animate-fade-in-up" style="opacity: 0;">
				<Shield size={40} class="text-primary" />
			</div>
			<h1 class="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 animate-fade-in-up" style="opacity: 0; animation-delay: 100ms;">
				Политика конфиденциальности
			</h1>
			<p class="text-lg md:text-xl text-gray-300 mb-4 animate-fade-in-up" style="opacity: 0; animation-delay: 200ms;">
				Ваша конфиденциальность важна для нас. Узнайте, как мы собираем, используем и защищаем вашу личную информацию.
			</p>
			<p class="text-sm text-muted animate-fade-in-up" style="opacity: 0; animation-delay: 300ms;">Обновлено: {lastUpdated}</p>
		</div>
	</div>
</section>

<!-- Quick Summary -->
<section class="py-12 lg:py-16 bg-surface">
	<div class="max-w-7xl mx-auto px-4 lg:px-8">
		<div class="max-w-4xl mx-auto">
			<div class="bg-primary/10 rounded-lg p-6 lg:p-8 border border-primary/20">
				<div class="flex items-start gap-4">
					<div class="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center flex-shrink-0">
						<Shield size={24} class="text-primary" />
					</div>
					<div>
						<h2 class="text-xl font-semibold text-black mb-3">Конфиденциальность вкратце</h2>
						<ul class="space-y-2 text-muted">
							<li class="flex items-center gap-2">
								<Lock size={16} class="text-primary flex-shrink-0" />
								Мы используем шифрование по отраслевым стандартам для защиты ваших данных
							</li>
							<li class="flex items-center gap-2">
								<Eye size={16} class="text-primary flex-shrink-0" />
								Мы не продаём вашу личную информацию третьим лицам
							</li>
							<li class="flex items-center gap-2">
								<UserCheck size={16} class="text-primary flex-shrink-0" />
								Вы контролируете, какая информация видна в вашем профиле
							</li>
							<li class="flex items-center gap-2">
								<Database size={16} class="text-primary flex-shrink-0" />
								Вы можете запросить удаление ваших данных в любое время
							</li>
						</ul>
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

			<!-- Privacy Policy Content -->
			<div class="lg:col-span-3">
				<div class="bg-white rounded-lg shadow-sm border border-border p-6 lg:p-10">
					<!-- Introduction -->
					<article id="introduction" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Shield size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">1. Введение</h2>
						</div>
						<div class="space-y-4 text-muted leading-relaxed">
							<p>
								В PeelJobs мы стремимся уважать вашу конфиденциальность в интернете и признаём вашу потребность
								в надлежащей защите и управлении любой лично идентифицирующей информацией
								(«Личная информация»), которой вы делитесь с нами.
							</p>
							<p>
								«Личная информация» означает любую информацию, которая может быть использована для идентификации
								лица, включая, помимо прочего, имя и фамилию, домашний или иной физический адрес
								и адрес электронной почты или иную контактную информацию, как на работе, так и дома. Как правило,
								вы можете посещать PeelJobs, не сообщая нам, кто вы, и не раскрывая никакой Личной
								информации о себе.
							</p>
						</div>
					</article>

					<!-- Cookies Section -->
					<article id="cookies" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Cookie size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">2. Куки и технологии отслеживания</h2>
						</div>
						<div class="bg-surface rounded-lg p-6 border border-border">
							<div class="space-y-4 text-muted leading-relaxed">
								<p>
									Некоторые из наших веб-страниц используют «куки» и другие технологии отслеживания. «Куки» — это
									небольшой текстовый файл, который может использоваться, например, для сбора
									информации о активности на сайте. Некоторые куки и другие технологии могут служить
									для сохранения Личной информации, ранее указанной пользователем.
								</p>
								<p>
									Большинство браузеров позволяют управлять куки, в том числе принимать их или нет
									и как их удалять. Вы можете настроить большинство браузеров на уведомление при
									получении куки или заблокировать куки в браузере, но обратите внимание,
									что если вы решите удалить или заблокировать куки, вам потребуется заново ввести
									исходный идентификатор пользователя и пароль для доступа к определённым частям сайта.
								</p>
								<p>
									Технологии отслеживания могут записывать такую информацию, как интернет-домены и имена
									хостов; интернет-протокол (IP) адреса; программное обеспечение браузера и тип
									операционной системы; паттерны кликов; даты и время доступа к нашему сайту. Наше
									использование куки и других технологий отслеживания позволяет нам улучшить наш сайт
									и ваш опыт взаимодействия с ним.
								</p>
							</div>
						</div>
					</article>

					<!-- Third Party Services -->
					<article id="third-party" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Globe size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">3. Сторонние сервисы</h2>
						</div>
						<div class="space-y-4 text-muted leading-relaxed">
							<p>
								Третьи лица предоставляют определённые сервисы, доступные на PeelJobs. Мы можем предоставлять
								информацию, включая Личную информацию, которую мы собираем, сторонним поставщикам
								услуг, чтобы помочь нам в реализации программ, продуктов, информации и сервисов. Поставщики
								услуг также являются важным средством поддержки нашего сайта и списков рассылки.
							</p>
							<p>
								Мы предпримем разумные шаги для обеспечения того, чтобы эти сторонние поставщики услуг
								были обязаны защищать Личную информацию от нашего имени. Мы не намерены передавать
								Личную информацию без вашего согласия третьим лицам, не связанным обязательствами
								действовать от нашего имени, если только такая передача не требуется по закону.
							</p>
						</div>
					</article>

					<!-- Your Consent -->
					<article id="consent" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<UserCheck size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">4. Ваше согласие</h2>
						</div>
						<div class="bg-primary/10 rounded-lg p-6 border border-primary/20">
							<p class="text-muted leading-relaxed">
								Используя этот сайт, вы соглашаетесь с условиями нашей Политики конфиденциальности и с нашей
								обработкой Личной информации в целях, указанных выше, а также в тех, которые
								разъясняются в местах сбора Личной информации на сайте.
							</p>
						</div>
					</article>

					<!-- Information Security -->
					<article id="security" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-success-light rounded-xl flex items-center justify-center">
								<Lock size={24} class="text-success" />
							</div>
							<h2 class="text-2xl font-semibold text-black">5. Информационная безопасность</h2>
						</div>
						<div class="bg-success-light rounded-lg p-6 border border-success/20">
							<ul class="space-y-4 text-muted">
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-success rounded-full mt-2 flex-shrink-0"></div>
									<span>Мы принимаем соответствующие меры безопасности для защиты от несанкционированного доступа или
									несанкционированного изменения, раскрытия или уничтожения данных.</span>
								</li>
								<li class="flex items-start gap-3">
									<div class="w-2 h-2 bg-success rounded-full mt-2 flex-shrink-0"></div>
									<span>Мы ограничиваем доступ к вашей лично идентифицирующей информации для сотрудников, которым
									необходимо знать эту информацию для работы, развития или улучшения наших сервисов.</span>
								</li>
							</ul>
						</div>
					</article>

					<!-- Updating Information -->
					<article id="updating" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Database size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">6. Обновление вашей информации</h2>
						</div>
						<p class="text-muted leading-relaxed">
							Мы предоставляем механизмы для обновления и исправления вашей лично идентифицирующей
							информации для многих наших сервисов. Для получения дополнительной информации, пожалуйста,
							обратитесь к справочной документации для каждого сервиса.
						</p>
					</article>

					<!-- Children -->
					<article id="children" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Users size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">7. Дети</h2>
						</div>
						<p class="text-muted leading-relaxed">
							PeelJobs не будет связываться с детьми до 13 лет по поводу специальных предложений или
							в маркетинговых целях без разрешения родителя.
						</p>
					</article>

					<!-- Information Sharing -->
					<article id="sharing" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Eye size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">8. Передача и раскрытие информации</h2>
						</div>
						<div class="bg-surface rounded-lg p-6 border border-border mb-6">
							<p class="font-semibold text-black mb-4">
								PeelJobs не сдаёт в аренду, не продаёт и не передаёт личную информацию о вас другим
								людям (за исключением случаев с вашего согласия) или неаффилированным компаниям, кроме как для предоставления
								продуктов или услуг, которые вы запрашивали, когда у нас есть ваше разрешение, или при следующих
								обстоятельствах:
							</p>
							<ol class="space-y-3 text-muted list-decimal list-inside">
								<li>
									Мы предоставляем информацию доверенным партнёрам, которые работают от имени или совместно с
									PeelJobs в рамках соглашений о конфиденциальности.
								</li>
								<li>
									Мы отвечаем на повестки, судебные приказы или правовые процедуры, а также для установления или
									осуществления наших законных прав или защиты от юридических претензий.
								</li>
								<li>
									Мы считаем необходимым поделиться информацией для расследования, предотвращения или
									принятия мер в отношении незаконной деятельности, предполагаемого мошенничества или нарушений наших условий
									использования.
								</li>
								<li>
									Мы передаём информацию о вас, если PeelJobs приобретается или сливается с другой
									компанией.
								</li>
							</ol>
						</div>
						<ul class="space-y-3 text-muted">
							<li class="flex items-start gap-3">
								<div class="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
								<span>PeelJobs не предоставляет никакой личной информации рекламодателям, когда вы взаимодействуете
								с целевой рекламой или просматриваете её.</span>
							</li>
							<li class="flex items-start gap-3">
								<div class="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
								<span>Наши рекламодатели включают поставщиков финансовых услуг и нефинансовые компании.</span>
							</li>
						</ul>
					</article>

					<!-- Confidentiality -->
					<article id="confidentiality" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<Shield size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">9. Конфиденциальность и безопасность</h2>
						</div>
						<ul class="space-y-3 text-muted leading-relaxed">
							<li class="flex items-start gap-3">
								<div class="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
								<span>Мы ограничиваем доступ к личной информации о вас для сотрудников, которые, по нашему разумному
								убеждению, должны иметь контакт с этой информацией.</span>
							</li>
							<li class="flex items-start gap-3">
								<div class="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
								<span>Мы имеем физические, электронные и процедурные меры защиты, соответствующие индийским законам,
								для защиты личной информации о вас.</span>
							</li>
						</ul>
					</article>

					<!-- Policy Changes -->
					<article id="changes" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-warning-light rounded-xl flex items-center justify-center">
								<Bell size={24} class="text-warning" />
							</div>
							<h2 class="text-2xl font-semibold text-black">10. Изменения в данной Политике конфиденциальности</h2>
						</div>
						<div class="bg-warning-light rounded-lg p-6 border border-warning/20">
							<p class="text-muted leading-relaxed">
								PeelJobs оставляет за собой право обновлять, изменять или модифицировать данную политику в любое время.
								Политика вступает в силу с даты такого обновления, изменения или модификации.
							</p>
						</div>
					</article>

					<!-- Disclaimer -->
					<article id="disclaimer" class="mb-12 scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-error-light rounded-xl flex items-center justify-center">
								<AlertTriangle size={24} class="text-error" />
							</div>
							<h2 class="text-2xl font-semibold text-black">11. Отказ от ответственности</h2>
						</div>
						<div class="bg-error-light rounded-lg p-6 border border-error/20">
							<div class="space-y-4 text-muted leading-relaxed">
								<p>
									PeelJobs не хранит данные кредитных карт в месте, доступном через
									Интернет. После завершения транзакции по кредитной карте все данные
									кредитной карты перемещаются в офлайн для обеспечения максимальной безопасности.
								</p>
								<p class="font-semibold text-black">
									PeelJobs не несёт ответственности за любые убытки или ущерб, причинённые в результате
									раскрытия любой информации о счёте пользователя и/или информации,
									относящейся к онлайн-транзакциям с использованием кредитных/дебетовых карт.
								</p>
							</div>
						</div>
					</article>

					<!-- Contact Information -->
					<article id="contact" class="scroll-mt-6">
						<div class="flex items-center gap-4 mb-6">
							<div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
								<MessageCircle size={24} class="text-primary" />
							</div>
							<h2 class="text-2xl font-semibold text-black">12. Контактная информация</h2>
						</div>
						<div class="bg-surface rounded-lg p-6 border border-border">
							<p class="text-muted leading-relaxed mb-4">
								PeelJobs приветствует ваши комментарии относительно данного заявления о конфиденциальности. Если у вас
								возникнут опасения по поводу нарушения данной Политики конфиденциальности, мы приложим все коммерчески
								разумные усилия для их устранения.
							</p>
							<a
								href="/contact/"
								class="inline-flex items-center gap-2 text-primary hover:text-primary-hover font-medium"
							>
								Связаться с нами
								<ArrowRight size={16} />
							</a>
							<p class="text-sm text-muted mt-4">
								<strong>Примечание:</strong> Условия данного соглашения могут быть изменены PeelJobs в любое время.
								PeelJobs вправе предлагать свои услуги любому клиенту/потенциальному клиенту без ограничений.
							</p>
						</div>
					</article>

					<!-- Acknowledgment -->
					<div class="bg-primary/10 rounded-lg p-6 mt-10 border border-primary/20">
						<h3 class="font-semibold text-primary mb-2">Ваше согласие</h3>
						<p class="text-primary/80">
							Используя PeelJobs, вы подтверждаете, что прочитали и поняли данную Политику конфиденциальности
							и соглашаетесь на сбор, использование и раскрытие вашей информации, как описано
							здесь.
						</p>
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
			<h2 class="text-2xl font-semibold tracking-tight mb-4">Есть вопросы о вашей конфиденциальности?</h2>
			<p class="text-gray-300 mb-8">
				Мы здесь, чтобы помочь. Обратитесь к нашей команде с любыми вопросами или опасениями, связанными с конфиденциальностью.
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
