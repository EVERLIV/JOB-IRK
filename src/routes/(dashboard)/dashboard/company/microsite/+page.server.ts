/**
 * Company Microsite Management - Server Load & Actions
 * Allows company admins to manage custom menu items for their company page
 */

import type { PageServerLoad, Actions } from './$types';
import { redirect, fail } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib/config/env';

export const load: PageServerLoad = async ({ parent, fetch }) => {
	// Get user data from parent layout
	const { user } = await parent();

	// Check if user is part of a company
	if (!user?.company) {
		throw redirect(302, '/dashboard/');
	}

	// Check if user has permission to edit company
	if (!user?.permissions?.can_edit_company) {
		throw redirect(302, '/dashboard/');
	}

	try {
		// Fetch company menu items
		const response = await fetch(`${API_BASE_URL}/recruiter/company/menu/`);

		const menuData = response.ok ? await response.json() : { menus: [] };

		return {
			user,
			company: user.company,
			menus: menuData.menus || []
		};
	} catch (error) {
		console.error('Error loading microsite data:', error);
		return {
			user,
			company: user.company,
			menus: [],
			error: 'Не удалось загрузить пункты меню'
		};
	}
};

export const actions: Actions = {
	/**
	 * Create new menu item
	 */
	createMenu: async ({ request, fetch }) => {
		const formData = await request.formData();

		const menuData = {
			title: formData.get('title')?.toString(),
			url: formData.get('url')?.toString(),
			is_active: formData.get('is_active') === 'true'
		};

		if (!menuData.title || !menuData.url) {
			return fail(400, {
				action: 'create',
				success: false,
				error: 'Укажите название и URL'
			});
		}

		try {
			const response = await fetch(`${API_BASE_URL}/recruiter/company/menu/add/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(menuData)
			});

			const result = await response.json();

			if (response.ok) {
				return {
					action: 'create',
					success: true,
					message: result.message || 'Пункт меню успешно создан',
					menu: result.menu
				};
			} else {
				return fail(400, {
					action: 'create',
					success: false,
					error: result.error || 'Не удалось создать пункт меню',
					errors: result
				});
			}
		} catch (error) {
			console.error('Error creating menu item:', error);
			return fail(500, {
				action: 'create',
				success: false,
				error: 'Произошла ошибка при создании пункта меню'
			});
		}
	},

	/**
	 * Update menu item
	 */
	updateMenu: async ({ request, fetch }) => {
		const formData = await request.formData();
		const menuId = formData.get('menu_id')?.toString();

		if (!menuId) {
			return fail(400, {
				action: 'update',
				success: false,
				error: 'Не указан ID пункта меню'
			});
		}

		const menuData: Record<string, any> = {};

		const title = formData.get('title')?.toString();
		const url = formData.get('url')?.toString();
		const isActive = formData.get('is_active')?.toString();
		const order = formData.get('order')?.toString();

		if (title) menuData.title = title;
		if (url) menuData.url = url;
		if (isActive !== undefined) menuData.is_active = isActive === 'true';
		if (order) menuData.order = parseInt(order);

		try {
			const response = await fetch(`${API_BASE_URL}/recruiter/company/menu/edit/${menuId}/`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(menuData)
			});

			const result = await response.json();

			if (response.ok) {
				return {
					action: 'update',
					success: true,
					message: result.message || 'Пункт меню успешно обновлён',
					menu: result.menu
				};
			} else {
				return fail(400, {
					action: 'update',
					success: false,
					error: result.error || 'Не удалось обновить пункт меню',
					errors: result
				});
			}
		} catch (error) {
			console.error('Error updating menu item:', error);
			return fail(500, {
				action: 'update',
				success: false,
				error: 'Произошла ошибка при обновлении пункта меню'
			});
		}
	},

	/**
	 * Delete menu item
	 */
	deleteMenu: async ({ request, fetch }) => {
		const formData = await request.formData();
		const menuId = formData.get('menu_id')?.toString();

		if (!menuId) {
			return fail(400, {
				action: 'delete',
				success: false,
				error: 'Не указан ID пункта меню'
			});
		}

		try {
			const response = await fetch(`${API_BASE_URL}/recruiter/company/menu/delete/${menuId}/`, {
				method: 'DELETE'
			});

			const result = await response.json();

			if (response.ok) {
				return {
					action: 'delete',
					success: true,
					message: result.message || 'Пункт меню успешно удалён'
				};
			} else {
				return fail(400, {
					action: 'delete',
					success: false,
					error: result.error || 'Не удалось удалить пункт меню'
				});
			}
		} catch (error) {
			console.error('Error deleting menu item:', error);
			return fail(500, {
				action: 'delete',
				success: false,
				error: 'Произошла ошибка при удалении пункта меню'
			});
		}
	},

	/**
	 * Toggle menu item status (active/inactive)
	 */
	toggleMenuStatus: async ({ request, fetch }) => {
		const formData = await request.formData();
		const menuId = formData.get('menu_id')?.toString();

		if (!menuId) {
			return fail(400, {
				action: 'toggleStatus',
				success: false,
				error: 'Не указан ID пункта меню'
			});
		}

		try {
			const response = await fetch(`${API_BASE_URL}/recruiter/company/menu/status/${menuId}/`, {
				method: 'POST'
			});

			const result = await response.json();

			if (response.ok) {
				return {
					action: 'toggleStatus',
					success: true,
					message: result.message || 'Статус пункта меню успешно обновлён',
					menu: result.menu
				};
			} else {
				return fail(400, {
					action: 'toggleStatus',
					success: false,
					error: result.error || 'Не удалось изменить статус пункта меню'
				});
			}
		} catch (error) {
			console.error('Error toggling menu status:', error);
			return fail(500, {
				action: 'toggleStatus',
				success: false,
				error: 'Произошла ошибка при изменении статуса пункта меню'
			});
		}
	}
};
