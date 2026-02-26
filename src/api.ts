const API_BASE_URL = 'http://localhost:8000/api';

export async function fetchWithTimeout(resource: string, options: RequestInit = {}) {
    const { timeout = 8000 } = options as any;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(`${API_BASE_URL}${resource}`, {
        ...options,
        signal: controller.signal
    });
    clearTimeout(id);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
}

export const api = {
    getCategories: () => fetchWithTimeout('/categories/'),
    getCategory: (id: number) => fetchWithTimeout(`/categories/${id}`),
    getCategoryTree: () => fetchWithTimeout('/categories/tree'),

    getProducts: (params?: Record<string, any>) => {
        const queryString = params
            ? '?' + new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)])).toString()
            : '';
        return fetchWithTimeout(`/products/${queryString}`);
    },

    getProduct: (id: number) => fetchWithTimeout(`/products/${id}`),
};
