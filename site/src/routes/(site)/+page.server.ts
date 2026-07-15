import type { PageServerLoad } from './$types';
import { getApiBaseUrl } from '$lib/config/env';

interface Category {
  id: number;
  name: string;
  slug: string;
}

interface Location {
  id: number;
  name: string;
  slug: string;
  jobs_count?: number;
}

interface Job {
  id: number;
  title: string;
  slug: string;
  company_name: string;
  company_logo: string;
  job_type: string;
  locations: Array<{ id: number; name: string; slug: string; state: string }>;
  skills: Array<{ id: number; name: string; slug: string }>;
  min_salary: number;
  max_salary: number;
  salary_display: string;
  experience_display: string;
  location_display: string;
  time_ago: string;
}

// Regional Truddy categories (must match industries fixture slugs)
const curatedCategorySlugs = [
  'roznichnaya-torgovlya',
  'transport-i-logistika',
  'stroitelstvo',
  'obschestvennoe-pitanie',
  'skladskoe-hozyaystvo',
  'meditsina-i-farmatsevtika',
  'obrazovanie',
  'ohrana-i-bezopasnost',
  'proizvodstvo',
  'zhkh-i-gorodskoe-hozyaystvo',
  'avtoservis-i-avtobiznes',
  'uslugi-naseleniyu'
];

async function fetchJson(url: string, timeoutMs = 8000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} for ${url}`);
    }
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

export const load: PageServerLoad = async () => {
  try {
    const apiBaseUrl = getApiBaseUrl();

    // Parallel SSR fetches — do not wait sequentially on cold Railway/Neon
    const [filterOptions, jobsData] = await Promise.all([
      fetchJson(`${apiBaseUrl}/jobs/filter-options/`),
      fetchJson(`${apiBaseUrl}/jobs/?page=1&page_size=8`)
    ]);

    const allCategories = filterOptions.industries || [];
    const matched = curatedCategorySlugs
      .map((slug) => allCategories.find((c: { slug: string }) => c.slug === slug))
      .filter(Boolean)
      .map((category: { id: number; name: string; slug: string }) => ({
        id: category.id,
        name: category.name.trim(),
        slug: category.slug
      })) as Category[];

    // Fallback: top industries by job count when curated list is empty
    const topCategories =
      matched.length > 0
        ? matched
        : (allCategories as Array<{ id: number; name: string; slug: string; count?: number }>)
            .slice()
            .sort((a, b) => (b.count || 0) - (a.count || 0))
            .slice(0, 12)
            .map((category) => ({
              id: category.id,
              name: category.name.trim(),
              slug: category.slug
            }));

    const topLocations = (filterOptions.locations || [])
      .slice()
      .sort((a: { count?: number }, b: { count?: number }) => (b.count || 0) - (a.count || 0))
      .slice(0, 12)
      .map((location: { id: number; name: string; slug: string; count?: number }) => ({
        id: location.id,
        name: location.name,
        slug: location.slug,
        jobs_count: location.count
      })) as Location[];

    const featuredJobs = (jobsData.results || []) as Job[];

    return {
      topCategories,
      topLocations,
      featuredJobs
    };
  } catch (error) {
    console.error('Error loading home page data:', error);
    return {
      topCategories: [] as Category[],
      topLocations: [] as Location[],
      featuredJobs: [] as Job[]
    };
  }
};
