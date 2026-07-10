<script lang="ts">
	import { untrack } from 'svelte';
	import {
		Building2,
		Upload,
		Globe,
		MapPin,
		Save,
		CheckCircle,
		XCircle
	} from '@lucide/svelte';
	import { enhance } from '$app/forms';
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();

	// Form data initialized from loaded company data (one-time snapshot, not reactive)
	let formData = $state(untrack(() => ({
		companyName: data.company?.name || '',
		logo: data.company?.logo_url || null as string | null,
		companySize: data.company?.size || '1-10',
		website: data.company?.website || '',
		about: data.company?.profile || '',
		primaryEmail: data.company?.email || '',
		phone: data.company?.phone_number || '',
		address: data.company?.address || ''
	})));

	const companySizes = [
		'1-10',
		'11-20',
		'21-50',
		'50-200',
		'200+'
	];

	let saving = $state(false);
	let showSuccessMessage = $state(false);
	let showErrorMessage = $state(false);

	// Watch for form submission result
	$effect(() => {
		if (form?.success) {
			showSuccessMessage = true;
			saving = false;
			// Update form data with returned company data
			if (form.company) {
				formData.companyName = form.company.name;
				formData.companySize = form.company.size;
				formData.website = form.company.website || '';
				formData.about = form.company.profile || '';
				formData.primaryEmail = form.company.email || '';
				formData.phone = form.company.phone_number || '';
				formData.address = form.company.address || '';
				formData.logo = form.company.logo_url || null;
			}
			setTimeout(() => {
				showSuccessMessage = false;
			}, 5000);
		} else if (form?.success === false) {
			showErrorMessage = true;
			saving = false;
			setTimeout(() => {
				showErrorMessage = false;
			}, 5000);
		}
	});

	function handleLogoUpload(event: Event) {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = (e) => {
				formData.logo = e.target?.result as string;
			};
			reader.readAsDataURL(file);
		}
	}

	function calculateCompleteness(): number {
		const fields = [
			formData.companyName,
			formData.logo,
			formData.companySize,
			formData.website,
			formData.about,
			formData.primaryEmail
		];
		const completed = fields.filter((f) => f && f.toString().trim() !== '').length;
		return Math.round((completed / fields.length) * 100);
	}

	let completeness = $derived(calculateCompleteness());
	let isAdmin = $derived(data.user?.is_admin === true);
</script>

<svelte:head>
	<title>Профиль компании - Truddy.ru Recruiter</title>
</svelte:head>

<div class="max-w-4xl space-y-6">
	<!-- Success/Error Messages -->
	{#if showSuccessMessage}
		<div class="bg-success-light border border-success/30 rounded-lg p-4 flex items-start gap-3">
			<CheckCircle class="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
			<div class="flex-1">
				<h3 class="text-sm font-medium text-success">Успех!</h3>
				<p class="text-sm text-success mt-1">{form?.message || 'Профиль компании успешно обновлён'}</p>
			</div>
		</div>
	{/if}

	{#if showErrorMessage}
		<div class="bg-error-light border border-error/30 rounded-lg p-4 flex items-start gap-3">
			<XCircle class="w-5 h-5 text-error flex-shrink-0 mt-0.5" />
			<div class="flex-1">
				<h3 class="text-sm font-medium text-error">Ошибка</h3>
				<p class="text-sm text-error mt-1">{form?.error || 'Не удалось обновить профиль компании'}</p>
			</div>
		</div>
	{/if}

	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
		<div>
			<h1 class="text-2xl md:text-3xl font-bold text-black">Профиль компании</h1>
			<p class="text-muted mt-1">Управляйте публичной информацией о вашей компании</p>
			{#if !isAdmin}
				<p class="text-sm text-amber-600 mt-1">⚠️ Только администраторы компании могут редактировать профиль</p>
			{/if}
		</div>
		{#if isAdmin}
			<a
				href="/dashboard/company/microsite/"
				class="inline-flex items-center gap-2 px-4 py-2 border border-border text-muted rounded-lg hover:bg-surface transition-colors text-sm font-medium"
			>
				<Globe class="w-4 h-4" />
				Управление микросайтом
			</a>
		{/if}
	</div>

	<!-- Profile Completeness -->
	<div class="bg-white rounded-lg border border-border p-6">
		<div class="flex items-center justify-between mb-3">
			<h3 class="text-sm font-medium text-black">Заполненность профиля</h3>
			<span class="text-sm font-semibold text-primary">{completeness}%</span>
		</div>
		<div class="w-full bg-surface rounded-full h-2">
			<div class="bg-primary h-2 rounded-full transition-all" style="width: {completeness}%"></div>
		</div>
		<p class="text-xs text-muted mt-2">
			Заполните профиль, чтобы привлечь более квалифицированных кандидатов
		</p>
	</div>

	<!-- Company Logo -->
	<div class="bg-white rounded-lg border border-border p-6">
		<h2 class="text-lg font-semibold text-black mb-4 flex items-center gap-2">
			<Building2 class="w-5 h-5" />
			Логотип компании
		</h2>
		<div class="flex items-start gap-6">
			<div
				class="w-32 h-32 rounded-lg border-2 border-dashed border-border flex items-center justify-center bg-surface overflow-hidden"
			>
				{#if formData.logo}
					<img src={formData.logo} alt="Логотип компании" class="w-full h-full object-cover" />
				{:else}
					<Building2 class="w-12 h-12 text-muted" />
				{/if}
			</div>
			<div class="flex-1">
				<label
					class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border rounded-lg text-sm font-medium text-muted hover:bg-surface transition-colors cursor-pointer"
				>
					<Upload class="w-4 h-4" />
					Загрузить логотип
					<input type="file" accept="image/*" onchange={handleLogoUpload} class="hidden" />
				</label>
				<p class="text-sm text-muted mt-2">
					Рекомендуется: квадратное изображение, минимум 200×200 px. Максимальный размер файла: 2 МБ.
				</p>
			</div>
		</div>
	</div>

	<!-- Company Form -->
	<form
		method="POST"
		action="?/updateCompany"
		use:enhance={() => {
			saving = true;
			return async ({ update }) => {
				await update();
			};
		}}
	>
		<!-- Basic Information -->
		<div class="bg-white rounded-lg border border-border p-6">
			<h2 class="text-lg font-semibold text-black mb-6">Основная информация</h2>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div class="md:col-span-2">
					<label for="company-name" class="block text-sm font-medium text-muted mb-2">
						Название компании <span class="text-error">*</span>
					</label>
					<input
						id="company-name"
						type="text"
						name="name"
						bind:value={formData.companyName}
						placeholder="Название вашей компании"
						required
						disabled={!isAdmin}
						class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
					/>
				</div>

				<div>
					<label for="company-size" class="block text-sm font-medium text-muted mb-2">
						Размер компании <span class="text-error">*</span>
					</label>
					<select
						id="company-size"
						name="size"
						bind:value={formData.companySize}
						disabled={!isAdmin}
						class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
					>
						{#each companySizes as size}
							<option value={size}>{size} сотрудников</option>
						{/each}
					</select>
				</div>

				<div>
					<label for="company-website" class="block text-sm font-medium text-muted mb-2">URL сайта</label>
					<div class="relative">
						<Globe class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
						<input
							id="company-website"
							type="url"
							name="website"
							bind:value={formData.website}
							placeholder="https://yourcompany.com"
							disabled={!isAdmin}
							class="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
						/>
					</div>
				</div>
			</div>
		</div>

		<!-- About Company -->
		<div class="bg-white rounded-lg border border-border p-6 mt-6">
			<h2 class="text-lg font-semibold text-black mb-6">О компании</h2>
			<div class="space-y-6">
				<div>
					<label for="company-profile" class="block text-sm font-medium text-muted mb-2">
						Описание компании <span class="text-error">*</span>
					</label>
					<textarea
						id="company-profile"
						name="profile"
						bind:value={formData.about}
						rows="5"
						placeholder="Расскажите кандидатам о вашей компании..."
						disabled={!isAdmin}
						class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
					></textarea>
				</div>
			</div>
		</div>

		<!-- Contact Information -->
		<div class="bg-white rounded-lg border border-border p-6 mt-6">
			<h2 class="text-lg font-semibold text-black mb-6">Контактная информация</h2>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<label for="company-email" class="block text-sm font-medium text-muted mb-2">
						Основной email <span class="text-error">*</span>
					</label>
					<input
						id="company-email"
						type="email"
						name="email"
						bind:value={formData.primaryEmail}
						placeholder="hr@yourcompany.com"
						disabled={!isAdmin}
						class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
					/>
				</div>

				<div>
					<label for="company-phone" class="block text-sm font-medium text-muted mb-2">Номер телефона</label>
					<input
						id="company-phone"
						type="tel"
						name="phone_number"
						bind:value={formData.phone}
						placeholder="+7 395 211-12-22"
						disabled={!isAdmin}
						class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
					/>
				</div>

				<div class="md:col-span-2">
					<label for="company-address" class="block text-sm font-medium text-muted mb-2">Адрес офиса</label>
					<textarea
						id="company-address"
						name="address"
						bind:value={formData.address}
						rows="2"
						placeholder="Полный адрес офиса"
						disabled={!isAdmin}
						class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-surface disabled:text-muted"
					></textarea>
				</div>
			</div>
		</div>

		<!-- Save Button -->
		{#if isAdmin}
			<div class="flex justify-end mt-6">
				<button
					type="submit"
					disabled={saving}
					class="inline-flex items-center gap-2 px-6 py-3 bg-primary rounded-lg text-sm font-medium text-white hover:bg-primary-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
				>
					<Save class="w-4 h-4" />
					{saving ? 'Сохранение...' : 'Сохранить изменения'}
				</button>
			</div>
		{/if}
	</form>
</div>
