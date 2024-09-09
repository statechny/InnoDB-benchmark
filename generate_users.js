const mysql = require('mysql2');
const { faker } = require('@faker-js/faker');
const util = require('util');

// MySQL connection configuration
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    database: 'test_db',   // The database you created
    connectTimeout: 10000
});

// node native promisify
const query = util.promisify(connection.query).bind(connection);

// Function to generate a single user
const generateUser = () => {
    const name = faker.person.fullName();
    const email = faker.internet.email();
    const dateOfBirth = faker.date.birthdate({ min: 18, max: 80, mode: 'age' });
    return [name, email, dateOfBirth.toISOString().split('T')[0]];
}

// Function to bulk insert users
const insertUsers = async (batchSize, totalUsers) => {
    let users = [];

    for (let i = 0; i < totalUsers; i++) {
        users.push(generateUser());

        // Insert in batches
        if (users.length === batchSize) {
            console.log(`Inserting batch of ${users.length} users`);
            await query(
                'INSERT INTO users (name, email, date_of_birth) VALUES ?',
                [users.map(user => [user[0], user[1], user[2]])]  // Correct format for batch insertion
            );
            users = [];  // Clear the batch
        }
    }

    // Insert remaining users if the last batch is incomplete
    if (users.length > 0) {
        console.log(`Inserting remaining ${users.length} users`);
        await query(
            'INSERT INTO users (name, email, date_of_birth) VALUES ?',
            [users.map(user => [user[0], user[1], user[2]])]  // Correct format for batch insertion
        );
    }

    connection.end(); // Close the connection after all inserts
}

// Generate and insert users
const batchSize = 1000;       // Number of users per batch
const totalUsers = 4000000;  // Total number of users to generate
console.log(`Inserting ${totalUsers} users...`);

insertUsers(batchSize, totalUsers)
    .then(() => console.log('All users inserted successfully'))
    .catch(err => console.error('Error inserting users:', err));
