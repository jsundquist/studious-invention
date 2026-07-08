import { createBrowserRouter } from 'react-router-dom'
import CatalogPage from './pages/CatalogPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <CatalogPage />,
  },
])

export default router
