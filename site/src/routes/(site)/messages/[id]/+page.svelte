<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import {
		ArrowLeft,
		Send,
		Paperclip,
		Phone,
		Video,
		Info,
		Check,
		CheckCheck,
		Smile,
		Image as ImageIcon,
		File,
		X,
		Building2,
		Mail,
		ExternalLink
	} from '@lucide/svelte';

	type Sender = 'me' | 'recruiter';

	interface Message {
		id: number;
		sender: Sender;
		text: string;
		timestamp: string;
		read: boolean;
	}

	interface RecruiterDetails {
		name: string;
		company: string;
		position: string;
		avatar: string | null;
		online: boolean;
		email: string;
		phone: string;
	}

	interface Conversation {
		id: number;
		recruiter: RecruiterDetails;
		jobTitle: string;
		jobId: number;
		messages: Message[];
	}

	type AttachmentType = 'image' | 'file';
	type CallType = 'voice' | 'video';

	const allConversations: Conversation[] = [
		{
			id: 1,
			recruiter: {
				name: 'Sarah Johnson',
				company: 'Innovate Inc.',
				position: 'Старший рекрутер',
				avatar: null,
				online: true,
				email: 'sarah.johnson@innovate.com',
				phone: '+1 (555) 123-4567'
			},
			jobTitle: 'Senior Software Engineer',
			jobId: 101,
			messages: [
				{
					id: 101,
					sender: 'recruiter',
					text: 'Здравствуйте! Я рассмотрела ваш отклик на позицию Senior Software Engineer. Ваш опыт работы с React и Node.js впечатляет!',
					timestamp: '2024-01-18T13:00:00',
					read: true
				},
				{
					id: 102,
					sender: 'me',
					text: 'Спасибо, что написали! Мне очень интересна эта возможность. Я работаю с React уже 4 года и хотел бы узнать больше о роли.',
					timestamp: '2024-01-18T13:15:00',
					read: true
				},
				{
					id: 103,
					sender: 'recruiter',
					text: 'Отлично! Роль предполагает руководство командой из 5 разработчиков и работу над новой клиентской платформой. Стек: React, Node.js, PostgreSQL и AWS.',
					timestamp: '2024-01-18T13:20:00',
					read: true
				},
				{
					id: 104,
					sender: 'me',
					text: 'Звучит отлично! У меня есть опыт работы со всеми этими технологиями. Какие будут следующие шаги?',
					timestamp: '2024-01-18T13:25:00',
					read: true
				},
				{
					id: 105,
					sender: 'recruiter',
					text: 'Отлично! Когда вам будет удобно созвониться, чтобы обсудить позицию подробнее?',
					timestamp: '2024-01-18T14:30:00',
					read: false
				}
			]
		},
		{
			id: 2,
			recruiter: {
				name: 'Michael Chen',
				company: 'Tech Corp',
				position: 'Менеджер по подбору персонала',
				avatar: null,
				online: false,
				email: 'michael.chen@techcorp.com',
				phone: '+1 (555) 234-5678'
			},
			jobTitle: 'Full Stack Developer',
			jobId: 102,
			messages: [
				{
					id: 201,
					sender: 'recruiter',
					text: 'Здравствуйте! Ваш профиль привлёк наше внимание. У нас есть вакансия Full Stack Developer, которая соответствует вашим навыкам.',
					timestamp: '2024-01-18T09:00:00',
					read: true
				},
				{
					id: 202,
					sender: 'recruiter',
					text: 'Мы хотели бы назначить с вами собеседование. Вы свободны на следующей неделе?',
					timestamp: '2024-01-18T10:15:00',
					read: false
				}
			]
		},
		{
			id: 3,
			recruiter: {
				name: 'Emily Rodriguez',
				company: 'StartupXYZ',
				position: 'HR-менеджер',
				avatar: null,
				online: true,
				email: 'emily@startupxyz.com',
				phone: '+1 (555) 345-6789'
			},
			jobTitle: 'React Developer',
			jobId: 103,
			messages: [
				{
					id: 301,
					sender: 'recruiter',
					text: 'Здравствуйте! Вы свободны во вторник на собеседование?',
					timestamp: '2024-01-17T15:00:00',
					read: true
				},
				{
					id: 302,
					sender: 'me',
					text: 'Да, вторник мне подходит! В какое время будет удобнее?',
					timestamp: '2024-01-17T15:30:00',
					read: true
				},
				{
					id: 303,
					sender: 'recruiter',
					text: 'Отлично! Отправлю приглашение на встречу на 14:00. Буду рада пообщаться с вами!',
					timestamp: '2024-01-17T16:45:00',
					read: true
				}
			]
		}
	];

	let conversationId = $state<number | null>(null);
	let conversation = $state<Conversation | null>(null);

	$effect(() => {
		const idParam = $page.params.id;
		if (!idParam) {
			conversationId = null;
			conversation = null;
			return;
		}
		const parsed = Number.parseInt(idParam, 10);
		if (Number.isNaN(parsed)) {
			conversationId = null;
			conversation = null;
			return;
		}
		conversationId = parsed;
		conversation = allConversations.find((c) => c.id === parsed) ?? null;
	});

	let messageText = $state('');
	let messages = $state<Message[]>([]);
	let showRecruiterInfo = $state(false);
	let showAttachmentMenu = $state(false);

	$effect(() => {
		if (!conversation && typeof window !== 'undefined') {
			goto('/messages/');
		}
	});

	$effect(() => {
		messages = conversation ? [...conversation.messages] : [];
	});

	function goBack(): void {
		goto('/messages/');
	}

	function sendMessage(): void {
		if (!messageText.trim() || !conversation) return;

		const newMessage: Message = {
			id: Date.now(),
			sender: 'me',
			text: messageText.trim(),
			timestamp: new Date().toISOString(),
			read: false
		};

		messages = [...messages, newMessage];
		messageText = '';

		setTimeout(() => {
			const messagesContainer = document.getElementById('messages-container');
			if (messagesContainer) {
				messagesContainer.scrollTop = messagesContainer.scrollHeight;
			}
		}, 100);
	}

	function handleKeyPress(event: KeyboardEvent): void {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	function formatMessageTime(timestamp: string): string {
		const date = new Date(timestamp);
		return date.toLocaleTimeString('ru-RU', { hour: 'numeric', minute: '2-digit', hour12: false });
	}

	function formatMessageDate(timestamp: string): string {
		const date = new Date(timestamp);
		const now = new Date();
		const diffMs = now.getTime() - date.getTime();
		const diffDays = Math.floor(diffMs / 86400000);

		if (diffDays === 0) return 'Сегодня';
		if (diffDays === 1) return 'Вчера';
		if (diffDays < 7) return date.toLocaleDateString('ru-RU', { weekday: 'long' });

		return date.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	function attachFile(type: AttachmentType): void {
		alert(`Функция прикрепления ${type === 'image' ? 'изображения' : 'файла'} будет реализована позже`);
		showAttachmentMenu = false;
	}

	function makeCall(type: CallType): void {
		alert(`Функция ${type === 'voice' ? 'аудио' : 'видео'}звонка будет реализована позже`);
	}

	function getInitials(name: string): string {
		return name
			.split(' ')
			.filter(Boolean)
			.map((part) => part[0]?.toUpperCase() ?? '')
			.join('');
	}

	type MessageGroups = Record<string, Message[]>;

	let groupedMessages = $state<MessageGroups>({});

	$effect(() => {
		groupedMessages = messages.reduce<MessageGroups>((groups, message) => {
			const dateKey = formatMessageDate(message.timestamp);
			if (!groups[dateKey]) {
				groups[dateKey] = [];
			}
			groups[dateKey].push(message);
			return groups;
		}, {});
	});
</script>

<svelte:head>
	<title>{conversation?.recruiter.name || 'Разговор'} - Сообщения - PeelJobs</title>
	<meta name="description" content="Чат с {conversation?.recruiter.name || 'рекрутером'}" />
</svelte:head>

{#if conversation}
	<div class="flex flex-col h-screen bg-surface-50">
		<!-- Header -->
		<header class="bg-white border-b border-gray-200 sticky top-0 z-10 elevation-1">
			<div class="max-w-5xl mx-auto px-4 lg:px-6">
				<div class="flex items-center justify-between py-4">
					<!-- Left: Back button and recruiter info -->
					<div class="flex items-center gap-3 flex-1 min-w-0">
						<button
							onclick={goBack}
							class="p-2 hover:bg-gray-100 rounded-xl transition-colors flex-shrink-0"
							title="Назад к сообщениям"
						>
							<ArrowLeft size={22} class="text-gray-600" />
						</button>

						<div class="relative flex-shrink-0">
							<div
								class="w-11 h-11 bg-primary-600 rounded-xl flex items-center justify-center text-white font-semibold"
							>
								{getInitials(conversation.recruiter.name)}
							</div>
							{#if conversation.recruiter.online}
								<div
									class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-success-500 border-2 border-white rounded-full"
								></div>
							{/if}
						</div>

						<div class="flex-1 min-w-0">
							<h1 class="font-semibold text-gray-900 truncate">{conversation.recruiter.name}</h1>
							<p class="text-sm text-gray-500 truncate">
								{conversation.recruiter.position} в {conversation.recruiter.company}
								{#if conversation.recruiter.online}
									<span class="text-success-600">• В сети</span>
								{:else}
									<span class="text-gray-400">• Не в сети</span>
								{/if}
							</p>
						</div>
					</div>

					<!-- Right: Action buttons -->
					<div class="flex items-center gap-1">
						<button
							onclick={() => makeCall('voice')}
							class="p-2.5 hover:bg-gray-100 rounded-xl transition-colors"
							title="Аудиозвонок"
						>
							<Phone size={18} class="text-gray-600" />
						</button>
						<button
							onclick={() => makeCall('video')}
							class="p-2.5 hover:bg-gray-100 rounded-xl transition-colors"
							title="Видеозвонок"
						>
							<Video size={18} class="text-gray-600" />
						</button>
						<button
							onclick={() => (showRecruiterInfo = !showRecruiterInfo)}
							class="p-2.5 hover:bg-gray-100 rounded-xl transition-colors {showRecruiterInfo
								? 'bg-primary-50 text-primary-600'
								: ''}"
							title="Информация о разговоре"
						>
							<Info size={18} class={showRecruiterInfo ? 'text-primary-600' : 'text-gray-600'} />
						</button>
					</div>
				</div>

				<!-- Job Context Banner -->
				<div class="pb-4">
					<a
						href="/jobs/{conversation.jobId}/"
						class="inline-flex items-center gap-2 px-4 py-2 bg-primary-50 hover:bg-primary-100 border border-primary-200 rounded-xl transition-colors text-sm"
					>
						<Building2 size={14} class="text-primary-600" />
						<span class="text-primary-700 font-medium">{conversation.jobTitle}</span>
						<ExternalLink size={12} class="text-primary-500" />
					</a>
				</div>
			</div>
		</header>

		<!-- Main Content Area -->
		<div class="flex-1 flex overflow-hidden">
			<!-- Messages Area -->
			<div class="flex-1 flex flex-col">
				<!-- Messages -->
				<div id="messages-container" class="flex-1 overflow-y-auto p-4 lg:p-6">
					<div class="max-w-3xl mx-auto space-y-6">
						{#each Object.entries(groupedMessages) as [date, dateMessages]}
							<div class="space-y-4">
								<!-- Date Divider -->
								<div class="flex items-center justify-center">
									<div class="bg-gray-200 text-gray-600 text-xs px-3 py-1 rounded-full font-medium">
										{date}
									</div>
								</div>

								<!-- Messages for this date -->
								{#each dateMessages as message (message.id)}
									<div class="flex" class:justify-end={message.sender === 'me'}>
										<div class="max-w-[75%] md:max-w-[65%]">
											<div
												class="rounded-2xl px-4 py-3 {message.sender === 'me'
													? 'bg-primary-600 text-white'
													: 'bg-white text-gray-900 elevation-1 border border-gray-100'}"
											>
												<p class="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
											</div>

											<div
												class="flex items-center gap-1.5 mt-1.5 px-1"
												class:justify-end={message.sender === 'me'}
											>
												<span class="text-xs text-gray-500"
													>{formatMessageTime(message.timestamp)}</span
												>
												{#if message.sender === 'me'}
													<span>
														{#if message.read}
															<CheckCheck size={14} class="text-primary-500" />
														{:else}
															<Check size={14} class="text-gray-400" />
														{/if}
													</span>
												{/if}
											</div>
										</div>
									</div>
								{/each}
							</div>
						{/each}
					</div>
				</div>

				<!-- Message Input -->
				<div class="border-t border-gray-200 bg-white">
					<div class="max-w-3xl mx-auto p-4">
						<!-- Attachment Menu -->
						{#if showAttachmentMenu}
							<div class="mb-3 flex items-center gap-2">
								<button
									onclick={() => attachFile('image')}
									class="flex items-center gap-2 px-4 py-2 bg-primary-50 hover:bg-primary-100 text-primary-700 rounded-xl transition-colors text-sm font-medium"
								>
									<ImageIcon size={16} />
									Изображение
								</button>
								<button
									onclick={() => attachFile('file')}
									class="flex items-center gap-2 px-4 py-2 bg-primary-50 hover:bg-primary-100 text-primary-700 rounded-xl transition-colors text-sm font-medium"
								>
									<File size={16} />
									Файл
								</button>
								<button
									onclick={() => (showAttachmentMenu = false)}
									class="ml-auto text-gray-500 hover:text-gray-700 p-1"
								>
									<X size={18} />
								</button>
							</div>
						{/if}

						<form
							onsubmit={(e) => {
								e.preventDefault();
								sendMessage();
							}}
							class="flex items-end gap-3"
						>
							<div class="flex-1 relative">
								<textarea
									bind:value={messageText}
									onkeypress={handleKeyPress}
									placeholder="Введите сообщение..."
									rows="1"
									class="w-full px-4 py-3 pr-20 border border-gray-200 rounded-2xl bg-gray-50 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 resize-none transition-all outline-none text-gray-900 placeholder-gray-500"
									style="min-height: 48px; max-height: 120px;"
								></textarea>

								<div class="absolute bottom-3 right-3 flex items-center gap-1">
									<button
										type="button"
										onclick={() => (showAttachmentMenu = !showAttachmentMenu)}
										class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
										title="Прикрепить файл"
									>
										<Paperclip size={18} />
									</button>
									<button
										type="button"
										class="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
										title="Добавить эмодзи"
									>
										<Smile size={18} />
									</button>
								</div>
							</div>

							<button
								type="submit"
								disabled={!messageText.trim()}
								class="bg-primary-600 hover:bg-primary-700 text-white font-medium p-3.5 rounded-2xl transition-colors elevation-1 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
								title="Отправить сообщение"
							>
								<Send size={20} />
							</button>
						</form>

						<p class="text-xs text-gray-500 mt-2 text-center">
							Нажмите Enter для отправки, Shift+Enter для новой строки
						</p>
					</div>
				</div>
			</div>

			<!-- Recruiter Info Sidebar (Desktop) -->
			{#if showRecruiterInfo}
				<div
					class="hidden lg:block w-80 border-l border-gray-200 bg-white overflow-y-auto animate-slide-in-right"
				>
					<div class="p-6">
						<div class="flex items-center justify-between mb-6">
							<h3 class="text-lg font-semibold text-gray-900">Информация о разговоре</h3>
							<button
								onclick={() => (showRecruiterInfo = false)}
								class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
							>
								<X size={18} class="text-gray-500" />
							</button>
						</div>

						<!-- Recruiter Details -->
						<div class="text-center mb-6 pb-6 border-b border-gray-200">
							<div
								class="w-20 h-20 bg-primary-600 rounded-2xl flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4"
							>
								{getInitials(conversation.recruiter.name)}
							</div>
							<h4 class="font-semibold text-gray-900 text-lg mb-1">{conversation.recruiter.name}</h4>
							<p class="text-sm text-gray-600 mb-1">{conversation.recruiter.position}</p>
							<p class="text-sm text-gray-500">{conversation.recruiter.company}</p>
							{#if conversation.recruiter.online}
								<span
									class="inline-flex items-center gap-1.5 mt-3 text-sm text-success-600 bg-success-500/10 px-3 py-1 rounded-full"
								>
									<span class="w-2 h-2 bg-success-500 rounded-full"></span>
									В сети
								</span>
							{:else}
								<span
									class="inline-flex items-center gap-1.5 mt-3 text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full"
								>
									<span class="w-2 h-2 bg-gray-400 rounded-full"></span>
									Не в сети
								</span>
							{/if}
						</div>

						<!-- Contact Info -->
						<div class="space-y-4 mb-6 pb-6 border-b border-gray-200">
							<h4 class="font-medium text-gray-900 text-sm">Контактная информация</h4>
							<div class="space-y-3">
								<div>
									<p class="text-xs text-gray-500 mb-1">Эл. почта</p>
									<a
										href="mailto:{conversation.recruiter.email}"
										class="text-sm text-primary-600 hover:underline flex items-center gap-1.5"
									>
										<Mail size={14} />
										{conversation.recruiter.email}
									</a>
								</div>
								<div>
									<p class="text-xs text-gray-500 mb-1">Телефон</p>
									<a
										href="tel:{conversation.recruiter.phone}"
										class="text-sm text-primary-600 hover:underline flex items-center gap-1.5"
									>
										<Phone size={14} />
										{conversation.recruiter.phone}
									</a>
								</div>
							</div>
						</div>

						<!-- Job Info -->
						<div class="space-y-4">
							<h4 class="font-medium text-gray-900 text-sm">Связанная вакансия</h4>
							<a
								href="/jobs/{conversation.jobId}/"
								class="block p-4 bg-primary-50 hover:bg-primary-100 border border-primary-200 rounded-2xl transition-colors"
							>
								<p class="font-semibold text-gray-900 mb-1">{conversation.jobTitle}</p>
								<p class="text-sm text-gray-600">{conversation.recruiter.company}</p>
								<p class="text-xs text-primary-600 mt-2 flex items-center gap-1">
									Просмотреть вакансию
									<ExternalLink size={12} />
								</p>
							</a>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>

	<!-- Mobile Recruiter Info Modal -->
	{#if showRecruiterInfo}
		<div class="lg:hidden fixed inset-0 z-50 flex items-end justify-center">
			<div class="absolute inset-0 bg-black/50"></div>
			<button
				type="button"
				class="absolute inset-0 cursor-default"
				onclick={() => (showRecruiterInfo = false)}
				onkeydown={(event) => {
					if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') {
						event.preventDefault();
						showRecruiterInfo = false;
					}
				}}
				aria-label="Закрыть информацию о рекрутере"
			></button>
			<div
				class="relative bottom-0 left-0 right-0 bg-white rounded-t-3xl p-6 max-h-[80vh] overflow-y-auto animate-fade-in-up"
				role="dialog"
				aria-modal="true"
				aria-label="Информация о рекрутере"
				tabindex="-1"
				onpointerdown={(event) => event.stopPropagation()}
			>
				<div class="w-12 h-1 bg-gray-300 rounded-full mx-auto mb-6"></div>

				<!-- Recruiter Details -->
				<div class="text-center mb-6 pb-6 border-b border-gray-200">
					<div
						class="w-20 h-20 bg-primary-600 rounded-2xl flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4"
					>
						{getInitials(conversation.recruiter.name)}
					</div>
					<h4 class="font-semibold text-gray-900 text-lg mb-1">{conversation.recruiter.name}</h4>
					<p class="text-sm text-gray-600 mb-1">{conversation.recruiter.position}</p>
					<p class="text-sm text-gray-500">{conversation.recruiter.company}</p>
					{#if conversation.recruiter.online}
						<span
							class="inline-flex items-center gap-1.5 mt-3 text-sm text-success-600 bg-success-500/10 px-3 py-1 rounded-full"
						>
							<span class="w-2 h-2 bg-success-500 rounded-full"></span>
							В сети
						</span>
					{:else}
						<span
							class="inline-flex items-center gap-1.5 mt-3 text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full"
						>
							<span class="w-2 h-2 bg-gray-400 rounded-full"></span>
							Не в сети
						</span>
					{/if}
				</div>

				<!-- Contact Info -->
				<div class="space-y-4 mb-6 pb-6 border-b border-gray-200">
					<h4 class="font-medium text-gray-900">Контактная информация</h4>
					<div class="space-y-3">
						<div>
							<p class="text-xs text-gray-500 mb-1">Эл. почта</p>
							<a
								href="mailto:{conversation.recruiter.email}"
								class="text-sm text-primary-600 hover:underline flex items-center gap-1.5"
							>
								<Mail size={14} />
								{conversation.recruiter.email}
							</a>
						</div>
						<div>
							<p class="text-xs text-gray-500 mb-1">Телефон</p>
							<a
								href="tel:{conversation.recruiter.phone}"
								class="text-sm text-primary-600 hover:underline flex items-center gap-1.5"
							>
								<Phone size={14} />
								{conversation.recruiter.phone}
							</a>
						</div>
					</div>
				</div>

				<!-- Job Info -->
				<div class="space-y-4">
					<h4 class="font-medium text-gray-900">Связанная вакансия</h4>
					<a
						href="/jobs/{conversation.jobId}/"
						class="block p-4 bg-primary-50 hover:bg-primary-100 border border-primary-200 rounded-2xl transition-colors"
					>
						<p class="font-semibold text-gray-900 mb-1">{conversation.jobTitle}</p>
						<p class="text-sm text-gray-600">{conversation.recruiter.company}</p>
						<p class="text-xs text-primary-600 mt-2 flex items-center gap-1">
							Просмотреть вакансию
							<ExternalLink size={12} />
						</p>
					</a>
				</div>
			</div>
		</div>
	{/if}
{:else}
	<!-- Loading or not found -->
	<div class="flex items-center justify-center min-h-screen bg-surface-50">
		<div class="text-center">
			<div
				class="w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"
			></div>
			<p class="text-gray-500">Загрузка разговора...</p>
		</div>
	</div>
{/if}
