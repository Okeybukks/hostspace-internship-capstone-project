# MongoDB Database Setup Guide

This guide outlines the steps to set up the database required to run the Kanban application. You can deploy the database both locally and in the cloud. The main difference between local and cloud deployments is the mechanism for creating a StorageClass needed to create Persistent Volumes and Persistent Volume Claims to store database data.

## Deployment Steps

1. **Manual Deployment**:
   - Navigate to the `database` folder.
   - Deploy the manifest files:
     ```bash
     kubectl create -f mongodb.yaml
     kubectl create -f mongo_service.yaml
     ```

2. **Deployment with ArgoCD**:
   - Copy the application manifest with `name: kanban-application-database` in the `argocd.yaml` file located in the root folder of this repo.

## Initializing Replica Set

Once the MongoDB resources are deployed, you need to initialize the replicaset:

```bash
# Connect to the MongoDB database
kubectl exec -it mongodb-0 -n kanban -- mongosh mongodb-0.mongo

# Initialize the replicaset
rs.initiate()

# Store the database configuration
var cfg = rs.config()

# Add primary to replica configuration
cfg.members[0].hosts = "mongodb-0.mongo:27017"

# Confirm configuration
rs.reconfig(cfg)

# Add secondary
rs.add("mongodb-1.mongo:27017")

# Check database status
rs.status()
```
## Creating Database and User
With the replicaset set up, create the database and user for the application:

```
# Connect to the primary database
kubectl exec -it mongodb-0 -n kanban -- mongosh mongodb-0.mongo

# Create database
use kanbanDB

# Create user
db.createUser({
  user: "username",
  pwd: "password",
  roles: [{ "role": "readWrite", "db": "kanbanDB" }]
})

# (Optional) Create test data
db.mycollection.insertOne({ name: 'John', age: 30 });
```

## Testing Database Connection

To test if you can log into the new database with the created user, execute the following command:

```
kubectl exec -it mongodb-0 -n kanban -- mongosh mongodb://username:password@mongo:27017/kanbanDB
```
If user creation was successful, you should be able to login to the `kanbanDB` database

When I tried to use the creaated user in pod two, I discovered I was having authentication issues, so I had to reconfigure
the replicaset using this command

```
rs.reconfig({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongodb-0.mongo:27017" },
    { _id: 1, host: "mongodb-1.mongo:27017" },
  ]
})
```

## Environment Variables and Secrets

This URL `mongodb://username:password@mongo:27017/kanbanDB` is value which is to be passed to the `MONGODB_URL` of the backend deployment but not directly. The value should be stored in the `MONGODB_URL` variable in the .env file which should not be pushed to the public.

Before pushing to the GitHub cloud repo, run the `secret_creator.py` program which creates a sealed secret that can be pushed to the Github cloud repo.

The .env file must be in your `.gitignore`
