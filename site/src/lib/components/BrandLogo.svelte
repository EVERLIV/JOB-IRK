<script lang="ts">
	import { Briefcase } from '@lucide/svelte';
	import { SITE_NAME } from '$lib/config/brand';

	type Props = {
		href?: string;
		class?: string;
		textClass?: string;
		iconBoxClass?: string;
		showText?: boolean;
		size?: 'sm' | 'md' | 'lg';
		reload?: boolean;
	};

	let {
		href = '/',
		class: className = '',
		textClass = 'text-black',
		iconBoxClass = 'bg-primary-600',
		showText = true,
		size = 'md',
		reload = false
	}: Props = $props();

	const iconBox = { sm: 'h-8 w-8', md: 'h-9 w-9', lg: 'h-10 w-10' };
	const iconSize = { sm: 16, md: 20, lg: 24 };
	const textSize = { sm: 'text-lg', md: 'text-xl', lg: 'text-2xl' };
</script>

<a
	{href}
	data-sveltekit-reload={reload || undefined}
	class="inline-flex items-center gap-2 group {className}"
>
	<span
		class="flex items-center justify-center rounded-lg text-white shadow-sm {iconBox[size]} {iconBoxClass}"
	>
		<Briefcase size={iconSize[size]} />
	</span>
	{#if showText}
		<span class="font-semibold {textSize[size]} {textClass}">{SITE_NAME}</span>
	{/if}
</a>
