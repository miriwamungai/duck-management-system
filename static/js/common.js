const getUser = () => {
  const userStr = sessionStorage.getItem('user');
  console.log(userStr)
  if (userStr) return JSON.parse(userStr);
  else return null;
};

// return the token from the session storage
const getToken = () => {
  return sessionStorage.getItem('token') || null;
};

const getRole = () => {
  return sessionStorage.getItem('role') || null;
};

// remove the token and user from the session storage
const removeUserSession = () => {
  sessionStorage.removeItem('token');
  sessionStorage.removeItem('role');
  sessionStorage.removeItem('user');
};

// set the token and user from the session storage
const setUserSession = (token, role, user) => {
  sessionStorage.setItem('token', token);
  sessionStorage.setItem('role', role);
  sessionStorage.setItem('user', JSON.stringify(user));
};

