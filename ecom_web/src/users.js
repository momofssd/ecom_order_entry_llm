export const users = [
    {
        id: 1,
        username: '1',
        password: '1',
        email: '1@gmail.com',
        isAdmin: true,
        customerCode: 'ALL'  // Admin has access to all customers
    },
    {
        id: 2,
        username: 'b',
        password: 'b',
        email: 'b@admin.com',
        isAdmin: false,
        customerCode: 'B'
    },
    {
        id: 3,
        username: 'c',
        password: 'c',
        email: 'c@admin.com',
        isAdmin: false,
        customerCode: 'C'
    },
    {
        id: 4,
        username: 'ba',
        password: 'ba',
        email: 'ba@admin.com',
        isAdmin: false,
        customerCode: 'BA'
    },
    {
        id: 5,
        username: 'g',
        password: 'g',
        email: 'g@admin.com',
        isAdmin: false,
        customerCode: 'G'
    },
    {
        id: 6,
        username: 'com',
        password: 'com',
        email: 'com@admin.com',
        isAdmin: false,
        customerCode: 'COM'
    },
    {
        id: 7,
        username: 'n',
        password: 'n',
        email: 'n@admin.com',
        isAdmin: false,
        customerCode: 'N'
    },

]
localStorage.setItem('users', JSON.stringify(users))
