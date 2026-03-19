// Static API Service
// Replaces the heavy SQLite WebAssembly engine with instant JSON fetching

const API_BASE = import.meta.env.BASE_URL + 'api';

export async function fetchCategories() {
  const response = await fetch(`${API_BASE}/categories.json`);
  if (!response.ok) throw new Error('Failed to fetch categories');
  return response.json();
}

export async function fetchCategoryItems(categoryId) {
  const response = await fetch(`${API_BASE}/category/${categoryId}.json`);
  if (!response.ok) throw new Error('Failed to fetch category items');
  return response.json();
}

export async function fetchSubindexItems(parentId) {
  const response = await fetch(`${API_BASE}/subindex/${parentId}.json`);
  if (!response.ok) {
    if (response.status === 404) return []; // No children
    throw new Error('Failed to fetch subindex items');
  }
  return response.json();
}

export async function fetchLines(subindexId) {
  const response = await fetch(`${API_BASE}/lines/${subindexId}.json`);
  if (!response.ok) throw new Error('Failed to fetch lines');
  return response.json();
}

let cachedSearchIndex = null;

export async function fetchBookmarkItems(ids) {
  if (!ids || ids.length === 0) return [];

  if (!cachedSearchIndex) {
    const response = await fetch(`${API_BASE}/search_index.json`);
    if (!response.ok) throw new Error('Failed to fetch search index');
    cachedSearchIndex = await response.json();
  }

  // Find the items matching the bookmarked IDs
  return cachedSearchIndex
    .filter(item => ids.includes(item.id))
    .map(item => ({
      Id: item.id,
      EnglishIndexName: item.title_en,
      UrduIndexName: item.title_ur,
      RUrduIndexName: item.title_ru,
      GujaratiIndexName: item.title_gu
    }));
}

export async function searchGlobal(term, lang) {
  if (!term || term.trim() === '') return [];
  term = term.toLowerCase();

  // Load the search index once into memory
  if (!cachedSearchIndex) {
    const response = await fetch(`${API_BASE}/search_index.json`);
    if (!response.ok) throw new Error('Failed to fetch search index');
    cachedSearchIndex = await response.json();
  }

  // Perform in-memory fuzzy search
  const results = cachedSearchIndex.filter(item => {
    return (
      (item.title_en && item.title_en.toLowerCase().includes(term)) ||
      (item.title_ur && item.title_ur.toLowerCase().includes(term)) ||
      (item.title_ru && item.title_ru.toLowerCase().includes(term)) ||
      (item.title_gu && item.title_gu.toLowerCase().includes(term)) ||
      (item.text_ar && item.text_ar.toLowerCase().includes(term)) ||
      (item.text_en && item.text_en.toLowerCase().includes(term)) ||
      (item.text_ur && item.text_ur.toLowerCase().includes(term)) ||
      (item.text_ru && item.text_ru.toLowerCase().includes(term)) ||
      (item.text_gu && item.text_gu.toLowerCase().includes(term))
    );
  });

  // Limit to 50 results to keep the UI snappy
  return results.slice(0, 50).map(item => ({
    SubindexId: item.id,
    EnglishTitle: item.title_en,
    UrduTitle: item.title_ur,
    RUrduTitle: item.title_ru,
    GujaratiTitle: item.title_gu,
    ArabicText1: item.text_ar ? item.text_ar.substring(0, 50) : ''
  }));
}