<script lang="ts">
	import { onMount } from 'svelte';
	import { Code, Plus, X, Pencil, Trash2, Save, Loader, Search, Star } from '@lucide/svelte';
	import { toast } from '$lib/stores/toast';
	import {
		searchSkills,
		getMySkills,
		addTechnicalSkill,
		updateTechnicalSkill,
		deleteTechnicalSkill,
		type Skill,
		type TechnicalSkill
	} from '$lib/api/skills';

	// User's current skills
	let userSkills: TechnicalSkill[] = [];
	let loading = true;
	let saving = false;

	// Add/Edit skill form
	let showAddForm = false;
	let editingSkillId: number | null = null;
	let skillSearch = '';
	let searchResults: Skill[] = [];
	let searchingSkills = false;
	let showSearchDropdown = false;

	// Form data
	let formData = {
		skill: null as number | null,
		skillName: '', // For display only
		year: undefined as number | undefined,
		month: undefined as number | undefined,
		last_used: '',
		version: '',
		proficiency: '' as '' | 'Poor' | 'Average' | 'Good' | 'Expert',
		is_major: false
	};

	const proficiencyLevels = [
		{ value: 'Poor', label: 'Новичок', color: 'bg-error-50 text-error-700 border-error-200' },
		{ value: 'Average', label: 'Средний', color: 'bg-warning-50 text-warning-700 border-warning-200' },
		{ value: 'Good', label: 'Продвинутый', color: 'bg-primary-50 text-primary-700 border-primary-200' },
		{ value: 'Expert', label: 'Эксперт', color: 'bg-success-50 text-success-700 border-success-200' }
	];

	onMount(async () => {
		await loadUserSkills();
	});

	async function loadUserSkills() {
		try {
			loading = true;
			userSkills = await getMySkills();
		} catch (err) {
			console.error('Failed to load skills:', err);
			toast.error('Не удалось загрузить навыки');
		} finally {
			loading = false;
		}
	}

	async function handleSearchSkills(search: string) {
		if (!search || search.length < 2) {
			searchResults = [];
			return;
		}

		try {
			searchingSkills = true;
			searchResults = await searchSkills({ search });
		} catch (err) {
			console.error('Failed to search skills:', err);
		} finally {
			searchingSkills = false;
		}
	}

	function selectSkill(skill: Skill) {
		formData.skill = skill.id;
		formData.skillName = skill.name;
		skillSearch = skill.name;
		showSearchDropdown = false;
		searchResults = [];
	}

	function openAddForm() {
		resetForm();
		showAddForm = true;
		editingSkillId = null;
	}

	function openEditForm(skill: TechnicalSkill) {
		formData = {
			skill: skill.skill.id,
			skillName: skill.skill.name,
			year: skill.year,
			month: skill.month,
			last_used: skill.last_used || '',
			version: skill.version || '',
			proficiency: (skill.proficiency as '' | 'Poor' | 'Average' | 'Good' | 'Expert') || '',
			is_major: skill.is_major
		};
		skillSearch = skill.skill.name;
		editingSkillId = skill.id;
		showAddForm = true;
	}

	function closeForm() {
		showAddForm = false;
		editingSkillId = null;
		resetForm();
	}

	function resetForm() {
		formData = {
			skill: null,
			skillName: '',
			year: undefined,
			month: undefined,
			last_used: '',
			version: '',
			proficiency: '',
			is_major: false
		};
		skillSearch = '';
		searchResults = [];
	}

	async function handleSaveSkill() {
		// Validation
		if (!formData.skill) {
			toast.error('Пожалуйста, выберите навык');
			return;
		}

		if (formData.year !== undefined && (formData.year < 0 || formData.year > 50)) {
			toast.error('Количество лет должно быть от 0 до 50');
			return;
		}

		if (formData.month !== undefined && (formData.month < 0 || formData.month > 11)) {
			toast.error('Количество месяцев должно быть от 0 до 11');
			return;
		}

		try {
			saving = true;

			const payload: any = {
				skill: formData.skill
			};

			// Only include fields that have values
			if (formData.year !== undefined) payload.year = formData.year;
			if (formData.month !== undefined) payload.month = formData.month;
			if (formData.last_used) payload.last_used = formData.last_used;
			if (formData.version) payload.version = formData.version;
			if (formData.proficiency) payload.proficiency = formData.proficiency;
			payload.is_major = formData.is_major;

			if (editingSkillId) {
				// Update existing skill
				await updateTechnicalSkill(editingSkillId, payload);
				toast.success('Навык успешно обновлён!');
			} else {
				// Add new skill
				await addTechnicalSkill(payload);
				toast.success('Навык успешно добавлен!');
			}

			await loadUserSkills();
			closeForm();
		} catch (err) {
			const errorMessage = err instanceof Error ? err.message : 'Не удалось сохранить навык';
			toast.error(errorMessage);
			console.error('Save skill error:', err);
		} finally {
			saving = false;
		}
	}

	async function handleDeleteSkill(skillId: number, skillName: string) {
		if (!confirm(`Вы уверены, что хотите удалить "${skillName}" из профиля?`)) {
			return;
		}

		try {
			await deleteTechnicalSkill(skillId);
			toast.success('Навык успешно удалён!');
			await loadUserSkills();
		} catch (err) {
			const errorMessage = err instanceof Error ? err.message : 'Не удалось удалить навык';
			toast.error(errorMessage);
			console.error('Delete skill error:', err);
		}
	}

	function formatExperience(year?: number, month?: number): string {
		if (year === undefined && month === undefined) return 'Не указано';
		const years = year ? `${year}y` : '';
		const months = month ? `${month}m` : '';
		return [years, months].filter(Boolean).join(' ');
	}

	function getProficiencyColor(proficiency?: string): string {
		const level = proficiencyLevels.find((l) => l.value === proficiency);
		return level?.color || 'bg-gray-100 text-gray-700';
	}

	function getProficiencyLabel(proficiency?: string): string {
		const level = proficiencyLevels.find((l) => l.value === proficiency);
		return level?.label || proficiency || 'Не указано';
	}

	// Search when user types
	$: handleSearchSkills(skillSearch);
</script>

<div class="p-5 lg:p-6">
	<div class="flex items-center justify-between mb-6">
		<div class="flex items-center gap-3">
			<div class="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center">
				<Code size={20} class="text-primary-600" />
			</div>
			<div>
				<h2 class="text-lg font-semibold text-gray-900">Технические навыки</h2>
				<p class="text-sm text-gray-600">Продемонстрируйте вашу экспертность</p>
			</div>
		</div>
		<button
			type="button"
			onclick={openAddForm}
			class="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700 transition-colors elevation-1 text-sm"
		>
			<Plus size={18} />
			<span class="hidden sm:inline">Добавить навык</span>
		</button>
	</div>

	<!-- Loading State -->
	{#if loading}
		<div class="flex flex-col items-center justify-center py-12">
			<div class="w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mb-4"></div>
			<p class="text-gray-600">Загрузка навыков...</p>
		</div>
	{:else if userSkills.length === 0 && !showAddForm}
		<!-- Empty State -->
		<div class="text-center py-12">
			<div class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-6">
				<Code size={36} class="text-gray-400" />
			</div>
			<h3 class="text-xl font-semibold text-gray-900 mb-2">Навыки ещё не добавлены</h3>
			<p class="text-gray-600 mb-6 max-w-md mx-auto">
				Добавьте ваши технические навыки, чтобы продемонстрировать экспертность и привлечь лучшие вакансии.
			</p>
			<button
				type="button"
				onclick={openAddForm}
				class="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700 transition-colors elevation-1"
			>
				<Plus size={18} />
				<span>Добавить первый навык</span>
			</button>
		</div>
	{:else}
		<!-- Skills Grid -->
		<div class="grid md:grid-cols-2 gap-4 mb-6">
			{#each userSkills as skill, i}
				<div
					class="bg-surface-50 border border-gray-100 rounded-2xl p-4 hover:border-primary-200 hover:bg-white transition-all animate-fade-in-up"
					style="opacity: 0; animation-delay: {i * 50}ms;"
				>
					<div class="flex items-start justify-between mb-3">
						<div class="flex-1">
							<h3 class="font-semibold text-gray-900 flex items-center gap-2">
								{skill.skill.name}
								{#if skill.is_major}
									<span class="inline-flex items-center gap-1 text-xs bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full border border-primary-200">
										<Star size={10} class="fill-current" />
										Основной
									</span>
								{/if}
							</h3>
							{#if skill.version}
								<p class="text-xs text-gray-500 mt-1">Версия: {skill.version}</p>
							{/if}
						</div>
						<div class="flex items-center gap-1">
							<button
								type="button"
								onclick={() => openEditForm(skill)}
								class="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-colors"
								title="Редактировать навык"
							>
								<Pencil size={16} />
							</button>
							<button
								type="button"
								onclick={() => handleDeleteSkill(skill.id, skill.skill.name)}
								class="p-2 text-gray-400 hover:text-error-600 hover:bg-error-50 rounded-xl transition-colors"
								title="Удалить навык"
							>
								<Trash2 size={16} />
							</button>
						</div>
					</div>

					<div class="grid grid-cols-2 gap-3 text-sm">
						<div>
							<p class="text-gray-500 text-xs mb-1">Опыт</p>
							<p class="font-medium text-gray-900">{formatExperience(skill.year, skill.month)}</p>
						</div>
						<div>
							<p class="text-gray-500 text-xs mb-1">Уровень</p>
							<span class="inline-block px-2.5 py-1 rounded-full text-xs font-medium border {getProficiencyColor(skill.proficiency)}">
								{getProficiencyLabel(skill.proficiency)}
							</span>
						</div>
					</div>

					{#if skill.last_used}
						<p class="text-xs text-gray-500 mt-3 pt-3 border-t border-gray-100">Последнее использование: {skill.last_used}</p>
					{/if}
				</div>
			{/each}
		</div>

		<!-- Summary Card -->
		<div class="p-5 bg-primary-50 border border-primary-100 rounded-2xl">
			<div class="flex items-start gap-4">
				<div class="w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center flex-shrink-0">
					<Code size={22} class="text-primary-600" />
				</div>
				<div>
					<h3 class="font-semibold text-gray-900 mb-1">
						{userSkills.length} {userSkills.length === 1 ? 'Навык' : 'Навыка'} Добавлено
					</h3>
					<p class="text-sm text-gray-600">
						Поддерживайте ваши навыки в актуальном состоянии, чтобы привлекать лучшие вакансии и соответствовать релевантным позициям.
					</p>
				</div>
			</div>
		</div>
	{/if}

	<!-- Add/Edit Form Modal -->
	{#if showAddForm}
		<div
			class="fixed inset-0 z-50 overflow-y-auto"
			aria-labelledby="modal-title"
			role="dialog"
			aria-modal="true"
		>
			<!-- Backdrop -->
			<div
				class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity animate-fade-in"
				onclick={closeForm}
				onkeydown={(e) => e.key === 'Escape' && closeForm()}
				role="button"
				tabindex="-1"
				aria-label="Закрыть модальное окно"
			></div>

			<!-- Modal -->
			<div class="flex min-h-screen items-center justify-center p-4">
				<div
					class="relative w-full max-w-2xl transform rounded-2xl bg-white elevation-4 transition-all animate-scale-in my-8"
				>
					<!-- Header -->
					<div class="flex items-center justify-between border-b border-gray-100 p-5 lg:p-6">
						<div class="flex items-center gap-3">
							<div class="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center">
								<Code size={20} class="text-primary-600" />
							</div>
							<h3 class="text-lg font-semibold text-gray-900" id="modal-title">
								{editingSkillId ? 'Редактировать навык' : 'Добавить навык'}
							</h3>
						</div>
						<button
							type="button"
							onclick={closeForm}
							class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-colors"
						>
							<X size={20} />
						</button>
					</div>

					<!-- Form -->
					<form onsubmit={(e) => { e.preventDefault(); handleSaveSkill(); }} class="p-5 lg:p-6 space-y-5">
						<!-- Skill Search -->
						<div class="relative">
							<label for="skill_search" class="block text-sm font-medium text-gray-700 mb-2">
								Название навыка <span class="text-error-500">*</span>
							</label>
							<div class="relative">
								<span class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none z-10">
									<Search size={18} class="text-gray-400" />
								</span>
								<input
									type="text"
									id="skill_search"
									bind:value={skillSearch}
									onfocus={() => (showSearchDropdown = true)}
									placeholder="Поиск навыка (напр., Python, Java, React)..."
									class="w-full pl-11 pr-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
									disabled={editingSkillId !== null}
									autocomplete="off"
								/>
								{#if searchingSkills}
									<div class="absolute right-4 top-3.5">
										<Loader size={18} class="animate-spin text-primary-600" />
									</div>
								{/if}
							</div>

							<!-- Search Dropdown -->
							{#if showSearchDropdown && searchResults.length > 0 && !editingSkillId}
								<div class="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-2xl shadow-xl max-h-60 overflow-y-auto">
									{#each searchResults as skill}
										<button
											type="button"
											onmousedown={() => selectSkill(skill)}
											class="w-full text-left px-4 py-3 hover:bg-primary-50 flex items-center justify-between transition-colors first:rounded-t-2xl last:rounded-b-2xl border-b border-gray-50 last:border-b-0"
										>
											<div>
												<div class="font-medium text-gray-900">{skill.name}</div>
												<div class="text-xs text-gray-500 capitalize">{skill.skill_type}</div>
											</div>
											<Plus size={16} class="text-primary-600" />
										</button>
									{/each}
								</div>
							{:else if showSearchDropdown && skillSearch.length >= 2 && searchResults.length === 0 && !searchingSkills}
								<div class="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-2xl shadow-xl p-4 text-center text-gray-500">
									Навыки по запросу "{skillSearch}" не найдены
								</div>
							{:else if showSearchDropdown && skillSearch.length < 2 && skillSearch.length > 0}
								<div class="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-2xl shadow-xl p-4 text-center text-gray-500">
									Введите минимум 2 символа для поиска
								</div>
							{/if}

							{#if formData.skill}
								<p class="mt-2 text-sm text-success-600 font-medium">✓ Выбрано: {formData.skillName}</p>
							{/if}
							{#if editingSkillId}
								<p class="mt-2 text-xs text-gray-500">Навык нельзя изменить при редактировании</p>
							{/if}
						</div>

						<!-- Experience -->
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<div>
								<label for="years" class="block text-sm font-medium text-gray-700 mb-2">
									Лет опыта
								</label>
								<input
									type="number"
									id="years"
									bind:value={formData.year}
									min="0"
									max="50"
									placeholder="0-50"
									class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
								/>
							</div>
							<div>
								<label for="months" class="block text-sm font-medium text-gray-700 mb-2">
									Месяцы
								</label>
								<input
									type="number"
									id="months"
									bind:value={formData.month}
									min="0"
									max="11"
									placeholder="0-11"
									class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
								/>
							</div>
						</div>

						<!-- Proficiency -->
						<div>
							<label for="proficiency" class="block text-sm font-medium text-gray-700 mb-2">
								Уровень владения
							</label>
							<select
								id="proficiency"
								bind:value={formData.proficiency}
								class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none appearance-none"
							>
								<option value="">Выберите уровень</option>
								{#each proficiencyLevels as level}
									<option value={level.value}>{level.label}</option>
								{/each}
							</select>
						</div>

						<!-- Version -->
						<div>
							<label for="version" class="block text-sm font-medium text-gray-700 mb-2">
								Версия (необязательно)
							</label>
							<input
								type="text"
								id="version"
								bind:value={formData.version}
								placeholder="e.g., 5.0, ES6, 3.x"
								class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
							/>
						</div>

						<!-- Last Used -->
						<div>
							<label for="last_used" class="block text-sm font-medium text-gray-700 mb-2">
								Последнее использование (необязательно)
							</label>
							<input
								type="date"
								id="last_used"
								bind:value={formData.last_used}
								class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
							/>
						</div>

						<!-- Is Major Skill -->
						<div class="p-4 bg-gray-50 rounded-xl border border-gray-100">
							<label class="flex items-start gap-3 cursor-pointer">
								<input
									type="checkbox"
									bind:checked={formData.is_major}
									class="w-5 h-5 mt-0.5 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
								/>
								<div>
									<p class="font-medium text-gray-900">Основной навык</p>
									<p class="text-sm text-gray-600">Отметьте как один из ваших главных навыков, чтобы выделить его в профиле</p>
								</div>
							</label>
						</div>

						<!-- Action Buttons -->
						<div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
							<button
								type="button"
								onclick={closeForm}
								class="px-5 py-2.5 text-gray-700 bg-white border border-gray-200 rounded-full font-medium hover:bg-gray-50 transition-colors"
								disabled={saving}
							>
								Отмена
							</button>
							<button
								type="submit"
								disabled={saving || !formData.skill}
								class="px-5 py-2.5 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 elevation-1"
							>
								{#if saving}
									<Loader size={18} class="animate-spin" />
									Сохранение...
								{:else}
									<Save size={18} />
									{editingSkillId ? 'Обновить навык' : 'Добавить навык'}
								{/if}
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	{/if}
</div>
