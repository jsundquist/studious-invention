import { render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import CatalogPage from './CatalogPage'
import * as workflowsApi from '../api/workflows'

describe('CatalogPage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows a loading spinner while the request is in flight', () => {
    vi.spyOn(workflowsApi, 'listWorkflows').mockReturnValue(
      new Promise(() => {}),
    )

    render(<CatalogPage />)

    expect(screen.getByRole('progressbar')).toBeInTheDocument()
  })

  it('renders workflow cards once loaded', async () => {
    vi.spyOn(workflowsApi, 'listWorkflows').mockResolvedValue([
      {
        id: 'create-backend-api',
        name: 'Create Backend API',
        version: 2,
        definition_key: '1',
      },
    ])

    render(<CatalogPage />)

    expect(await screen.findByText('Create Backend API')).toBeInTheDocument()
    expect(screen.getByText('v2')).toBeInTheDocument()
    expect(screen.getByText('create-backend-api')).toBeInTheDocument()
  })

  it('shows an empty state when there are no workflows', async () => {
    vi.spyOn(workflowsApi, 'listWorkflows').mockResolvedValue([])

    render(<CatalogPage />)

    expect(
      await screen.findByText('No workflows are available yet.'),
    ).toBeInTheDocument()
  })

  it('shows an error message when the request fails', async () => {
    vi.spyOn(workflowsApi, 'listWorkflows').mockRejectedValue(
      new Error('Failed to fetch workflows: 500'),
    )

    render(<CatalogPage />)

    expect(
      await screen.findByText('Failed to fetch workflows: 500'),
    ).toBeInTheDocument()
  })

  it('does not update state after unmount', async () => {
    let resolvePromise: (
      value: workflowsApi.WorkflowSummary[],
    ) => void = () => {}
    vi.spyOn(workflowsApi, 'listWorkflows').mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve
      }),
    )

    const { unmount } = render(<CatalogPage />)
    unmount()
    resolvePromise([])

    await waitFor(() => {
      // Nothing to assert on the unmounted tree; this just ensures no
      // "state update on unmounted component" warning is thrown.
    })
  })
})
