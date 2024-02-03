var dbName = 'my_test_database';
db = db.getSiblingDB(dbName);

// Create a test collection
db.createCollection('test_collection');
db.your_collection_name.insert([
    
    { name: 'Test', surname: 'Neri'}
]);

db.your_collection_name.createIndex({ name: 1 });

print('Initialization complete.');
