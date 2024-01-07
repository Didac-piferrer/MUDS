db.createUser(
    {
        user: 'didac',
        pwd: '12345',
        roles: [
            { role: "clusterMonitor", db: "admin" },
            { role: "dbOwner", db: "db_name" },
            { role: 'readWrite', db: 'db_hero' }
        ]
    }
)