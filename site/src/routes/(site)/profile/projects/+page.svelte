<script lang="ts">
	import { onMount } from 'svelte';
	import { FolderOpen, Plus, Rocket } from '@lucide/svelte';
	import { toast } from '$lib/stores/toast';
	import { getMyProjects, deleteProject } from '$lib/api/projects';
	import type { Project } from '$lib/api/projects';
	import ProjectCard from '$lib/components/profile/ProjectCard.svelte';
	import AddProjectModal from '$lib/components/profile/AddProjectModal.svelte';

	let projectList: Project[] = $state([]);
	let loading = $state(true);
	let isModalOpen = $state(false);
	let selectedProject: Project | null = $state(null);

	onMount(async () => {
		await loadProjects();
	});

	async function loadProjects() {
		loading = true;
		try {
			projectList = await getMyProjects();
		} catch (error) {
			console.error('Failed to load projects:', error);
			toast.error('Не удалось загрузить проекты');
		} finally {
			loading = false;
		}
	}

	function handleAddProject() {
		selectedProject = null;
		isModalOpen = true;
	}

	function handleEditProject(project: Project) {
		selectedProject = project;
		isModalOpen = true;
	}

	async function handleDeleteProject(id: number) {
		if (!confirm('Вы уверены, что хотите удалить этот проект?')) {
			return;
		}

		try {
			await deleteProject(id);
			toast.success('Проект успешно удалён!');
			await loadProjects();
		} catch (error) {
			console.error('Failed to delete project:', error);
			toast.error('Не удалось удалить проект. Попробуйте ещё раз.');
		}
	}

	async function handleSuccess() {
		await loadProjects();
	}

	function handleCloseModal() {
		isModalOpen = false;
		selectedProject = null;
	}
</script>

<svelte:head>
	<title>Проекты - Профиль - Truddy.ru</title>
	<meta name="description" content="Продемонстрируйте ваше портфолио и достижения" />
</svelte:head>

<!-- Header -->
<div class="mb-6 animate-fade-in-up" style="opacity: 0;">
	<div class="flex items-center justify-between gap-4">
		<div class="flex items-center gap-3">
			<div class="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center">
				<FolderOpen size={20} class="text-primary-600" />
			</div>
			<div>
				<h2 class="text-xl lg:text-2xl font-bold text-gray-900">Проекты</h2>
				<p class="text-sm text-gray-600">Продемонстрируйте ваше портфолио и достижения</p>
			</div>
		</div>
		<button
			type="button"
			onclick={handleAddProject}
			class="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700 transition-colors elevation-1 text-sm"
		>
			<Plus size={18} />
			<span class="hidden sm:inline">Добавить проект</span>
		</button>
	</div>
</div>

<!-- Project List -->
{#if loading}
	<div
		class="bg-white rounded-2xl p-12 elevation-1 border border-gray-100 text-center animate-fade-in-up"
		style="opacity: 0; animation-delay: 100ms;"
	>
		<div
			class="w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"
		></div>
		<p class="text-gray-600">Загрузка проектов...</p>
	</div>
{:else if projectList.length === 0}
	<!-- Empty State -->
	<div
		class="bg-white rounded-2xl p-12 elevation-1 border border-gray-100 text-center animate-fade-in-up"
		style="opacity: 0; animation-delay: 100ms;"
	>
		<div
			class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-6"
		>
			<FolderOpen size={36} class="text-gray-400" />
		</div>
		<h3 class="text-xl font-semibold text-gray-900 mb-2">Проекты ещё не добавлены</h3>
		<p class="text-gray-600 mb-6 max-w-md mx-auto">
			Добавьте проекты, чтобы продемонстрировать вашу работу, навыки и достижения. Проекты помогают рекрутерам понять ваш практический опыт.
		</p>
		<button
			type="button"
			onclick={handleAddProject}
			class="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700 transition-colors elevation-1"
		>
			<Plus size={18} />
			<span>Добавить первый проект</span>
		</button>
	</div>
{:else}
	<!-- Project Cards -->
	<div class="space-y-4">
		{#each projectList as project, i (project.id)}
			<div
				class="bg-white rounded-2xl elevation-1 border border-gray-100 overflow-hidden animate-fade-in-up"
				style="opacity: 0; animation-delay: {(i + 1) * 50 + 100}ms;"
			>
				<ProjectCard {project} onEdit={handleEditProject} onDelete={handleDeleteProject} />
			</div>
		{/each}
	</div>

	<!-- Summary -->
	<div
		class="mt-6 p-5 lg:p-6 bg-primary-50 border border-primary-100 rounded-2xl animate-fade-in-up"
		style="opacity: 0; animation-delay: 400ms;"
	>
		<div class="flex items-start gap-4">
			<div
				class="w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center flex-shrink-0"
			>
				<Rocket size={22} class="text-primary-600" />
			</div>
			<div>
				<h3 class="font-semibold text-gray-900 mb-1">
					{projectList.length} {projectList.length === 1 ? 'Проект' : 'Проекта'} в портфолио
				</h3>
				<p class="text-sm text-gray-600">
					Ваши проекты демонстрируют ваши навыки и опыт потенциальным работодателям. Обновляйте их вашей последней работой!
				</p>
			</div>
		</div>
	</div>
{/if}

<!-- Add/Edit Project Modal -->
<AddProjectModal
	bind:isOpen={isModalOpen}
	onClose={handleCloseModal}
	onSuccess={handleSuccess}
	project={selectedProject}
/>
