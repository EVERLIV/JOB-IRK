<script lang="ts">
	import {
		ArrowLeft,
		Briefcase,
		MapPin,
		Calendar,
		DollarSign,
		Users,
		Eye,
		Clock,
		Building,
		Globe,
		Mail,
		Edit,
		Share2,
		ExternalLink,
		TrendingUp,
		Target,
		Bell,
		BellOff,
		Copy
	} from '@lucide/svelte';
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { Button, Card, Badge } from '$lib/components/ui';
	import type { JobStatus } from '$lib/types';

	let { data } = $props();
	let togglingNotifications = $state(false);

	function formatDate(dateString?: string): string {
		if (!dateString) return 'Н/Д';
		const date = new Date(dateString);
		return date.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	function formatSalary(min: number, max: number, type: string): string {
		if (!min && !max) return 'Не указана';
		const minStr = min ? `₹${(min / 100000).toFixed(1)}L` : '';
		const maxStr = max ? `₹${(max / 100000).toFixed(1)}L` : '';
		const range = minStr && maxStr ? `${minStr} - ${maxStr}` : minStr || maxStr;
		return `${range} в ${type === 'Month' ? 'месяц' : 'год'}`;
	}

	function getJobStatusLabel(status: JobStatus): string {
		const labels: Record<string, string> = {
			Live: 'Активна',
			Draft: 'Черновик',
			Disabled: 'Закрыта',
			Expired: 'Истекла'
		};
		return labels[status] || status;
	}

	function getWorkModeLabel(mode: string): string {
		const labels: Record<string, string> = {
			'in-office': 'В офисе',
			remote: 'Удалённо',
			hybrid: 'Гибрид'
		};
		return labels[mode] || mode.replace('-', ' ');
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
</script>

<svelte:head>
	<title>{data.job.title} - Детали вакансии - Truddy.ru</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center gap-4">
		<a
			href="/dashboard/jobs/"
			class="p-2 hover:bg-surface rounded-lg transition-colors"
			title="Вернуться к вакансиям"
		>
			<ArrowLeft class="w-5 h-5" />
		</a>
		<div class="flex-1">
			<div class="flex items-center gap-3 mb-2">
				<h1 class="text-2xl md:text-3xl font-bold text-black">{data.job.title}</h1>
				<Badge variant={getStatusVariant(data.job.status)}>{getJobStatusLabel(data.job.status)}</Badge>
			</div>
			<p class="text-muted">{data.job.company_name || 'Ваша компания'}</p>
		</div>
	</div>

	<!-- Stats Cards -->
	<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
		<div class="bg-white rounded-lg border border-border p-4">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
					<Users class="w-5 h-5 text-primary" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.totalApplicants}</div>
					<div class="text-sm text-muted">Всего кандидатов</div>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-4">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-warning-light rounded-lg flex items-center justify-center">
					<Clock class="w-5 h-5 text-warning" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.applicantsStats.pending}</div>
					<div class="text-sm text-muted">На рассмотрении</div>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-4">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
					<Users class="w-5 h-5 text-primary" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.applicantsStats.shortlisted}</div>
					<div class="text-sm text-muted">Отобрано</div>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-4">
			<div class="flex items-center gap-3">
				<div class="w-10 h-10 bg-success-light rounded-lg flex items-center justify-center">
					<Users class="w-5 h-5 text-success" />
				</div>
				<div>
					<div class="text-2xl font-bold text-black">{data.applicantsStats.selected}</div>
					<div class="text-sm text-muted">Нанято</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Analytics Section (30-day period) -->
	{#if data.analytics}
		<div class="bg-white rounded-lg border border-border p-6">
			<h2 class="text-lg font-semibold text-black mb-4">Аналитика откликов (за 30 дней)</h2>
			<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
				<div class="text-center">
					<div class="text-2xl font-bold text-primary">{data.analytics.metrics.total_applications}</div>
					<div class="text-sm text-muted mt-1">Всего откликов</div>
				</div>
				<div class="text-center">
					<div class="text-2xl font-bold text-purple-600">{data.analytics.pipeline.pending}</div>
					<div class="text-sm text-muted mt-1">На рассмотрении</div>
				</div>
				<div class="text-center">
					<div class="text-2xl font-bold text-success">{data.analytics.pipeline.hired}</div>
					<div class="text-sm text-muted mt-1">Нанято</div>
				</div>
				<div class="text-center">
					<div class="flex items-center justify-center gap-1">
						<Target class="w-5 h-5 text-success" />
						<div class="text-2xl font-bold text-success">{data.analytics.pipeline.conversion_rate}%</div>
					</div>
					<div class="text-sm text-muted mt-1">Конверсия</div>
				</div>
			</div>

			{#if data.analytics.metrics.avg_per_day > 0}
				<div class="mt-4 pt-4 border-t border-border">
					<div class="flex items-center justify-center gap-2 text-sm text-muted">
						<TrendingUp class="w-4 h-4 text-primary" />
						<span>В среднем <span class="font-semibold text-black">{data.analytics.metrics.avg_per_day}</span> откликов в день</span>
					</div>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Action Buttons -->
	<div class="flex flex-wrap gap-3">
		<a
			href="/dashboard/jobs/{data.job.id}/applicants/"
			class="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition-colors"
		>
			<Users class="w-4 h-4" />
			Кандидаты
		</a>

		{#if data.job.status === 'Draft'}
			<a
				href="/dashboard/jobs/{data.job.id}/edit/"
				class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors"
			>
				<Edit class="w-4 h-4" />
				Редактировать
			</a>
		{/if}

		<!-- Email Notifications Toggle -->
		<form method="POST" action="?/toggleNotifications" use:enhance={() => {
			togglingNotifications = true;
			return async ({ result }) => {
				togglingNotifications = false;
				if (result.type === 'success') {
					await invalidateAll();
				}
			};
		}}>
			<button
				type="submit"
				disabled={togglingNotifications}
				class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
				title={data.job.send_email_notifications ? 'Отключить email-уведомления' : 'Включить email-уведомления'}
			>
				{#if data.job.send_email_notifications}
					<Bell class="w-4 h-4 text-success" />
					<span>Уведомления вкл.</span>
				{:else}
					<BellOff class="w-4 h-4 text-muted" />
					<span>Уведомления выкл.</span>
				{/if}
			</button>
		</form>

		<a
			href="/dashboard/jobs/{data.job.id}/preview/"
			class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors"
		>
			<Eye class="w-4 h-4" />
			Предпросмотр
		</a>

		<a
			href="/dashboard/jobs/new/?copy_from={data.job.id}"
			class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors"
		>
			<Copy class="w-4 h-4" />
			Копировать вакансию
		</a>

		<button
			class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors"
		>
			<Share2 class="w-4 h-4" />
			Поделиться
		</button>

		{#if data.job.status === 'Live' || data.job.status === 'Published'}
			<a
				href="/jobs/{data.job.id}/"
				target="_blank"
				class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors"
			>
				<ExternalLink class="w-4 h-4" />
				Публичная страница
			</a>
		{/if}
	</div>

	<!-- Job Details -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<!-- Main Content -->
		<div class="lg:col-span-2 space-y-6">
			<!-- Job Information -->
			<div class="bg-white rounded-lg border border-border p-6">
				<h2 class="text-lg font-semibold text-black mb-4">Информация о вакансии</h2>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<div>
						<div class="text-sm font-medium text-muted mb-1">Тип занятости</div>
						<div class="text-black">{getJobTypeLabel(data.job.job_type)}</div>
					</div>

					<div>
						<div class="text-sm font-medium text-muted mb-1">Формат работы</div>
						<div class="text-black">{getWorkModeLabel(data.job.work_mode)}</div>
					</div>

					<div>
						<div class="text-sm font-medium text-muted mb-1">Опыт</div>
						<div class="text-black">
							{#if data.job.fresher}
								Без опыта
							{:else}
								{data.job.min_year}–{data.job.max_year} лет
							{/if}
						</div>
					</div>

					<div>
						<div class="text-sm font-medium text-muted mb-1">Вакансий</div>
						<div class="text-black">{data.job.vacancies}</div>
					</div>

					<div>
						<div class="text-sm font-medium text-muted mb-1">Зарплата</div>
						<div class="text-black">
							{formatSalary(data.job.min_salary, data.job.max_salary, data.job.salary_type)}
						</div>
					</div>

					{#if data.job.seniority_level}
						<div>
							<div class="text-sm font-medium text-muted mb-1">Уровень должности</div>
							<div class="text-black capitalize">{data.job.seniority_level}</div>
						</div>
					{/if}
				</div>
			</div>

			<!-- Description -->
			<div class="bg-white rounded-lg border border-border p-6">
				<h2 class="text-lg font-semibold text-black mb-4">Описание вакансии</h2>
				<div class="prose prose-sm max-w-none text-muted">
					{@html data.job.description}
				</div>
			</div>

			<!-- Skills -->
			{#if data.job.skills && data.job.skills.length > 0}
				<div class="bg-white rounded-lg border border-border p-6">
					<h2 class="text-lg font-semibold text-black mb-4">Требуемые навыки</h2>
					<div class="flex flex-wrap gap-2">
						{#each data.job.skills as skill}
							<span class="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
								{skill.name}
							</span>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Qualifications -->
			{#if data.job.qualifications && data.job.qualifications.length > 0}
				<div class="bg-white rounded-lg border border-border p-6">
					<h2 class="text-lg font-semibold text-black mb-4">Образование</h2>
					<div class="flex flex-wrap gap-2">
						{#each data.job.qualifications as qual}
							<span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
								{qual.name}
							</span>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Benefits -->
			{#if data.job.benefits && data.job.benefits.length > 0}
				<div class="bg-white rounded-lg border border-border p-6">
					<h2 class="text-lg font-semibold text-black mb-4">Льготы и бонусы</h2>
					<ul class="space-y-2">
						{#each data.job.benefits as benefit}
							<li class="flex items-center gap-2 text-muted">
								<div class="w-1.5 h-1.5 bg-success rounded-full"></div>
								{benefit}
							</li>
						{/each}
					</ul>
				</div>
			{/if}
		</div>

		<!-- Sidebar -->
		<div class="space-y-6">
			<!-- Job Status -->
			<div class="bg-white rounded-lg border border-border p-6">
				<h3 class="text-sm font-semibold text-black mb-4">Статус вакансии</h3>
				<div class="space-y-3 text-sm">
					<div class="flex items-center justify-between">
						<span class="text-muted">Статус</span>
						<Badge variant={getStatusVariant(data.job.status)} size="sm">{getJobStatusLabel(data.job.status)}</Badge>
					</div>
					<div class="flex items-center justify-between">
						<span class="text-muted">Опубликовано</span>
						<span class="text-black">{data.job.time_ago}</span>
					</div>
					<div class="flex items-center justify-between">
						<span class="text-muted">Истекает</span>
						<span class="text-black">
						{#if data.job.published_on}
							{formatDate(new Date(new Date(data.job.published_on).getTime() + 30*24*60*60*1000).toISOString())}
						{:else}
							Недоступно
						{/if}
					</span>
					</div>
					{#if data.job.days_until_expiry !== null}
						<div class="flex items-center justify-between">
							<span class="text-muted">Дней осталось</span>
							<span class="text-black font-medium">{data.job.days_until_expiry}</span>
						</div>
					{/if}
				</div>
			</div>

			<!-- Locations -->
			{#if data.job.locations && data.job.locations.length > 0}
				<div class="bg-white rounded-lg border border-border p-6">
					<h3 class="text-sm font-semibold text-black mb-4 flex items-center gap-2">
						<MapPin class="w-4 h-4" />
						Локации
					</h3>
					<div class="space-y-2">
						{#each data.job.locations as location}
							<div class="text-sm text-muted">
								{location.name}, {location.state || ''}
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Industries -->
			{#if data.job.industries && data.job.industries.length > 0}
				<div class="bg-white rounded-lg border border-border p-6">
					<h3 class="text-sm font-semibold text-black mb-4 flex items-center gap-2">
						<Building class="w-4 h-4" />
						Отрасли
					</h3>
					<div class="flex flex-wrap gap-2">
						{#each data.job.industries as industry}
							<span class="text-sm px-2 py-1 bg-surface text-muted rounded">
								{industry.name}
							</span>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Company Info -->
			{#if data.job.company_description}
				<div class="bg-white rounded-lg border border-border p-6">
					<h3 class="text-sm font-semibold text-black mb-4">О компании</h3>
					<p class="text-sm text-muted leading-relaxed">{data.job.company_description}</p>
				</div>
			{/if}
		</div>
	</div>
</div>
