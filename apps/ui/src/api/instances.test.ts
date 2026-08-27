import { afterEach, describe, expect, it, vi } from 'vitest'
import { completeTask, getInstance, listTasks } from './instances'

describe('instances api client', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('getInstance returns parsed instance status on success', async () => {
    const instance = {
      instance_id: '1',
      workflow: 'wf-1',
      state: 'ACTIVE',
      active_elements: [],
    }
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue({ ok: true, json: () => Promise.resolve(instance) }),
    )

    await expect(getInstance('1')).resolves.toEqual(instance)
  })

  it('getInstance throws when the response is not ok', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, status: 404 }),
    )

    await expect(getInstance('missing')).rejects.toThrow(
      'Failed to fetch instance: 404',
    )
  })

  it('listTasks returns parsed tasks on success', async () => {
    const tasks = [
      {
        task_id: 't-1',
        element_id: 'review',
        element_name: 'Review',
        assignee: null,
      },
    ]
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue({ ok: true, json: () => Promise.resolve(tasks) }),
    )

    await expect(listTasks('1')).resolves.toEqual(tasks)
  })

  it('completeTask posts outcome and reason', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true })
    vi.stubGlobal('fetch', fetchMock)

    await completeTask('1', 't-1', 'skipped', 'not applicable')

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/instances/1/tasks/t-1/complete',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ outcome: 'skipped', reason: 'not applicable' }),
      }),
    )
  })

  it('completeTask throws when the response is not ok', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, status: 502 }),
    )

    await expect(completeTask('1', 't-1', 'approved')).rejects.toThrow(
      'Failed to complete task: 502',
    )
  })
})
