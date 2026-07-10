<script lang="ts">
	import BrandLogo from '$lib/components/BrandLogo.svelte';
	import { SITE_TAGLINE } from '$lib/config/brand';
	import { setContext } from 'svelte';

	const layoutState = $state({
		containerClass: 'max-w-md',
		mainClass: 'flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8'
	});

	setContext('authLayout', layoutState);

	let { children } = $props();
</script>

<div class="min-h-screen bg-surface flex flex-col">
	<!-- Header -->
	<header class="bg-white border-b border-border">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
			<BrandLogo href="/" subtitle={SITE_TAGLINE} />
		</div>
	</header>

	<!-- Main Content -->
	<main class={layoutState.mainClass}>
		<div class={`w-full ${layoutState.containerClass}`}>
			{@render children?.()}
		</div>
	</main>

	<!-- Footer -->
	<footer class="bg-white border-t border-border py-6">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted">
				<p>&copy; 2025 Truddy.ru. Все права защищены.</p>
				<div class="flex gap-6">
					<a href="/about/" class="hover:text-black transition-colors">О нас</a>
					<a href="/privacy/" class="hover:text-black transition-colors">Конфиденциальность</a>
					<a href="/terms/" class="hover:text-black transition-colors">Условия</a>
					<a href="/contact/" class="hover:text-black transition-colors">Контакты</a>
				</div>
			</div>
		</div>
	</footer>
</div>
