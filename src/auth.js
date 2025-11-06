// This is src/auth.js
function login(username, password) {
  if (username === "admin" && password === "admin") {
    return true;
  }
  return false;
}

module.exports = login;