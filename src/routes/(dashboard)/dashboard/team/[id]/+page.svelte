<script lang="ts">
	import {
		ArrowLeft,
		Mail,
		Phone,
		Calendar,
		Briefcase,
		Users,
		Eye,
		Crown,
		Shield,
		CheckCircle,
		Clock,
		TrendingUp,
		FileText
	} from '@lucide/svelte';

	let { data } = $props();
	let member = $derived(data.member);

	function formatDate(dateString?: string): string {
		if (!dateString) return '—';
		const date = new Date(dateString);
		return date.toLocaleDateString('ru-RU', { month: 'long', day: 'numeric', year: 'numeric' });
	}

	function getJobStatusLabel(status: string): string {
		const labels: Record<string, string> = {
			Live: 'Активна',
			Draft: 'Черновик',
			Disabled: 'Закрыта',
			Expired: 'Истекла'
		};
		return labels[status] || status;
	}

	function getInitials(firstName: string, lastName: string): string {
		return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
	}
</script>

<svelte:head>
	<title>{member.first_name} {member.last_name} — участник команды — PeelJobs</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center gap-4">
		<a
			href="/dashboard/team/"
			class="p-2 hover:bg-surface rounded-lg transition-colors"
			title="Назад к команде"
		>
			<ArrowLeft class="w-5 h-5" />
		</a>
		<div>
			<h1 class="text-2xl md:text-3xl font-bold text-black">Профиль участника команды</h1>
			<p class="text-muted mt-1">Результаты работы и история активности</p>
		</div>
	</div>

	<!-- Member Profile Card -->
	<div class="bg-white rounded-lg border border-border p-6">
		<div class="flex items-start gap-6">
			<!-- Avatar -->
			<div class="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
				{#if member.profile_pic}
					<img
						src={member.profile_pic}
						alt="{member.first_name} {member.last_name}"
						class="w-full h-full rounded-full object-cover"
					/>
				{:else}
					<span class="text-3xl font-bold text-primary">
						{getInitials(member.first_name, member.last_name)}
					</span>
				{/if}
			</div>

			<!-- Member Info -->
			<div class="flex-1">
				<div class="flex items-center gap-3 mb-2">
					<h2 class="text-2xl font-bold text-black">
						{member.first_name}
						{member.last_name}
					</h2>
					{#if member.is_admin}
						<span class="inline-flex items-center gap-1 px-3 py-1 bg-purple-100 text-purple-800 text-sm font-medium rounded-full">
							<Crown class="w-4 h-4" />
							Администратор
						</span>
					{/if}
					{#if member.is_active}
						<span class="inline-flex items-center gap-1 px-3 py-1 bg-success-light text-success text-sm font-medium rounded-full">
							<CheckCircle class="w-4 h-4" />
							Активен
						</span>
					{:else}
						<span class="inline-flex items-center gap-1 px-3 py-1 bg-surface text-black text-sm font-medium rounded-full">
							<Clock class="w-4 h-4" />
							Неактивен
						</span>
					{/if}
				</div>

				<p class="text-lg text-muted mb-4">{member.job_title || 'Должность не указана'}</p>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
					<div class="flex items-center gap-2 text-muted">
						<Mail class="w-4 h-4" />
						<a href="mailto:{member.email}" class="hover:text-primary">{member.email}</a>
					</div>

					{#if member.mobile}
						<div class="flex items-center gap-2 text-muted">
							<Phone class="w-4 h-4" />
							<a href="tel:{member.mobile}" class="hover:text-primary">{member.mobile}</a>
						</div>
					{/if}

					<div class="flex items-center gap-2 text-muted">
						<Calendar class="w-4 h-4" />
						<span>В команде с {formatDate(member.date_joined)}</span>
					</div>

					{#if member.last_login}
						<div class="flex items-center gap-2 text-muted">
							<Clock class="w-4 h-4" />
							<span>Последняя активность: {formatDate(member.last_login)}</span>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>

	<!-- Stats Cards -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
		<div class="bg-white rounded-lg border border-border p-6">
			<div class="flex items-center gap-3 mb-3">
				<div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
					<Briefcase class="w-5 h-5 text-primary" />
				</div>
				<h3 class="text-sm font-medium text-muted">Опубликовано вакансий</h3>
			</div>
			<div class="text-3xl font-bold text-black">{member.stats?.jobs_posted || 0}</div>
			<div class="flex items-center gap-1 mt-2 text-sm text-muted">
				<TrendingUp class="w-4 h-4" />
				<span>{member.stats?.active_jobs || 0} активны сейчас</span>
			</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-6">
			<div class="flex items-center gap-3 mb-3">
				<div class="w-10 h-10 bg-success-light rounded-lg flex items-center justify-center">
					<Users class="w-5 h-5 text-success" />
				</div>
				<h3 class="text-sm font-medium text-muted">Всего откликов</h3>
			</div>
			<div class="text-3xl font-bold text-black">{member.stats?.total_applicants || 0}</div>
			<div class="text-sm text-muted mt-2">По всем вакансиям</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-6">
			<div class="flex items-center gap-3 mb-3">
				<div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
					<Eye class="w-5 h-5 text-purple-600" />
				</div>
				<h3 class="text-sm font-medium text-muted">Всего просмотров</h3>
			</div>
			<div class="text-3xl font-bold text-black">{member.stats?.total_views || 0}</div>
			<div class="text-sm text-muted mt-2">По всем вакансиям</div>
		</div>
	</div>

	<!-- Recent Jobs -->
	{#if member.recent_jobs && member.recent_jobs.length > 0}
		<div class="bg-white rounded-lg border border-border">
			<div class="p-6 border-b border-border">
				<h3 class="text-lg font-semibold text-black flex items-center gap-2">
					<FileText class="w-5 h-5" />
					Последние вакансии
				</h3>
			</div>
			<div class="divide-y divide-border">
				{#each member.recent_jobs as job}
					<a
						href="/dashboard/jobs/{job.id}/"
						class="flex items-center justify-between p-4 hover:bg-surface transition-colors"
					>
						<div class="flex-1">
							<h4 class="font-medium text-black hover:text-primary">{job.title}</h4>
							<div class="flex items-center gap-4 mt-1 text-sm text-muted">
								<span class="inline-flex items-center gap-1">
									<span class="px-2 py-0.5 rounded text-xs font-medium {job.status === 'Live'
										? 'bg-success-light text-success'
										: job.status === 'Draft'
											? 'bg-surface text-black'
											: 'bg-error-light text-error'}">
										{getJobStatusLabel(job.status)}
									</span>
								</span>
								<span>Опубликовано {formatDate(job.posted_date)}</span>
							</div>
						</div>
						<div class="flex items-center gap-6 text-sm">
							<div class="flex items-center gap-1 text-muted">
								<Users class="w-4 h-4" />
								<span>{job.applicants_count}</span>
							</div>
							<div class="flex items-center gap-1 text-muted">
								<Eye class="w-4 h-4" />
								<span>{job.views_count || 0}</span>
							</div>
						</div>
					</a>
				{/each}
			</div>
		</div>
	{:else}
		<div class="bg-white rounded-lg border border-border p-12 text-center">
			<Briefcase class="w-12 h-12 text-muted mx-auto mb-4" />
			<h3 class="text-lg font-semibold text-black mb-2">Вакансий пока нет</h3>
			<p class="text-muted">Этот участник команды ещё не публиковал вакансии</p>
		</div>
	{/if}

	<!-- Permissions Section -->
	<div class="bg-white rounded-lg border border-border p-6">
		<h3 class="text-lg font-semibold text-black mb-4 flex items-center gap-2">
			<Shield class="w-5 h-5" />
			Права доступа
		</h3>
		<div class="space-y-2">
			<div class="flex items-center justify-between py-2">
				<span class="text-muted">Публикация вакансий</span>
				{#if member.permissions?.can_post_jobs}
					<CheckCircle class="w-5 h-5 text-success" />
				{:else}
					<span class="text-sm text-muted">Нет доступа</span>
				{/if}
			</div>
			<div class="flex items-center justify-between py-2">
				<span class="text-muted">Управление командой</span>
				{#if member.permissions?.can_manage_team}
					<CheckCircle class="w-5 h-5 text-success" />
				{:else}
					<span class="text-sm text-muted">Нет доступа</span>
				{/if}
			</div>
			<div class="flex items-center justify-between py-2">
				<span class="text-muted">Редактирование профиля компании</span>
				{#if member.permissions?.can_edit_company}
					<CheckCircle class="w-5 h-5 text-success" />
				{:else}
					<span class="text-sm text-muted">Нет доступа</span>
				{/if}
			</div>
			<div class="flex items-center justify-between py-2">
				<span class="text-muted">Администратор компании</span>
				{#if member.permissions?.is_company_admin}
					<CheckCircle class="w-5 h-5 text-success" />
				{:else}
					<span class="text-sm text-muted">Нет доступа</span>
				{/if}
			</div>
		</div>
	</div>
</div>
