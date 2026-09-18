/**
 * ARGUS API Client
 *
 * Abstracts data fetching so components never contain hardcoded URLs or mock JSON.
 * When VITE_USE_MOCKS=true and the API is unreachable, falls back to static data.
 *
 * Owner: Member 4
 */
import type { InvestigationResponse, Camera } from './types';
import { MOCK_INVESTIGATION, MOCK_CAMERAS } from './mockData';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === 'true';

async function apiFetch<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) throw new Error(`API ${res.status}`);
    return await res.json() as T;
  } catch {
    if (USE_MOCKS) {
      console.warn(`API unreachable for ${path}, using static mock.`);
      return fallback;
    }
    throw new Error(`API request failed for ${path} and mocks are disabled.`);
  }
}

export async function getInvestigation(id: string): Promise<InvestigationResponse> {
  return apiFetch<InvestigationResponse>(`/investigations/${id}`, MOCK_INVESTIGATION);
}

export async function getCameras(): Promise<Camera[]> {
  return apiFetch<Camera[]>('/cameras', MOCK_CAMERAS);
}
