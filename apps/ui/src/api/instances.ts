const API_BASE: string = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export interface InstanceStatus {
  instance_id: string
  workflow: string
  state: string
  active_elements: ActiveElement[]
}

export interface ActiveElement {
  element_id: string
  element_name: string
  element_type: string
  started_at: string
}

export async function getInstance(instanceId: string): Promise<InstanceStatus> {
  const res = await fetch(`${API_BASE}/instances/${instanceId}`)
  if (!res.ok) {
    throw new Error(`Failed to fetch instance: ${res.status}`)
  }
  return res.json() as Promise<InstanceStatus>
}
