using './main.bicep'

param staticWebAppName = 'swa-gotoguy-blog-prod'
param location = 'westeurope'
param skuName = 'Standard'
param tags = {
  workload: 'blog'
  app: 'gotoguy-blog'
  environment: 'prod'
  managedBy: 'bicep'
}
