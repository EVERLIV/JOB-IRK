<script lang="ts">
	import { User, Mail, Phone, Calendar } from '@lucide/svelte';

	// Accept the full formData object, only use the fields we need
	export let formData: {
		first_name: string;
		last_name: string;
		mobile: string;
		alternate_mobile: string;
		gender: string;
		dob: string;
		marital_status: string;
		nationality: string;
		[key: string]: any; // Allow other fields
	};
	export let email: string;
	export let validationErrors: Record<string, string> = {};
</script>

<div class="p-5 lg:p-6">
	<div class="flex items-center gap-3 mb-6">
		<div class="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center">
			<User size={20} class="text-primary-600" />
		</div>
		<div>
			<h2 class="text-lg font-semibold text-gray-900">Личные данные</h2>
			<p class="text-sm text-gray-600">Ваши основные данные</p>
		</div>
	</div>

	<div class="grid md:grid-cols-2 gap-5">
		<!-- First Name -->
		<div>
			<label for="first_name" class="block text-sm font-medium text-gray-700 mb-2">
				Имя <span class="text-error-500">*</span>
			</label>
			<input
				id="first_name"
				type="text"
				bind:value={formData.first_name}
				class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white transition-all outline-none {validationErrors.first_name ? 'border-error-500 focus:border-error-500 focus:ring-2 focus:ring-error-500/20' : 'border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20'}"
				required
			/>
			{#if validationErrors.first_name}
				<p class="mt-2 text-sm text-error-600">{validationErrors.first_name}</p>
			{/if}
		</div>

		<!-- Last Name -->
		<div>
			<label for="last_name" class="block text-sm font-medium text-gray-700 mb-2">
				Фамилия <span class="text-error-500">*</span>
			</label>
			<input
				id="last_name"
				type="text"
				bind:value={formData.last_name}
				class="w-full px-4 py-3 border rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white transition-all outline-none {validationErrors.last_name ? 'border-error-500 focus:border-error-500 focus:ring-2 focus:ring-error-500/20' : 'border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20'}"
				required
			/>
			{#if validationErrors.last_name}
				<p class="mt-2 text-sm text-error-600">{validationErrors.last_name}</p>
			{/if}
		</div>

		<!-- Email (Read-only) -->
		<div>
			<label for="email" class="block text-sm font-medium text-gray-700 mb-2">
				Электронная почта
			</label>
			<div class="relative">
				<span class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
					<Mail size={18} class="text-gray-400" />
				</span>
				<div class="w-full pl-11 pr-4 py-3 border border-gray-200 rounded-xl bg-gray-100 text-gray-600">
					{email}
				</div>
			</div>
			<p class="mt-2 text-xs text-gray-500">Электронную почту нельзя изменить</p>
		</div>

		<!-- Mobile Number -->
		<div>
			<label for="mobile" class="block text-sm font-medium text-gray-700 mb-2">
				Мобильный номер
			</label>
			<div class="relative">
				<span class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
					<Phone size={18} class="text-gray-400" />
				</span>
				<input
					id="mobile"
					type="tel"
					bind:value={formData.mobile}
					placeholder="+91 9876543210"
					class="w-full pl-11 pr-4 py-3 border rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white transition-all outline-none {validationErrors.mobile ? 'border-error-500 focus:border-error-500 focus:ring-2 focus:ring-error-500/20' : 'border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20'}"
				/>
			</div>
			{#if validationErrors.mobile}
				<p class="mt-2 text-sm text-error-600">{validationErrors.mobile}</p>
			{/if}
		</div>

		<!-- Alternate Mobile Number -->
		<div>
			<label for="alternate_mobile" class="block text-sm font-medium text-gray-700 mb-2">
				Дополнительный мобильный номер
			</label>
			<div class="relative">
				<span class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
					<Phone size={18} class="text-gray-400" />
				</span>
				<input
					id="alternate_mobile"
					type="tel"
					bind:value={formData.alternate_mobile}
					placeholder="+91 9876543210"
					class="w-full pl-11 pr-4 py-3 border rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white transition-all outline-none {validationErrors.alternate_mobile ? 'border-error-500 focus:border-error-500 focus:ring-2 focus:ring-error-500/20' : 'border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20'}"
				/>
			</div>
			{#if validationErrors.alternate_mobile}
				<p class="mt-2 text-sm text-error-600">{validationErrors.alternate_mobile}</p>
			{/if}
		</div>

		<!-- Gender -->
		<div>
			<label for="gender" class="block text-sm font-medium text-gray-700 mb-2">Пол</label>
			<select
				id="gender"
				bind:value={formData.gender}
				class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none appearance-none"
			>
				<option value="">Выберите пол</option>
				<option value="M">Мужской</option>
				<option value="F">Женский</option>
			</select>
		</div>

		<!-- Date of Birth -->
		<div>
			<label for="dob" class="block text-sm font-medium text-gray-700 mb-2">
				Дата рождения
			</label>
			<div class="relative">
				<span class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
					<Calendar size={18} class="text-gray-400" />
				</span>
				<input
					id="dob"
					type="date"
					bind:value={formData.dob}
					class="w-full pl-11 pr-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
				/>
			</div>
		</div>

		<!-- Marital Status -->
		<div>
			<label for="marital_status" class="block text-sm font-medium text-gray-700 mb-2">
				Семейное положение
			</label>
			<select
				id="marital_status"
				bind:value={formData.marital_status}
				class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none appearance-none"
			>
				<option value="">Выберите статус</option>
				<option value="Single">Не женат/Не замужем</option>
				<option value="Married">Женат/Замужем</option>
			</select>
		</div>

		<!-- Nationality -->
		<div>
			<label for="nationality" class="block text-sm font-medium text-gray-700 mb-2">
				Гражданство
			</label>
			<input
				id="nationality"
				type="text"
				bind:value={formData.nationality}
				placeholder="напр., Российское"
				class="w-full px-4 py-3 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder-gray-500 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all outline-none"
			/>
		</div>
	</div>
</div>
