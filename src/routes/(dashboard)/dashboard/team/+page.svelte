<script lang="ts">
	import {
		Users,
		UserPlus,
		Mail,
		Crown,
		Calendar,
		Briefcase,
		FileText,
		MoreVertical,
		Edit,
		Trash2,
		Send,
		X,
		CheckCircle,
		XCircle,
		Shield,
		Clock,
		Eye
	} from '@lucide/svelte';
	import { enhance } from '$app/forms';
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();

	// State management
	let showInviteDialog = $state(false);
	let showEditDialog = $state(false);
	let showRemoveDialog = $state(false);
	let selectedMember = $state<any>(null);
	let searchQuery = $state('');
	let submitting = $state(false);
	let showSuccessMessage = $state(false);
	let showErrorMessage = $state(false);

	// Invite form state
	let inviteForm = $state({
		email: '',
		job_title: '',
		message: ''
	});

	// Edit form state
	let editForm = $state({
		job_title: '',
		is_admin: false
	});

	// Computed values
	let isAdmin = $derived(data.user?.is_admin === true);
	let filteredMembers = $derived(
		data.team.members.filter(
			(member: any) =>
				member.first_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				member.last_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				member.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				member.job_title?.toLowerCase().includes(searchQuery.toLowerCase())
		)
	);

	// Watch for form submission results
	$effect(() => {
		if (form?.success) {
			showSuccessMessage = true;
			submitting = false;

			// Close dialogs on success
			if (form.action === 'invite') {
				showInviteDialog = false;
				resetInviteForm();
			} else if (form.action === 'update') {
				showEditDialog = false;
				selectedMember = null;
			} else if (form.action === 'remove') {
				showRemoveDialog = false;
				selectedMember = null;
			}

			setTimeout(() => {
				showSuccessMessage = false;
			}, 5000);
		} else if (form?.success === false) {
			showErrorMessage = true;
			submitting = false;
			setTimeout(() => {
				showErrorMessage = false;
			}, 5000);
		}
	});

	function resetInviteForm() {
		inviteForm.email = '';
		inviteForm.job_title = '';
		inviteForm.message = '';
	}

	function openEditDialog(member: any) {
		selectedMember = member;
		editForm.job_title = member.job_title || '';
		editForm.is_admin = member.is_admin;
		showEditDialog = true;
	}

	function openRemoveDialog(member: any) {
		selectedMember = member;
		showRemoveDialog = true;
	}

	function formatDate(dateString: string) {
		if (!dateString) return '—';
		const date = new Date(dateString);
		return date.toLocaleDateString('ru-RU', { year: 'numeric', month: 'short', day: 'numeric' });
	}

	function getInitials(firstName: string, lastName: string) {
		return `${firstName?.[0] || ''}${lastName?.[0] || ''}`.toUpperCase() || '?';
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'pending':
				return 'bg-warning-light text-warning';
			case 'accepted':
				return 'bg-success-light text-success';
			case 'expired':
				return 'bg-error-light text-error';
			case 'cancelled':
				return 'bg-surface text-black';
			default:
				return 'bg-surface text-black';
		}
	}

	function getStatusLabel(status: string) {
		switch (status) {
			case 'pending':
				return 'Ожидает';
			case 'accepted':
				return 'Принято';
			case 'expired':
				return 'Истекло';
			case 'cancelled':
				return 'Отменено';
			default:
				return status;
		}
	}
</script>

<svelte:head>
	<title>Управление командой - Truddy.ru Recruiter</title>
</svelte:head>

<div class="max-w-7xl space-y-6">
	<!-- Success/Error Messages -->
	{#if showSuccessMessage}
		<div class="bg-success-light border border-success/30 rounded-lg p-4 flex items-start gap-3">
			<CheckCircle class="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
			<div class="flex-1">
				<h3 class="text-sm font-medium text-success">Готово!</h3>
				<p class="text-sm text-success mt-1">{form?.message || 'Действие выполнено успешно'}</p>
			</div>
		</div>
	{/if}

	{#if showErrorMessage}
		<div class="bg-error-light border border-error/30 rounded-lg p-4 flex items-start gap-3">
			<XCircle class="w-5 h-5 text-error flex-shrink-0 mt-0.5" />
			<div class="flex-1">
				<h3 class="text-sm font-medium text-error">Ошибка</h3>
				<p class="text-sm text-error mt-1">{form?.error || 'Не удалось выполнить действие'}</p>
			</div>
		</div>
	{/if}

	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
		<div>
			<h1 class="text-2xl md:text-3xl font-bold text-black flex items-center gap-2">
				<Users class="w-8 h-8" />
				Управление командой
			</h1>
			<p class="text-muted mt-1">
				Управляйте участниками команды и совместно работайте над вакансиями
			</p>
			{#if !isAdmin}
				<p class="text-sm text-amber-600 mt-1">⚠️ Только администраторы компании могут управлять участниками команды</p>
			{/if}
		</div>

		{#if isAdmin}
			<button
				onclick={() => (showInviteDialog = true)}
				class="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition-colors"
			>
				<UserPlus class="w-4 h-4" />
				Пригласить участника
			</button>
		{/if}
	</div>

	<!-- Team Stats -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
		<div class="bg-white rounded-lg border border-border p-6">
			<div class="flex items-center gap-3">
				<div class="p-3 bg-primary/10 rounded-lg">
					<Users class="w-6 h-6 text-primary" />
				</div>
				<div>
					<p class="text-sm text-muted">Всего участников</p>
					<p class="text-2xl font-bold text-black">{data.team.total_members}</p>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-6">
			<div class="flex items-center gap-3">
				<div class="p-3 bg-purple-100 rounded-lg">
					<Crown class="w-6 h-6 text-purple-600" />
				</div>
				<div>
					<p class="text-sm text-muted">Администраторы</p>
					<p class="text-2xl font-bold text-black">
						{data.team.members.filter((m: any) => m.is_admin).length}
					</p>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg border border-border p-6">
			<div class="flex items-center gap-3">
				<div class="p-3 bg-success-light rounded-lg">
					<Mail class="w-6 h-6 text-success" />
				</div>
				<div>
					<p class="text-sm text-muted">Ожидающие приглашения</p>
					<p class="text-2xl font-bold text-black">{data.invitations.pending_count}</p>
				</div>
			</div>
		</div>
	</div>

	<!-- Search -->
	<div class="bg-white rounded-lg border border-border p-4">
		<input
			type="text"
			bind:value={searchQuery}
			placeholder="Поиск участников по имени, email или должности..."
			class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
		/>
	</div>

	<!-- Team Members List -->
	<div class="bg-white rounded-lg border border-border">
		<div class="p-6 border-b border-border">
			<h2 class="text-lg font-semibold text-black">Участники команды ({filteredMembers.length})</h2>
		</div>

		<div class="divide-y divide-border">
			{#each filteredMembers as member}
				<div class="p-6 hover:bg-surface transition-colors">
					<div class="flex items-start gap-4">
						<!-- Avatar -->
						<div
							class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-primary font-semibold flex-shrink-0"
						>
							{getInitials(member.first_name, member.last_name)}
						</div>

						<!-- Member Info -->
						<div class="flex-1 min-w-0">
							<div class="flex items-start justify-between gap-4">
								<div class="flex-1">
									<div class="flex items-center gap-2">
										<h3 class="text-base font-semibold text-black">
											{member.first_name}
											{member.last_name || ''}
										</h3>
										{#if member.is_admin}
											<span
												class="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded"
											>
												<Crown class="w-3 h-3" />
												Админ
											</span>
										{/if}
										{#if member.id === data.user.id}
											<span
												class="inline-flex items-center px-2 py-1 bg-primary/10 text-primary text-xs font-medium rounded"
											>
												Вы
											</span>
										{/if}
									</div>
									<p class="text-sm text-muted mt-1">{member.email}</p>
									{#if member.job_title}
										<p class="text-sm text-muted mt-1 flex items-center gap-1">
											<Briefcase class="w-3 h-3" />
											{member.job_title}
										</p>
									{/if}
								</div>

								<!-- Actions Menu -->
								{#if isAdmin && member.id !== data.user.id}
									<div class="flex items-center gap-2">
										<a
											href="/dashboard/team/{member.id}/"
											class="p-2 text-muted hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
											title="Просмотр деталей"
										>
											<Eye class="w-4 h-4" />
										</a>
										<button
											onclick={() => openEditDialog(member)}
											class="p-2 text-muted hover:text-primary hover:bg-primary/10 rounded-lg transition-colors"
											title="Редактировать участника"
										>
											<Edit class="w-4 h-4" />
										</button>
										<button
											onclick={() => openRemoveDialog(member)}
											class="p-2 text-muted hover:text-error hover:bg-error-light rounded-lg transition-colors"
											title="Удалить участника"
										>
											<Trash2 class="w-4 h-4" />
										</button>
									</div>
								{/if}
							</div>

							<!-- Member Stats -->
							<div class="grid grid-cols-3 gap-4 mt-4">
								<div class="text-center p-3 bg-surface rounded-lg">
									<p class="text-xs text-muted">Опубликовано вакансий</p>
									<p class="text-lg font-semibold text-black">{member.stats.jobs_posted}</p>
								</div>
								<div class="text-center p-3 bg-surface rounded-lg">
									<p class="text-xs text-muted">Активные вакансии</p>
									<p class="text-lg font-semibold text-black">{member.stats.active_jobs}</p>
								</div>
								<div class="text-center p-3 bg-surface rounded-lg">
									<p class="text-xs text-muted">Всего соискателей</p>
									<p class="text-lg font-semibold text-black">{member.stats.total_applicants}</p>
								</div>
							</div>

							<div class="flex items-center gap-4 mt-3 text-xs text-muted">
								<span class="flex items-center gap-1">
									<Calendar class="w-3 h-3" />
									В команде с {formatDate(member.date_joined)}
								</span>
								{#if member.last_login}
									<span class="flex items-center gap-1">
										<Clock class="w-3 h-3" />
										Последняя активность {formatDate(member.last_login)}
									</span>
								{/if}
							</div>
						</div>
					</div>
				</div>
			{/each}

			{#if filteredMembers.length === 0}
				<div class="p-12 text-center">
					<Users class="w-12 h-12 text-muted mx-auto mb-3" />
					<p class="text-muted">Участники команды не найдены</p>
				</div>
			{/if}
		</div>
	</div>

	<!-- Pending Invitations -->
	{#if isAdmin && data.invitations.invitations.length > 0}
		<div class="bg-white rounded-lg border border-border">
			<div class="p-6 border-b border-border">
				<h2 class="text-lg font-semibold text-black flex items-center gap-2">
					<Mail class="w-5 h-5" />
					Ожидающие приглашения ({data.invitations.pending_count})
				</h2>
			</div>

			<div class="divide-y divide-border">
				{#each data.invitations.invitations as invitation}
					<div class="p-6 hover:bg-surface transition-colors">
						<div class="flex items-start justify-between gap-4">
							<div class="flex-1">
								<div class="flex items-center gap-2">
									<Mail class="w-4 h-4 text-muted" />
									<p class="font-medium text-black">{invitation.email}</p>
									<span class="px-2 py-1 text-xs font-medium rounded {getStatusColor(invitation.status)}">
										{getStatusLabel(invitation.status)}
									</span>
								</div>
								{#if invitation.role_title}
									<p class="text-sm text-muted mt-1">Роль: {invitation.role_title}</p>
								{/if}
								<div class="flex items-center gap-4 mt-2 text-xs text-muted">
									<span>Пригласил(а) {invitation.invited_by_name}</span>
									<span>Отправлено {formatDate(invitation.created_at)}</span>
									{#if invitation.status === 'pending'}
										<span class="text-amber-600">Истекает через {invitation.days_remaining} дн.</span>
									{/if}
								</div>
							</div>

							{#if invitation.status === 'pending'}
								<div class="flex items-center gap-2">
									<form method="POST" action="?/resendInvitation" use:enhance>
										<input type="hidden" name="invitation_id" value={invitation.id} />
										<button
											type="submit"
											class="p-2 text-muted hover:text-success hover:bg-success-light rounded-lg transition-colors"
											title="Отправить приглашение повторно"
										>
											<Send class="w-4 h-4" />
										</button>
									</form>
									<form method="POST" action="?/cancelInvitation" use:enhance>
										<input type="hidden" name="invitation_id" value={invitation.id} />
										<button
											type="submit"
											class="p-2 text-muted hover:text-error hover:bg-error-light rounded-lg transition-colors"
											title="Отменить приглашение"
										>
											<X class="w-4 h-4" />
										</button>
									</form>
								</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

<!-- Invite Member Dialog -->
{#if showInviteDialog}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
		<div class="bg-white rounded-lg max-w-md w-full">
			<div class="p-6 border-b border-border">
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-semibold text-black flex items-center gap-2">
						<UserPlus class="w-5 h-5" />
						Пригласить участника
					</h3>
					<button
						onclick={() => {
							showInviteDialog = false;
							resetInviteForm();
						}}
						class="text-muted hover:text-muted"
					>
						<X class="w-5 h-5" />
					</button>
				</div>
			</div>

			<form
				method="POST"
				action="?/inviteMember"
				use:enhance={() => {
					submitting = true;
					return async ({ update }) => {
						await update();
					};
				}}
			>
				<div class="p-6 space-y-4">
					<div>
						<label for="invite-email" class="block text-sm font-medium text-muted mb-2">
							Адрес электронной почты <span class="text-error">*</span>
						</label>
						<input
							id="invite-email"
							type="email"
							name="email"
							bind:value={inviteForm.email}
							required
							placeholder="kollega@example.com"
							class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
						/>
					</div>

					<div>
						<label for="invite-job-title" class="block text-sm font-medium text-muted mb-2">Должность (необязательно)</label>
						<input
							id="invite-job-title"
							type="text"
							name="job_title"
							bind:value={inviteForm.job_title}
							placeholder="напр., Старший рекрутер"
							class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
						/>
					</div>

					<div>
						<label for="invite-message" class="block text-sm font-medium text-muted mb-2">
							Личное сообщение (необязательно)
						</label>
						<textarea
							id="invite-message"
							name="message"
							bind:value={inviteForm.message}
							rows="3"
							placeholder="Добавьте личное сообщение к приглашению..."
							class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
						></textarea>
					</div>

					<p class="text-sm text-muted">
						На указанный email будет отправлено приглашение со ссылкой для присоединения к команде.
						Срок действия приглашения — 7 дней.
					</p>
				</div>

				<div class="p-6 border-t border-border flex justify-end gap-3">
					<button
						type="button"
						onclick={() => {
							showInviteDialog = false;
							resetInviteForm();
						}}
						class="px-4 py-2 text-muted bg-surface rounded-lg hover:bg-surface transition-colors"
					>
						Отмена
					</button>
					<button
						type="submit"
						disabled={submitting || !inviteForm.email}
						class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{submitting ? 'Отправка...' : 'Отправить приглашение'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- Edit Member Dialog -->
{#if showEditDialog && selectedMember}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
		<div class="bg-white rounded-lg max-w-md w-full">
			<div class="p-6 border-b border-border">
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-semibold text-black flex items-center gap-2">
						<Edit class="w-5 h-5" />
						Редактировать участника
					</h3>
					<button
						onclick={() => {
							showEditDialog = false;
							selectedMember = null;
						}}
						class="text-muted hover:text-muted"
					>
						<X class="w-5 h-5" />
					</button>
				</div>
			</div>

			<form
				method="POST"
				action="?/updateMember"
				use:enhance={() => {
					submitting = true;
					return async ({ update }) => {
						await update();
					};
				}}
			>
				<input type="hidden" name="user_id" value={selectedMember.id} />

				<div class="p-6 space-y-4">
					<div>
						<p class="text-sm text-muted mb-4">
							Редактирование: <strong>{selectedMember.first_name} {selectedMember.last_name}</strong>
						</p>
					</div>

					<div>
						<label for="edit-job-title" class="block text-sm font-medium text-muted mb-2">Должность</label>
						<input
							id="edit-job-title"
							type="text"
							name="job_title"
							bind:value={editForm.job_title}
							placeholder="напр., Старший рекрутер"
							class="w-full px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary"
						/>
					</div>

					<div class="flex items-start gap-3 p-4 bg-purple-50 rounded-lg">
						<input
							type="checkbox"
							name="is_admin"
							id="is_admin"
							bind:checked={editForm.is_admin}
							value="true"
							class="mt-1"
						/>
						<label for="is_admin" class="flex-1">
							<div class="flex items-center gap-2 text-sm font-medium text-black">
								<Shield class="w-4 h-4 text-purple-600" />
								Администратор компании
							</div>
							<p class="text-xs text-muted mt-1">
								Администраторы могут приглашать участников, управлять командой и редактировать профиль компании
							</p>
						</label>
					</div>
				</div>

				<div class="p-6 border-t border-border flex justify-end gap-3">
					<button
						type="button"
						onclick={() => {
							showEditDialog = false;
							selectedMember = null;
						}}
						class="px-4 py-2 text-muted bg-surface rounded-lg hover:bg-surface transition-colors"
					>
						Отмена
					</button>
					<button
						type="submit"
						disabled={submitting}
						class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{submitting ? 'Сохранение...' : 'Сохранить изменения'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- Remove Member Dialog -->
{#if showRemoveDialog && selectedMember}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
		<div class="bg-white rounded-lg max-w-md w-full">
			<div class="p-6 border-b border-border">
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-semibold text-error flex items-center gap-2">
						<Trash2 class="w-5 h-5" />
						Удалить участника
					</h3>
					<button
						onclick={() => {
							showRemoveDialog = false;
							selectedMember = null;
						}}
						class="text-muted hover:text-muted"
					>
						<X class="w-5 h-5" />
					</button>
				</div>
			</div>

			<form
				method="POST"
				action="?/removeMember"
				use:enhance={() => {
					submitting = true;
					return async ({ update }) => {
						await update();
					};
				}}
			>
				<input type="hidden" name="user_id" value={selectedMember.id} />

				<div class="p-6">
					<p class="text-muted mb-4">
						Вы уверены, что хотите удалить
						<strong>{selectedMember.first_name} {selectedMember.last_name}</strong>
						из команды?
					</p>
					<div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
						<p class="text-sm text-amber-800">
							⚠️ Этот участник потеряет доступ ко всем вакансиям и данным компании. Он станет
							независимым рекрутером.
						</p>
					</div>
				</div>

				<div class="p-6 border-t border-border flex justify-end gap-3">
					<button
						type="button"
						onclick={() => {
							showRemoveDialog = false;
							selectedMember = null;
						}}
						class="px-4 py-2 text-muted bg-surface rounded-lg hover:bg-surface transition-colors"
					>
						Отмена
					</button>
					<button
						type="submit"
						disabled={submitting}
						class="px-4 py-2 bg-error text-white rounded-lg hover:bg-error transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{submitting ? 'Удаление...' : 'Удалить участника'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}
