<script lang="ts">
	import { untrack } from 'svelte';
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import {
		Plus,
		Search,
		Filter,
		Eye,
		Users,
		Edit,
		XCircle,
		ExternalLink,
		Calendar,
		MapPin,
		Briefcase,
		Send,
		Archive,
		Copy
	} from '@lucide/svelte';
	import { Button, Card, Badge } from '$lib/components/ui';
	import type { JobStatus } from '$lib/types';

	// Get data from server-side load function
	let { data } = $props();

	// Initialize filters from URL params (one-time snapshot, not reactive)
	let searchQuery = $state(untrack(() => data.filters.search));
	let selectedFilter = $state<JobStatus | 'all'>(untrack(() => data.filters.status as JobStatus | 'all'));
	let viewMode = $state<'grid' | 'list'>('list');
	let submittingAction = $state<number | null>(null);

	const filterOptions = [
		{ value: 'all', label: 'Все вакансии' },
		{ value: 'Live', label: 'Активные' },
		{ value: 'Draft', label: 'Черновики' },
		{ value: 'Disabled', label: 'Закрытые' },
		{ value: 'Expired', label: 'Истекшие' }
	];

	function getJobStatusLabel(status: JobStatus): string {
		const labels: Record<string, string> = {
			Live: 'Активна',
			Draft: 'Черновик',
			Disabled: 'Закрыта',
			Expired: 'Истекла'
		};
		return labels[status] || status;
	}

	function getJobTypeLabel(type: string): string {
		const labels: Record<string, string> = {
			'full-time': 'Полная занятость',
			permanent: 'Постоянная',
			contract: 'Контракт',
			'part-time': 'Частичная занятость',
			internship: 'Стажировка',
			freelance: 'Фриланс'
		};
		return labels[type] || type;
	}

	// Update URL when filters change
	function updateFilters() {
		const params = new URLSearchParams();
		params.set('page', '1'); // Reset to page 1 on filter change

		if (selectedFilter !== 'all') {
			params.set('status', selectedFilter);
		}

		if (searchQuery.trim()) {
			params.set('search', searchQuery.trim());
		}

		goto(`?${params.toString()}`, { keepFocus: true, noScroll: true });
	}

	// Navigate to page
	function goToPage(pageNum: number) {
		const params = new URLSearchParams($page.url.searchParams);
		params.set('page', pageNum.toString());
		goto(`?${params.toString()}`, { keepFocus: true, noScroll: true });
	}

	function formatDate(dateString?: string): string {
		if (!dateString) return 'Н/Д';
		const date = new Date(dateString);
		return date.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	function getStatusVariant(status: JobStatus): 'success' | 'warning' | 'error' | 'neutral' {
		switch (status) {
			case 'Live':
				return 'success';
			case 'Draft':
				return 'neutral';
			case 'Disabled':
				return 'error';
			case 'Expired':
				return 'warning';
			default:
				return 'neutral';
		}
	}

	async function handleDelete(jobId: number, jobTitle: string) {
		if (!confirm(`Вы уверены, что хотите удалить «${jobTitle}»?`)) {
			return;
		}

		submittingAction = jobId;

		// Use fetch to submit delete action
		const formData = new FormData();
		formData.append('jobId', jobId.toString());

		try {
			const response = await fetch('?/delete', {
				method: 'POST',
				body: formData
			});

			const result = await response.json();

			if (result.type === 'success') {
				// Refresh the page data
				await invalidateAll();
			} else {
				alert(result.data?.error || 'Не удалось удалить вакансию');
			}
		} catch (err: any) {
			alert(err.message || 'Не удалось удалить вакансию');
		} finally {
			submittingAction = null;
		}
	}
</script>

<svelte:head>
	<title>Вакансии - PeelJobs Recruiter</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
		<div>
			<h1 class="text-2xl md:text-3xl font-bold text-black">Вакансии</h1>
			<p class="text-muted mt-1">Управление публикациями вакансий</p>
		</div>
		<div class="flex gap-3">
			<Button href="/dashboard/jobs/inactive/" variant="secondary">
				<Archive class="w-4 h-4" />
				Неактивные вакансии
			</Button>
			<Button href="/dashboard/jobs/new/">
				<Plus class="w-4 h-4" />
				Опубликовать вакансию
			</Button>
		</div>
	</div>

	<!-- Filters and Search -->
	<Card padding="md">
		<form onsubmit={(e) => { e.preventDefault(); updateFilters(); }} class="flex flex-col md:flex-row gap-4">
			<!-- Search -->
			<div class="flex-1 relative">
				<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
				<input
					type="text"
					bind:value={searchQuery}
					onchange={updateFilters}
					placeholder="Поиск по названию вакансии..."
					class="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
				/>
			</div>

			<!-- Filter -->
			<div class="flex items-center gap-3">
				<div class="relative">
					<Filter class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
					<select
						bind:value={selectedFilter}
						onchange={updateFilters}
						class="pl-9 pr-8 py-2 border border-border rounded-lg bg-white focus:ring-2 focus:ring-primary/20 focus:border-primary appearance-none cursor-pointer"
					>
						{#each filterOptions as option}
							<option value={option.value}>{option.label}</option>
						{/each}
					</select>
				</div>

				<div class="flex border border-border rounded-lg overflow-hidden">
					<button
						type="button"
						onclick={() => (viewMode = 'list')}
						class="px-3 py-2 {viewMode === 'list' ? 'bg-primary/10 text-primary' : 'bg-white text-muted'} hover:bg-surface transition-colors"
						aria-label="Список"
					>
						<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
							<path
								fill-rule="evenodd"
								d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
					<button
						type="button"
						onclick={() => (viewMode = 'grid')}
						class="px-3 py-2 {viewMode === 'grid' ? 'bg-primary/10 text-primary' : 'bg-white text-muted'} hover:bg-surface transition-colors"
						aria-label="Сетка"
					>
						<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
							<path
								d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM13 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2h-2z"
							/>
						</svg>
					</button>
				</div>
			</div>
		</form>
	</Card>

	<!-- Empty State -->
	{#if data.jobs.length === 0}
		<Card padding="lg" class="text-center">
			<Briefcase class="w-12 h-12 text-muted mx-auto mb-4" />
			<h3 class="text-lg font-semibold text-black mb-2">Вакансии не найдены</h3>
			<p class="text-muted mb-6">
				{searchQuery || selectedFilter !== 'all'
					? 'Попробуйте изменить фильтры или поисковый запрос'
					: 'Начните с публикации первой вакансии'}
			</p>
			<Button href="/dashboard/jobs/new/">
				<Plus class="w-4 h-4" />
				Опубликовать вакансию
			</Button>
		</Card>
	{:else if viewMode === 'list'}
		<!-- List View -->
		<Card padding="none">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-surface border-b border-border">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Детали вакансии
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Статус
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Опубликовано
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Истекает
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Статистика
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Действия
							</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-border">
						{#each data.jobs as job}
							<tr class="hover:bg-surface transition-colors">
								<td class="px-6 py-4">
									<div class="flex items-start gap-3">
										<div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
											<Briefcase class="w-5 h-5 text-primary" />
										</div>
										<div>
											<a
												href="/dashboard/jobs/{job.id}/{job.status === 'Draft' ? '' : 'applicants/'}"
												class="font-medium text-black hover:text-primary transition-colors"
											>
												{job.title}
											</a>
											<div class="flex items-center gap-3 mt-1 text-sm text-muted">
												<span>{job.company_name}</span>
												<span>•</span>
												<span class="flex items-center gap-1">
													<MapPin class="w-3 h-3" />
													{job.location_display}
												</span>
												<span>•</span>
												<span>{getJobTypeLabel(job.job_type)}</span>
											</div>
											{#if job.is_expiring_soon}
												<span class="inline-flex items-center gap-1 mt-2 px-2 py-1 bg-warning-light text-warning text-xs font-medium rounded">
													<Calendar class="w-3 h-3" />
													Истекает через {job.days_until_expiry} дн.
												</span>
											{/if}
										</div>
									</div>
								</td>
								<td class="px-6 py-4">
									<Badge variant={getStatusVariant(job.status)}>
										{getJobStatusLabel(job.status)}
									</Badge>
								</td>
								<td class="px-6 py-4 text-sm text-muted">
									{job.time_ago}
								</td>
								<td class="px-6 py-4 text-sm text-muted">
									{#if job.days_until_expiry !== null && job.days_until_expiry !== undefined}
										{job.days_until_expiry} дн. осталось
									{:else}
										Истекла
									{/if}
								</td>
								<td class="px-6 py-4">
									<div class="flex items-center gap-4 text-sm">
										<div class="flex items-center gap-1 text-muted">
											<Eye class="w-4 h-4" />
											{job.views_count.toLocaleString()}
										</div>
										<a
											href="/dashboard/jobs/{job.id}/applicants/"
											class="flex items-center gap-1 text-primary hover:text-primary-hover font-medium transition-colors"
										>
											<Users class="w-4 h-4" />
											{job.applicants_count}
										</a>
									</div>
								</td>
								<td class="px-6 py-4">
									<div class="flex items-center gap-2">
										{#if job.status === 'Draft'}
											<form method="POST" action="?/publish" use:enhance={() => {
												submittingAction = job.id;
												return async ({ update }) => {
													await update();
													submittingAction = null;
												};
											}}>
												<input type="hidden" name="jobId" value={job.id} />
												<button
													type="submit"
													disabled={submittingAction === job.id}
													class="p-2 text-success hover:bg-success-light rounded-lg transition-colors disabled:opacity-50"
													title="Опубликовать"
												>
													<Send class="w-4 h-4" />
												</button>
											</form>
										{/if}
										{#if job.status === 'Live'}
											<form method="POST" action="?/close" use:enhance={() => {
												submittingAction = job.id;
												return async ({ update }) => {
													await update();
													submittingAction = null;
												};
											}}>
												<input type="hidden" name="jobId" value={job.id} />
												<button
													type="submit"
													disabled={submittingAction === job.id}
													class="p-2 text-warning hover:bg-warning-light rounded-lg transition-colors disabled:opacity-50"
													title="Закрыть"
												>
													<Archive class="w-4 h-4" />
												</button>
											</form>
										{/if}
										{#if job.status === 'Draft'}
											<a
												href="/dashboard/jobs/{job.id}/edit/"
												class="p-2 text-muted hover:bg-surface rounded-lg transition-colors"
												title="Редактировать"
											>
												<Edit class="w-4 h-4" />
											</a>
										{/if}
										<a
											href="/dashboard/jobs/{job.id}/"
											class="p-2 text-muted hover:bg-surface rounded-lg transition-colors"
											title="Просмотр"
										>
											<ExternalLink class="w-4 h-4" />
										</a>
										<a
											href="/dashboard/jobs/new/?copy_from={job.id}"
											class="p-2 text-primary hover:bg-primary/10 rounded-lg transition-colors"
											title="Копировать вакансию"
										>
											<Copy class="w-4 h-4" />
										</a>
										{#if job.status === 'Draft'}
											<button
												onclick={() => handleDelete(job.id, job.title)}
												disabled={submittingAction === job.id}
												class="p-2 text-error hover:bg-error-light rounded-lg transition-colors disabled:opacity-50"
												title="Удалить"
											>
												<XCircle class="w-4 h-4" />
											</button>
										{/if}
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</Card>
	{:else}
		<!-- Grid View -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each data.jobs as job}
				<Card hover padding="md">
					<div class="flex items-start justify-between mb-4">
						<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
							<Briefcase class="w-6 h-6 text-primary" />
						</div>
						<Badge variant={getStatusVariant(job.status)}>
							{getJobStatusLabel(job.status)}
						</Badge>
					</div>

					<a
						href="/dashboard/jobs/{job.id}/{job.status === 'Draft' ? '' : 'applicants/'}"
						class="block mb-3"
					>
						<h3 class="text-lg font-semibold text-black hover:text-primary transition-colors line-clamp-2">
							{job.title}
						</h3>
					</a>

					<div class="space-y-2 text-sm text-muted mb-4">
						<div class="flex items-center gap-2">
							<MapPin class="w-4 h-4" />
							{job.location_display}
						</div>
						<div class="flex items-center gap-2">
							<Calendar class="w-4 h-4" />
							Опубликовано {job.time_ago}
						</div>
					</div>

					{#if job.is_expiring_soon}
						<div class="mb-4">
							<span class="inline-flex items-center gap-1 px-2 py-1 bg-warning-light text-warning text-xs font-medium rounded">
								<Calendar class="w-3 h-3" />
								Истекает через {job.days_until_expiry} дн.
							</span>
						</div>
					{/if}

					<div class="flex items-center justify-between mb-4 pt-4 border-t border-border">
						<div class="flex items-center gap-1 text-sm text-muted">
							<Eye class="w-4 h-4" />
							{job.views_count.toLocaleString()}
						</div>
						<a
							href="/dashboard/jobs/{job.id}/applicants/"
							class="flex items-center gap-1 text-sm text-primary hover:text-primary-hover font-medium transition-colors"
						>
							<Users class="w-4 h-4" />
							{job.applicants_count} откликов
						</a>
					</div>

					<div class="flex items-center gap-2">
						{#if job.status === 'Draft'}
							<form method="POST" action="?/publish" use:enhance class="flex-1">
								<input type="hidden" name="jobId" value={job.id} />
								<button
									type="submit"
									class="w-full inline-flex items-center justify-center gap-2 px-3 py-2 bg-success rounded-full text-sm font-medium text-white hover:opacity-90 transition-opacity"
								>
									<Send class="w-4 h-4" />
									Опубликовать
								</button>
							</form>
						{:else if job.status === 'Live'}
							<form method="POST" action="?/close" use:enhance class="flex-1">
								<input type="hidden" name="jobId" value={job.id} />
								<button
									type="submit"
									class="w-full inline-flex items-center justify-center gap-2 px-3 py-2 bg-warning rounded-full text-sm font-medium text-white hover:opacity-90 transition-opacity"
								>
									<Archive class="w-4 h-4" />
									Закрыть
								</button>
							</form>
						{/if}
						{#if job.status === 'Draft'}
							<Button href="/dashboard/jobs/{job.id}/edit/" variant="secondary" size="sm" class="flex-1">
								<Edit class="w-4 h-4" />
								Редактировать
							</Button>
						{/if}
						<Button href="/dashboard/jobs/{job.id}/" size="sm" class="flex-1">
							Просмотр
						</Button>
					</div>
				</Card>
			{/each}
		</div>
	{/if}

	<!-- Pagination -->
	{#if data.jobs.length > 0 && (data.next || data.previous)}
		<Card padding="md">
			<div class="flex items-center justify-between">
				<div class="text-sm text-muted">
					Показано {data.jobs.length} из {data.count} вакансий
				</div>
				<div class="flex items-center gap-2">
					<Button
						variant="secondary"
						size="sm"
						onclick={() => goToPage(data.currentPage - 1)}
						disabled={!data.previous}
					>
						Назад
					</Button>
					<span class="text-sm text-muted px-2">Страница {data.currentPage}</span>
					<Button
						variant="secondary"
						size="sm"
						onclick={() => goToPage(data.currentPage + 1)}
						disabled={!data.next}
					>
						Далее
					</Button>
				</div>
			</div>
		</Card>
	{/if}
</div>
