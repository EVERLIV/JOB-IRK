<script lang="ts">
	import { Briefcase } from '@lucide/svelte';
	import { SITE_NAME } from '$lib/config/brand';

	type Props = {
		href?: string;
		class?: string;
		textClass?: string;
		subtitle?: string;
		subtitleClass?: string;
		showText?: boolean;
		size?: 'sm' | 'md' | 'lg';
	};

	let {
		href = '/',
		class: className = '',
		textClass = 'text-black',
		subtitle = '',
		subtitleClass = 'text-sm text-muted ml-2',
		showText = true,
		size = 'md'
	}: Props = $props();

	const iconBox = { sm: 'h-8 w-8', md: 'h-9 w-9', lg: 'h-10 w-10' };
	const iconSize = { sm: 16, md: 20, lg: 24 };
	const textSize = { sm: 'text-lg', md: 'text-xl', lg: 'text-2xl' };
</script>

<a {href} class="inline-flex items-center gap-2 group {className}">
	<span
		class="flex items-center justify-center rounded-lg bg-primary-600 text-white shadow-sm {iconBox[size]}"
	>
		<Briefcase size={iconSize[size]} />
	</span>
	{#if showText}
		<span class="font-bold {textSize[size]} {textClass}">{SITE_NAME}</span>
	{/if}
	{#if subtitle}
		<span class={subtitleClass}>{subtitle}</span>
	{/if}
</a>
