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

export interface TaskItem {
  task_id: string
  element_id: string
  element_name: string | null
  assignee: string | null
}

export async function getInstance(instanceId: string): Promise<InstanceStatus> {
  const res = await fetch(`${API_BASE}/instances/${instanceId}`)
  if (!res.ok) {
    throw new Error(`Failed to fetch instance: ${res.status}`)
  }
  return res.json() as Promise<InstanceStatus>
}

export async function listTasks(instanceId: string): Promise<TaskItem[]> {
  const res = await fetch(`${API_BASE}/instances/${instanceId}/tasks`)
  if (!res.ok) {
    throw new Error(`Failed to fetch tasks: ${res.status}`)
  }
  return res.json() as Promise<TaskItem[]>
}

export async function completeTask(
  instanceId: string,
  taskId: string,
  outcome: 'approved' | 'skipped',
  reason?: string,
): Promise<void> {
  const res = await fetch(`${API_BASE}/instances/${instanceId}/tasks/${taskId}/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ outcome, reason: reason ?? '' }),
  })
  if (!res.ok) {
    throw new Error(`Failed to complete task: ${res.status}`)
  }
}
