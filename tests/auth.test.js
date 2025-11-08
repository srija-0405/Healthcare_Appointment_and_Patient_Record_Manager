// This is tests/auth.test.js
const login = require('../src/auth');

test('login function should return true for correct credentials', () => {
  // This test checks if login('admin', 'admin') returns true
  expect(login('admin', 'admin')).toBe(true);
});

test('login function should return false for incorrect credentials', () => {
  // This test checks if login('admin', 'wrong') returns false
  expect(login('admin', 'wrong')).toBe(false);
});