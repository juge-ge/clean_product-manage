import { router } from './index'

export async function setupRouter(app) {
  app.use(router)
  return router
}
