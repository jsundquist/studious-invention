const API_BASE: string = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export interface WorkflowSummary {
  id: string
  name: string
  version: number
  definition_key: string
}

export async function listWorkflows(): Promise<WorkflowSummary[]> {
  const res = await fetch(`${API_BASE}/workflows`)
  if (!res.ok) {
    throw new Error(`Failed to fetch workflows: ${res.status}`)
  }
  return res.json() as Promise<WorkflowSummary[]>
}
