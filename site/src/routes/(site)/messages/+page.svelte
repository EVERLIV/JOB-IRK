<script lang="ts">
	import { MessageSquare, Search, Archive, Star, Trash2, ChevronRight, Inbox, Mail, Circle, Clock, Building2 } from '@lucide/svelte';
	import { goto } from '$app/navigation';

	interface RecruiterSummary {
		name: string;
		company: string;
		position: string;
		avatar: string | null;
		online: boolean;
	}

	type FilterType = 'all' | 'unread' | 'starred' | 'archived';

	interface ConversationSummary {
		id: number;
		recruiter: RecruiterSummary;
		jobTitle: string;
		lastMessage: string;
		lastMessageSender: 'me' | 'recruiter';
		timestamp: string;
		unread: number;
		starred: boolean;
		archived: boolean;
	}

	let conversations = $state<ConversationSummary[]>([
		{
			id: 1,
			recruiter: {
				name: 'Sarah Johnson',
				company: 'Innovate Inc.',
				position: 'Старший рекрутер',
				avatar: null,
				online: true
			},
			jobTitle: 'Senior Software Engineer',
			lastMessage: 'Отлично! Когда вам будет удобно созвониться?',
			lastMessageSender: 'recruiter',
			timestamp: '2024-01-18T14:30:00',
			unread: 2,
			starred: false,
			archived: false
		},
		{
			id: 2,
			recruiter: {
				name: 'Michael Chen',
				company: 'Tech Corp',
				position: 'Менеджер по подбору персонала',
				avatar: null,
				online: false
			},
			jobTitle: 'Full Stack Developer',
			lastMessage: 'Мы хотели бы назначить с вами собеседование.',
			lastMessageSender: 'recruiter',
			timestamp: '2024-01-18T10:15:00',
			unread: 1,
			starred: true,
			archived: false
		},
		{
			id: 3,
			recruiter: {
				name: 'Emily Rodriguez',
				company: 'StartupXYZ',
				position: 'HR-менеджер',
				avatar: null,
				online: true
			},
			jobTitle: 'React Developer',
			lastMessage: 'Отлично! Скоро отправлю приглашение на встречу.',
			lastMessageSender: 'recruiter',
			timestamp: '2024-01-17T16:45:00',
			unread: 0,
			starred: false,
			archived: false
		},
		{
			id: 4,
			recruiter: {
				name: 'David Williams',
				company: 'Cloud Solutions',
				position: 'Ведущий рекрутер',
				avatar: null,
				online: false
			},
			jobTitle: 'DevOps Engineer',
			lastMessage: 'Спасибо за ваш интерес!',
			lastMessageSender: 'recruiter',
			timestamp: '2024-01-16T14:20:00',
			unread: 0,
			starred: false,
			archived: false
		},
		{
			id: 5,
			recruiter: {
				name: 'Jessica Park',
				company: 'Data Analytics Inc.',
				position: 'Технический рекрутер',
				avatar: null,
				online: true
			},
			jobTitle: 'Backend Engineer',
			lastMessage: 'С нетерпением жду нашего разговора!',
			lastMessageSender: 'me',
			timestamp: '2024-01-15T11:30:00',
			unread: 0,
			starred: true,
			archived: false
		}
	]);

	let searchQuery = $state('');
	let filterType = $state<FilterType>('all');

	const totalUnread = $derived(
		conversations
			.filter((conversation) => !conversation.archived)
			.reduce((sum, conversation) => sum + conversation.unread, 0)
	);

	const starredCount = $derived(
		conversations.filter((conversation) => conversation.starred && !conversation.archived).length
	);

	const filteredConversations = $derived(
		(() => {
			const searchLower = searchQuery.toLowerCase();

			return conversations
				.filter((conversation) => {
					if (filterType === 'unread' && conversation.unread === 0) return false;
					if (filterType === 'starred' && !conversation.starred) return false;
					if (filterType === 'archived' && !conversation.archived) return false;
					if (filterType === 'all' && conversation.archived) return false;

					return (
						conversation.recruiter.name.toLowerCase().includes(searchLower) ||
						conversation.recruiter.company.toLowerCase().includes(searchLower) ||
						conversation.jobTitle.toLowerCase().includes(searchLower) ||
						conversation.lastMessage.toLowerCase().includes(searchLower)
					);
				})
				.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
		})()
	);

	function openConversation(id: number): void {
		goto(`/messages/${id}/`);
	}

	function toggleStar(id: number, event: MouseEvent): void {
		event.stopPropagation();
		conversations = conversations.map((conversation) =>
			conversation.id === id ? { ...conversation, starred: !conversation.starred } : conversation
		);
	}

	function archiveConversation(id: number, event: MouseEvent): void {
		event.stopPropagation();
		conversations = conversations.map((conversation) =>
			conversation.id === id ? { ...conversation, archived: true } : conversation
		);
	}

	function deleteConversation(id: number, event: MouseEvent): void {
		event.stopPropagation();
		if (
			confirm('Вы уверены, что хотите удалить этот разговор? Это действие нельзя отменить.')
		) {
			conversations = conversations.filter((conversation) => conversation.id !== id);
		}
	}

	function formatTimestamp(timestamp: string): string {
		const date = new Date(timestamp);
		const now = new Date();
		const diffMs = now.getTime() - date.getTime();
		const diffMins = Math.floor(diffMs / 60000);
		const diffHours = Math.floor(diffMs / 3600000);
		const diffDays = Math.floor(diffMs / 86400000);

		if (diffMins < 1) return 'Только что';
		if (diffMins < 60) return `${diffMins} мин. назад`;
		if (diffHours < 24) return `${diffHours} ч. назад`;
		if (diffDays === 1) return 'Вчера';
		if (diffDays < 7) return `${diffDays} дн. назад`;

		return date.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric' });
	}
</script>

<svelte:head>
	<title>Сообщения - PeelJobs</title>
	<meta name="description" content="Общайтесь с рекрутерами и HR-менеджерами" />
</svelte:head>

<!-- Hero Section -->
<section class="bg-[#1D2226] text-white py-12 lg:py-16 relative overflow-hidden">
	<!-- Decorative Elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
		<div class="absolute bottom-0 right-1/4 w-80 h-80 bg-primary/10 rounded-full blur-3xl"></div>
	</div>

	<div class="max-w-7xl mx-auto px-4 lg:px-8 relative">
		<!-- Breadcrumb -->
		<nav class="mb-6" aria-label="Навигация">
			<ol class="flex items-center gap-2 text-sm text-muted">
				<li>
					<a href="/jobseeker-dashboard/" class="hover:text-white transition-colors">Панель управления</a>
				</li>
				<li class="flex items-center gap-2">
					<ChevronRight size={14} />
					<span class="text-white font-medium">Сообщения</span>
				</li>
			</ol>
		</nav>

		<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
			<div class="flex items-center gap-4">
				<div
					class="w-14 h-14 rounded-lg bg-white/10 flex items-center justify-center animate-fade-in-up"
					style="opacity: 0;"
				>
					<MessageSquare size={28} class="text-white/80" />
				</div>
				<div>
					<h1
						class="text-3xl lg:text-4xl font-semibold tracking-tight mb-1 animate-fade-in-up"
						style="opacity: 0; animation-delay: 100ms;"
					>
						Сообщения
					</h1>
					<p
						class="text-gray-300 animate-fade-in-up"
						style="opacity: 0; animation-delay: 150ms;"
					>
						{totalUnread > 0
							? `${totalUnread} непрочитанн${totalUnread > 1 ? 'ых' : 'ое'} сообщени${totalUnread > 1 ? 'й' : 'е'}`
							: 'Всё прочитано!'}
					</p>
				</div>
			</div>

			<!-- Filter Tabs (Desktop) -->
			<div
				class="hidden lg:flex items-center gap-2 animate-fade-in-up"
				style="opacity: 0; animation-delay: 200ms;"
			>
				<button
					onclick={() => (filterType = 'all')}
					class="px-4 py-2.5 rounded-full text-sm font-medium transition-all {filterType === 'all'
						? 'bg-white text-black'
						: 'bg-white/10 text-white hover:bg-white/20'}"
				>
					Все
				</button>
				<button
					onclick={() => (filterType = 'unread')}
					class="px-4 py-2.5 rounded-full text-sm font-medium transition-all flex items-center gap-2 {filterType ===
					'unread'
						? 'bg-white text-black'
						: 'bg-white/10 text-white hover:bg-white/20'}"
				>
					Непрочитанные
					{#if totalUnread > 0}
						<span
							class="text-xs px-2 py-0.5 rounded-full {filterType === 'unread'
								? 'bg-primary text-white'
								: 'bg-primary text-white'}">{totalUnread}</span
						>
					{/if}
				</button>
				<button
					onclick={() => (filterType = 'starred')}
					class="px-4 py-2.5 rounded-full text-sm font-medium transition-all flex items-center gap-2 {filterType ===
					'starred'
						? 'bg-white text-black'
						: 'bg-white/10 text-white hover:bg-white/20'}"
				>
					<Star size={14} />
					Избранные
				</button>
				<button
					onclick={() => (filterType = 'archived')}
					class="px-4 py-2.5 rounded-full text-sm font-medium transition-all flex items-center gap-2 {filterType ===
					'archived'
						? 'bg-white text-black'
						: 'bg-white/10 text-white hover:bg-white/20'}"
				>
					<Archive size={14} />
					Архив
				</button>
			</div>
		</div>
	</div>
</section>

<!-- Main Content -->
<section class="py-8 lg:py-12 bg-surface min-h-[60vh]">
	<div class="max-w-4xl mx-auto px-4 lg:px-8">
		<!-- Mobile Filter Tabs -->
		<div
			class="lg:hidden mb-4 flex items-center gap-2 overflow-x-auto pb-2 animate-fade-in-up"
			style="opacity: 0;"
		>
			<button
				onclick={() => (filterType = 'all')}
				class="px-4 py-2.5 rounded-full text-sm font-medium whitespace-nowrap flex-shrink-0 transition-all {filterType ===
				'all'
					? 'bg-primary text-white shadow-sm'
					: 'bg-white text-muted'}"
			>
				Все
			</button>
			<button
				onclick={() => (filterType = 'unread')}
				class="px-4 py-2.5 rounded-full text-sm font-medium whitespace-nowrap flex-shrink-0 flex items-center gap-2 transition-all {filterType ===
				'unread'
					? 'bg-primary text-white shadow-sm'
					: 'bg-white text-muted'}"
			>
				Непрочитанные
				{#if totalUnread > 0}
					<span
						class="text-xs px-2 py-0.5 rounded-full {filterType === 'unread'
							? 'bg-white text-primary'
							: 'bg-primary text-white'}">{totalUnread}</span
					>
				{/if}
			</button>
			<button
				onclick={() => (filterType = 'starred')}
				class="px-4 py-2.5 rounded-full text-sm font-medium whitespace-nowrap flex-shrink-0 flex items-center gap-2 transition-all {filterType ===
				'starred'
					? 'bg-primary text-white shadow-sm'
					: 'bg-white text-muted'}"
			>
				<Star size={14} />
				Избранные
			</button>
			<button
				onclick={() => (filterType = 'archived')}
				class="px-4 py-2.5 rounded-full text-sm font-medium whitespace-nowrap flex-shrink-0 flex items-center gap-2 transition-all {filterType ===
				'archived'
					? 'bg-primary text-white shadow-sm'
					: 'bg-white text-muted'}"
			>
				<Archive size={14} />
				Архив
			</button>
		</div>

		<!-- Search Bar -->
		<div
			class="bg-white rounded-lg p-4 lg:p-5 shadow-sm border border-border mb-6 animate-fade-in-up"
			style="opacity: 0; animation-delay: 50ms;"
		>
			<div class="relative">
				<div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
					<Search size={18} class="text-muted" />
				</div>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Поиск по имени, компании, вакансии или сообщению..."
					class="w-full pl-11 pr-4 py-3 border border-border rounded-xl bg-gray-50 text-black placeholder-muted focus:bg-white focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all outline-none"
				/>
			</div>
		</div>

		<!-- Conversations List -->
		{#if filteredConversations.length > 0}
			<div
				class="bg-white rounded-lg shadow-sm border border-border overflow-hidden divide-y divide-border animate-fade-in-up"
				style="opacity: 0; animation-delay: 100ms;"
			>
				{#each filteredConversations as conversation, i (conversation.id)}
					<div
						class="group flex items-start gap-4 p-5 lg:p-6 hover:bg-surface transition-colors cursor-pointer {conversation.unread >
						0
							? 'bg-primary/5'
							: ''}"
						onclick={() => openConversation(conversation.id)}
						onkeydown={(e) => e.key === 'Enter' && openConversation(conversation.id)}
						role="button"
						tabindex="0"
						style="animation: fade-in-up 0.5s ease forwards; animation-delay: {(i + 1) * 50 + 100}ms; opacity: 0;"
					>
						<!-- Avatar -->
						<div class="relative flex-shrink-0">
							<div
								class="w-12 h-12 {conversation.unread > 0
									? 'bg-primary'
									: 'bg-gray-200'} rounded-xl flex items-center justify-center text-lg font-semibold {conversation.unread >
								0
									? 'text-white'
									: 'text-muted'}"
							>
								{conversation.recruiter.name.charAt(0)}
							</div>
							{#if conversation.recruiter.online}
								<div
									class="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-success border-2 border-white rounded-full"
								></div>
							{/if}
						</div>

						<!-- Content -->
						<div class="flex-1 min-w-0">
							<div class="flex items-start justify-between mb-1.5">
								<div class="flex items-center gap-2 min-w-0">
									{#if conversation.unread > 0}
										<Circle size={8} class="text-primary fill-primary flex-shrink-0" />
									{/if}
									<h3
										class="font-semibold text-black truncate {conversation.unread > 0
											? ''
											: 'text-muted'}"
									>
										{conversation.recruiter.name}
									</h3>
									{#if conversation.starred}
										<Star size={14} class="text-warning fill-warning flex-shrink-0" />
									{/if}
								</div>
								<div class="flex items-center gap-2 flex-shrink-0 ml-2">
									<span class="text-xs text-muted flex items-center gap-1">
										<Clock size={12} />
										{formatTimestamp(conversation.timestamp)}
									</span>
									{#if conversation.unread > 0}
										<span
											class="bg-primary text-white text-xs px-2 py-0.5 rounded-full font-medium"
										>
											{conversation.unread}
										</span>
									{/if}
								</div>
							</div>

							<div class="flex items-center gap-2 text-sm text-muted mb-2">
								<Building2 size={14} class="text-muted flex-shrink-0" />
								<span class="truncate"
									>{conversation.recruiter.position} в {conversation.recruiter.company}</span
								>
							</div>

							<div class="flex items-center gap-2 mb-2">
								<span class="text-xs bg-primary/10 text-primary px-2.5 py-1 rounded-full">
									{conversation.jobTitle}
								</span>
							</div>

							<p class="text-sm text-muted line-clamp-1">
								{#if conversation.lastMessageSender === 'me'}
									<span class="text-muted font-medium">Вы: </span>
								{/if}
								{conversation.lastMessage}
							</p>
						</div>

						<!-- Actions -->
						<div
							class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0"
						>
							<button
								onclick={(e) => toggleStar(conversation.id, e)}
								class="p-2 hover:bg-gray-100 rounded-xl transition-colors"
								title={conversation.starred ? 'Убрать из избранного' : 'В избранное'}
							>
								<Star
									size={16}
									class={conversation.starred
										? 'text-warning fill-warning'
										: 'text-muted'}
								/>
							</button>
							{#if !conversation.archived}
								<button
									onclick={(e) => archiveConversation(conversation.id, e)}
									class="p-2 hover:bg-gray-100 rounded-xl transition-colors"
									title="В архив"
								>
									<Archive size={16} class="text-muted" />
								</button>
							{/if}
							<button
								onclick={(e) => deleteConversation(conversation.id, e)}
								class="p-2 hover:bg-error-light rounded-xl transition-colors"
								title="Удалить"
							>
								<Trash2 size={16} class="text-error" />
							</button>
						</div>

						<!-- Arrow -->
						<ChevronRight
							size={20}
							class="text-gray-300 group-hover:text-primary group-hover:translate-x-0.5 transition-all flex-shrink-0 self-center"
						/>
					</div>
				{/each}
			</div>
		{:else}
			<!-- Empty State -->
			<div
				class="bg-white rounded-lg p-12 shadow-sm border border-border text-center animate-fade-in-up"
				style="opacity: 0; animation-delay: 100ms;"
			>
				<div
					class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-6"
				>
					{#if filterType === 'archived'}
						<Archive size={36} class="text-muted" />
					{:else if filterType === 'starred'}
						<Star size={36} class="text-muted" />
					{:else if filterType === 'unread'}
						<Mail size={36} class="text-muted" />
					{:else}
						<Inbox size={36} class="text-muted" />
					{/if}
				</div>
				<h3 class="text-xl font-semibold text-black mb-2">
					{#if filterType === 'archived'}
						Нет архивных разговоров
					{:else if filterType === 'starred'}
						Нет избранных разговоров
					{:else if filterType === 'unread'}
						Нет непрочитанных сообщений
					{:else if searchQuery}
						Разговоры не найдены
					{:else}
						Пока нет сообщений
					{/if}
				</h3>
				<p class="text-muted max-w-md mx-auto">
					{#if searchQuery}
						Попробуйте изменить параметры поиска или фильтры
					{:else if filterType === 'all'}
						Здесь будут отображаться ваши разговоры с рекрутерами
					{:else if filterType === 'archived'}
						Архивные разговоры будут отображаться здесь
					{:else if filterType === 'starred'}
						Добавляйте важные разговоры в избранное
					{:else if filterType === 'unread'}
						Всё прочитано!
					{/if}
				</p>
			</div>
		{/if}

		<!-- Info Card -->
		{#if filteredConversations.length > 0}
			<div
				class="mt-8 bg-primary/10 rounded-lg p-5 lg:p-6 border border-primary/20 animate-fade-in-up"
				style="opacity: 0; animation-delay: 400ms;"
			>
				<div class="flex items-start gap-4">
					<div
						class="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center flex-shrink-0"
					>
						<MessageSquare size={22} class="text-primary" />
					</div>
					<div>
						<h3 class="font-semibold text-black mb-1">Будьте на связи</h3>
						<p class="text-sm text-muted">
							Быстрые ответы рекрутерам повышают ваши шансы. Старайтесь отвечать в течение 24-48
							часов, чтобы поддерживать диалог и производить хорошее впечатление.
						</p>
					</div>
				</div>
			</div>
		{/if}
	</div>
</section>
