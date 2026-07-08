import { Container, Typography } from '@mui/material'

export default function CatalogPage() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Artifact Catalog
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Workflow instances will appear here.
      </Typography>
    </Container>
  )
}
