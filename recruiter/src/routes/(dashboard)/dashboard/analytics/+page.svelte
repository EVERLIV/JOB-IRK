<script lang="ts">
	import { goto } from '$app/navigation';
	import {
		TrendingUp,
		TrendingDown,
		Users,
		Briefcase,
		Clock,
		Target,
		Download,
		CheckCircle,
		UserCheck,
		XCircle
	} from '@lucide/svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	const { analytics, period } = data;

	const periodOptions = [
		{ value: '7d', label: 'Последние 7 дней' },
		{ value: '30d', label: 'Последние 30 дней' },
		{ value: '90d', label: 'Последние 90 дней' }
	];

	function changePeriod(newPeriod: string) {
		goto(`/dashboard/analytics/?period=${newPeriod}`);
	}

	// Build overview metrics from real data
	$: overviewMetrics = [
		{
			label: 'Всего откликов',
			value: analytics.overview.total_applications.toLocaleString(),
			change: analytics.overview.trend,
			isPositive: analytics.overview.trend.startsWith('+'),
			icon: Users
		},
		{
			label: 'Активные вакансии',
			value: analytics.overview.total_jobs.toString(),
			change: `${analytics.overview.avg_per_day} откл./день`,
			isPositive: true,
			icon: Briefcase
		},
		{
			label: 'Нанято',
			value: analytics.pipeline.hired.toString(),
			change: `${analytics.pipeline.conversion_rate}% конверсия`,
			isPositive: true,
			icon: CheckCircle
		},
		{
			label: 'На рассмотрении',
			value: analytics.pipeline.pending.toString(),
			change: 'Требуют внимания',
			isPositive: false,
			icon: Clock
		}
	];

	// Pipeline metrics with percentages
	$: pipelineMetrics = [
		{
			stage: 'Новые отклики',
			count: analytics.overview.total_applications,
			percentage: 100
		},
		{
			stage: 'Отобраны',
			count: analytics.pipeline.shortlisted,
			percentage: Math.round((analytics.pipeline.shortlisted / analytics.overview.total_applications) * 100)
		},
		{
			stage: 'Нанято',
			count: analytics.pipeline.hired,
			percentage: Math.round((analytics.pipeline.hired / analytics.overview.total_applications) * 100)
		},
		{
			stage: 'Отклонены',
			count: analytics.pipeline.rejected,
			percentage: Math.round((analytics.pipeline.rejected / analytics.overview.total_applications) * 100)
		}
	];

	// Sort peak days
	const dayOrder = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
	const dayNamesRu: Record<string, string> = {
		monday: 'Понедельник',
		tuesday: 'Вторник',
		wednesday: 'Среда',
		thursday: 'Четверг',
		friday: 'Пятница',
		saturday: 'Суббота',
		sunday: 'Воскресенье'
	};
	$: peakDaysArray = dayOrder.map(day => ({
		day: dayNamesRu[day],
		count: analytics.peak_days[day] || 0
	}));
</script>

<svelte:head>
	<title>Аналитика - Truddy.ru Recruiter</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
		<div>
			<h1 class="text-2xl md:text-3xl font-bold text-black">Аналитика откликов</h1>
			<p class="text-muted mt-1">Отслеживайте эффективность найма и аналитику</p>
		</div>
		<div class="flex items-center gap-3">
			<select
				value={period}
				onchange={(e) => changePeriod(e.currentTarget.value)}
				class="px-4 py-2 border border-border rounded-lg bg-white focus:ring-2 focus:ring-primary/20 focus:border-primary"
			>
				{#each periodOptions as option}
					<option value={option.value}>{option.label}</option>
				{/each}
			</select>
			<button
				class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border rounded-lg text-sm font-medium text-muted hover:bg-surface transition-colors"
			>
				<Download class="w-4 h-4" />
				Экспорт отчёта
			</button>
		</div>
	</div>

	<!-- Overview Metrics -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		{#each overviewMetrics as metric}
			<div class="bg-white rounded-lg border border-border p-6">
				<div class="flex items-start justify-between">
					<div class="flex-1">
						<p class="text-sm font-medium text-muted">{metric.label}</p>
						<p class="text-3xl font-bold text-black mt-2">{metric.value}</p>
						<div class="flex items-center gap-1 mt-2">
							{#if metric.isPositive && metric.change.includes('%')}
								<TrendingUp class="w-4 h-4 text-success" />
								<span class="text-sm font-medium text-success">{metric.change}</span>
							{:else if !metric.isPositive && metric.change.includes('%')}
								<TrendingDown class="w-4 h-4 text-error" />
								<span class="text-sm font-medium text-error">{metric.change}</span>
							{:else}
								<span class="text-sm text-muted">{metric.change}</span>
							{/if}
						</div>
					</div>
					<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
						<metric.icon class="w-6 h-6 text-primary" />
					</div>
				</div>
			</div>
		{/each}
	</div>

	<!-- Job Performance -->
	<div class="bg-white rounded-lg border border-border">
		<div class="p-6 border-b border-border">
			<h2 class="text-lg font-semibold text-black">Эффективность вакансий</h2>
		</div>
		{#if analytics.job_performance.length > 0}
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-surface border-b border-border">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Название вакансии
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Отклики
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								На рассмотрении
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Отобраны
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Нанято
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Конверсия
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">
								Сред./день
							</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-border">
						{#each analytics.job_performance as job}
							<tr class="hover:bg-surface">
								<td class="px-6 py-4">
									<a href="/dashboard/jobs/{job.job_id}/" class="text-sm font-medium text-primary hover:text-primary">
										{job.job_title}
									</a>
								</td>
								<td class="px-6 py-4 text-sm text-black font-medium">
									{job.total_applications}
								</td>
								<td class="px-6 py-4 text-sm text-muted">
									{job.pending}
								</td>
								<td class="px-6 py-4 text-sm text-muted">
									{job.shortlisted}
								</td>
								<td class="px-6 py-4 text-sm text-success font-medium">
									{job.hired}
								</td>
								<td class="px-6 py-4 text-sm">
									<div class="flex items-center gap-2">
										<Target class="w-4 h-4 text-success" />
										{job.conversion_rate}%
									</div>
								</td>
								<td class="px-6 py-4 text-sm text-muted">
									{job.avg_applications_per_day}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="p-12 text-center">
				<Briefcase class="w-12 h-12 text-muted mx-auto mb-3" />
				<p class="text-muted">Нет активных вакансий за этот период</p>
			</div>
		{/if}
	</div>

	<!-- Pipeline & Peak Days Grid -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<!-- Application Pipeline -->
		<div class="bg-white rounded-lg border border-border">
			<div class="p-6 border-b border-border">
				<h2 class="text-lg font-semibold text-black">Воронка откликов</h2>
			</div>
			<div class="p-6">
				<div class="space-y-4">
					{#each pipelineMetrics as stage}
						<div>
							<div class="flex items-center justify-between mb-2">
								<span class="text-sm font-medium text-black">{stage.stage}</span>
								<span class="text-sm text-muted">{stage.count}</span>
							</div>
							<div class="w-full bg-surface rounded-full h-2">
								<div
									class="bg-primary h-2 rounded-full transition-all"
									style="width: {stage.percentage}%"
								></div>
							</div>
							<div class="text-xs text-muted mt-1">{stage.percentage}% от общего</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Peak Days -->
		<div class="bg-white rounded-lg border border-border">
			<div class="p-6 border-b border-border">
				<h2 class="text-lg font-semibold text-black">Отклики по дням недели</h2>
			</div>
			<div class="p-6">
				<div class="space-y-4">
					{#each peakDaysArray as day}
						{@const maxCount = Math.max(...peakDaysArray.map(d => d.count))}
						{@const percentage = maxCount > 0 ? (day.count / maxCount) * 100 : 0}
						<div>
							<div class="flex items-center justify-between mb-2">
								<span class="text-sm font-medium text-black">{day.day}</span>
								<span class="text-sm text-muted">{day.count}</span>
							</div>
							<div class="w-full bg-surface rounded-full h-2">
								<div
									class="bg-success h-2 rounded-full transition-all"
									style="width: {percentage}%"
								></div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>

	<!-- Key Insights -->
	<div class="bg-white rounded-lg border border-border">
		<div class="p-6 border-b border-border">
			<h2 class="text-lg font-semibold text-black">Ключевые выводы</h2>
		</div>
		<div class="p-6">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				{#if analytics.pipeline.pending > 0}
					<div class="flex gap-4">
						<div class="w-12 h-12 rounded-lg bg-warning-light flex items-center justify-center flex-shrink-0">
							<Clock class="w-6 h-6 text-warning" />
						</div>
						<div>
							<h3 class="font-semibold text-black mb-1">Требуются действия</h3>
							<p class="text-sm text-muted">
								{analytics.pipeline.pending} откликов ожидают рассмотрения.
							</p>
						</div>
					</div>
				{/if}

				{#if analytics.pipeline.conversion_rate > 3}
					<div class="flex gap-4">
						<div class="w-12 h-12 rounded-lg bg-success-light flex items-center justify-center flex-shrink-0">
							<Target class="w-6 h-6 text-success" />
						</div>
						<div>
							<h3 class="font-semibold text-black mb-1">Высокая конверсия</h3>
							<p class="text-sm text-muted">
								{analytics.pipeline.conversion_rate}% конверсия от откликов до найма.
							</p>
						</div>
					</div>
				{/if}

				{#if analytics.overview.avg_per_day > 0}
					<div class="flex gap-4">
						<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
							<TrendingUp class="w-6 h-6 text-primary" />
						</div>
						<div>
							<h3 class="font-semibold text-black mb-1">Скорость откликов</h3>
							<p class="text-sm text-muted">
								В среднем {analytics.overview.avg_per_day} откликов в день.
							</p>
						</div>
					</div>
				{/if}

				{#if analytics.pipeline.shortlisted > 0}
					<div class="flex gap-4">
						<div class="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center flex-shrink-0">
							<UserCheck class="w-6 h-6 text-purple-600" />
						</div>
						<div>
							<h3 class="font-semibold text-black mb-1">Активная воронка</h3>
							<p class="text-sm text-muted">
								{analytics.pipeline.shortlisted} квалифицированных кандидатов в воронке.
							</p>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
