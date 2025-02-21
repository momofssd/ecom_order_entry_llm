export const users = [
    {
        id: 1,
        username: '1',
        password: '1',
        email: '1@gmail.com',
        isAdmin: true
    },
    {
        id: 2,
        username: '2',
        password: '2',
        email: '2@admin.com',
        isAdmin: false
    },

]
localStorage.setItem('users', JSON.stringify(users))
