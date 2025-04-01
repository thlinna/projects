import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try {
          const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/users/me`);
          setUser(res.data.data);
        } catch (err) {
          localStorage.removeItem('token');
          delete axios.defaults.headers.common['Authorization'];
          setToken(null);
          setError('Istunto vanhentunut. Kirjaudu uudelleen sisään.');
        }
      }
      setLoading(false);
    };

    loadUser();
  }, [token]);

  const register = async (userData) => {
    try {
      setLoading(true);
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/api/users`, userData);
      
      const { token: newToken } = res.data;
      localStorage.setItem('token', newToken);
      setToken(newToken);
      
      return { success: true };
    } catch (err) {
      setError(err.response?.data?.message || 'Rekisteröityminen epäonnistui');
      return { 
        success: false, 
        message: err.response?.data?.message || 'Rekisteröityminen epäonnistui' 
      };
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      setLoading(true);
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/api/users/login`, {
        email,
        password
      });
      
      const { token: newToken } = res.data;
      localStorage.setItem('token', newToken);
      setToken(newToken);
      
      return { success: true };
    } catch (err) {
      setError(err.response?.data?.message || 'Kirjautuminen epäonnistui');
      return { 
        success: false, 
        message: err.response?.data?.message || 'Kirjautuminen epäonnistui' 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setToken(null);
  };

  const resetError = () => {
    setError(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        error,
        register,
        login,
        logout,
        resetError
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext; 