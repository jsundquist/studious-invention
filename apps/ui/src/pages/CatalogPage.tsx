import { useEffect, useState } from 'react'
import {
  Alert,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  Stack,
  Typography,
} from '@mui/material'
import { listWorkflows, type WorkflowSummary } from '../api/workflows'

export default function CatalogPage() {
  const [workflows, setWorkflows] = useState<WorkflowSummary[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    listWorkflows()
      .then((result) => {
        if (!cancelled) {
          setWorkflows(result)
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(
            err instanceof Error ? err.message : 'Failed to load workflows',
          )
        }
      })

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Artifact Catalog
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {!error && workflows === null && (
        <Stack sx={{ mt: 4, alignItems: 'center' }}>
          <CircularProgress />
        </Stack>
      )}

      {!error && workflows !== null && workflows.length === 0 && (
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          No workflows are available yet.
        </Typography>
      )}

      {!error && workflows !== null && workflows.length > 0 && (
        <Stack spacing={2} sx={{ mt: 2 }}>
          {workflows.map((workflow) => (
            <Card key={workflow.definition_key} variant="outlined">
              <CardContent>
                <Stack
                  direction="row"
                  sx={{ justifyContent: 'space-between', alignItems: 'center' }}
                >
                  <Typography variant="h6">{workflow.name}</Typography>
                  <Chip label={`v${workflow.version}`} size="small" />
                </Stack>
                <Typography variant="body2" color="text.secondary">
                  {workflow.id}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Stack>
      )}
    </Container>
  )
}
