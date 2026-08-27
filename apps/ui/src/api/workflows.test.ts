import { afterEach, describe, expect, it, vi } from 'vitest'
import { listWorkflows } from './workflows'

describe('listWorkflows', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('returns parsed workflows on success', async () => {
    const workflows = [
      { id: 'wf-1', name: 'Workflow 1', version: 1, definition_key: '1' },
    ]
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(workflows),
      }),
    )

    await expect(listWorkflows()).resolves.toEqual(workflows)
  })

  it('throws when the response is not ok', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.resolve({}),
      }),
    )

    await expect(listWorkflows()).rejects.toThrow(
      'Failed to fetch workflows: 500',
    )
  })
})
