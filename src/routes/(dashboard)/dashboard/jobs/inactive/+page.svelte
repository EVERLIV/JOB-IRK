<script lang="ts">
	import { untrack } from 'svelte';
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import {
		Search,
		Filter,
		Eye,
		Users,
		Archive,
		XCircle,
		Calendar,
		MapPin,
		Briefcase,
		RotateCcw,
		Trash2,
		ArrowLeft,
		AlertCircle
	} from '@lucide/svelte';
	import { Button, Card, Badge } from '$lib/components/ui';
	import type { JobStatus } from '$lib/types';

	let { data } = $props();

	// Initialize filters from URL params (one-time snapshot, not reactive)
	let searchQuery = $state(untrack(() => data.filters.search));
	let selectedFilter = $state(untrack(() => data.filters.status));
	let submittingAction = $state<number | null>(null);

	const filterOptions = [
		{ value: 'all', label: 'Все неактивные' },
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
		return labels[type] || type.replace('-', ' ');
	}

	function updateFilters() {
		const params = new URLSearchParams();
		params.set('page', '1');

		if (selectedFilter !== 'all') {
			params.set('status', selectedFilter);
		}

		if (searchQuery.trim()) {
			params.set('search', searchQuery.trim());
		}

		goto(`?${params.toString()}`, { keepFocus: true, noScroll: true });
	}

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

	function getStatusVariant(status: JobStatus): 'error' | 'warning' | 'neutral' {
		switch (status) {
			case 'Disabled':
				return 'error';
			case 'Expired':
				return 'warning';
			default:
				return 'neutral';
		}
	}
</script>

<svelte:head>
	<title>Неактивные вакансии - PeelJobs</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
		<div class="flex items-center gap-4">
			<a
				href="/dashboard/jobs/"
				class="p-2 hover:bg-surface rounded-lg transition-colors"
				title="Вернуться ко всем вакансиям"
			>
				<ArrowLeft class="w-5 h-5 text-muted" />
			</a>
			<div>
				<h1 class="text-2xl md:text-3xl font-bold text-black">Неактивные вакансии</h1>
				<p class="text-muted mt-1">Закрытые и просроченные публикации</p>
			</div>
		</div>
	</div>

	<!-- Stats Cards -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
		<Card padding="md">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-surface rounded-lg flex items-center justify-center">
					<Archive class="w-5 h-5 text-muted" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.stats.total}</div>
					<div class="text-sm text-muted">Всего неактивных</div>
				</div>
			</div>
		</Card>

		<Card padding="md">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-error-light rounded-lg flex items-center justify-center">
					<XCircle class="w-5 h-5 text-error" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.stats.disabled}</div>
					<div class="text-sm text-muted">Закрытые</div>
				</div>
			</div>
		</Card>

		<Card padding="md">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-warning-light rounded-lg flex items-center justify-center">
					<AlertCircle class="w-5 h-5 text-warning" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.stats.expired}</div>
					<div class="text-sm text-muted">Просроченные</div>
				</div>
			</div>
		</Card>
	</div>

	<!-- Filters -->
	<Card padding="md">
		<form
			onsubmit={(e) => {
				e.preventDefault();
				updateFilters();
			}}
			class="flex flex-col md:flex-row gap-4"
		>
			<!-- Search -->
			<div class="flex-1 relative">
				<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
				<input
					type="text"
					bind:value={searchQuery}
					onchange={updateFilters}
					placeholder="Поиск по неактивным вакансиям..."
					class="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
				/>
			</div>

			<!-- Status Filter -->
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
		</form>
	</Card>

	<!-- Jobs List -->
	{#if data.jobs.length === 0}
		<Card padding="lg" class="text-center">
			<Archive class="w-12 h-12 text-muted mx-auto mb-4" />
			<h3 class="text-lg font-semibold text-black mb-2">Неактивные вакансии не найдены</h3>
			<p class="text-muted">
				{searchQuery || selectedFilter !== 'all'
					? 'Попробуйте изменить фильтры'
					: 'Здесь появятся все ваши закрытые и просроченные вакансии'}
			</p>
		</Card>
	{:else}
		<div class="grid grid-cols-1 gap-4">
			{#each data.jobs as job}
				<Card hover padding="md">
					<div class="flex items-start justify-between gap-4">
						<!-- Job Info -->
						<div class="flex-1 min-w-0">
							<div class="flex items-center gap-3 mb-2">
								<h3 class="text-lg font-semibold text-black truncate">{job.title}</h3>
								<Badge variant={getStatusVariant(job.status)}>
									{getJobStatusLabel(job.status)}
								</Badge>
							</div>

							<div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm text-muted mb-3">
								<div class="flex items-center gap-2">
									<Briefcase class="w-4 h-4" />
									<span>{getJobTypeLabel(job.job_type)}</span>
								</div>
								<div class="flex items-center gap-2">
									<MapPin class="w-4 h-4" />
									<span>{job.location_display || 'Удалённо'}</span>
								</div>
								<div class="flex items-center gap-2">
									<Calendar class="w-4 h-4" />
									<span>Опубликовано {formatDate(job.published_on)}</span>
								</div>
							</div>

							<div class="flex items-center gap-4 text-sm">
								<div class="flex items-center gap-2 text-muted">
									<Users class="w-4 h-4" />
									<span>{job.applicants_count} откликов</span>
								</div>
								<div class="flex items-center gap-2 text-muted">
									<Eye class="w-4 h-4" />
									<span>{job.views_count} просмотров</span>
								</div>
							</div>
						</div>

						<!-- Actions -->
						<div class="flex flex-col gap-2">
							<Button href="/dashboard/jobs/{job.id}/" variant="secondary" size="sm">
								<Eye class="w-4 h-4" />
								Открыть
							</Button>

							<form
								method="POST"
								action="?/reactivate"
								use:enhance={() => {
									submittingAction = job.id;
									return async ({ result }) => {
										submittingAction = null;
										if (result.type === 'success') {
											await invalidateAll();
										}
									};
								}}
							>
								<input type="hidden" name="jobId" value={job.id} />
								<Button type="submit" size="sm" disabled={submittingAction === job.id} class="w-full">
									<RotateCcw class="w-4 h-4" />
									Восстановить
								</Button>
							</form>

							<form
								method="POST"
								action="?/delete"
								use:enhance={() => {
									if (!confirm('Вы уверены, что хотите навсегда удалить эту вакансию?')) {
										return () => {};
									}
									submittingAction = job.id;
									return async ({ result }) => {
										submittingAction = null;
										if (result.type === 'success') {
											await invalidateAll();
										}
									};
								}}
							>
								<input type="hidden" name="jobId" value={job.id} />
								<button
									type="submit"
									disabled={submittingAction === job.id}
									class="w-full inline-flex items-center justify-center gap-2 px-4 py-2 border border-error/30 text-error rounded-full hover:bg-error-light transition-colors text-sm font-medium disabled:opacity-50"
								>
									<Trash2 class="w-4 h-4" />
									Удалить
								</button>
							</form>
						</div>
					</div>
				</Card>
			{/each}
		</div>

		<!-- Pagination -->
		{#if data.count > 20}
			<Card padding="sm">
				<div class="flex items-center justify-between">
					<div class="text-sm text-muted">
						Страница <span class="font-medium text-black">{data.currentPage}</span> из
						<span class="font-medium text-black">{Math.ceil(data.count / 20)}</span>
					</div>

					<div class="flex gap-2">
						{#if data.previous}
							<Button variant="secondary" size="sm" onclick={() => goToPage(data.currentPage - 1)}>
								Назад
							</Button>
						{/if}

						{#if data.next}
							<Button variant="secondary" size="sm" onclick={() => goToPage(data.currentPage + 1)}>
								Далее
							</Button>
						{/if}
					</div>
				</div>
			</Card>
		{/if}
	{/if}
</div>
