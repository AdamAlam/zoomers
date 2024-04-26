'use client';
import { jwtDecode } from 'jwt-decode';
import { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        if (Date.now() >= (decoded.exp ?? 0) * 1000) {
          localStorage.removeItem('authToken');
          setIsAuthenticated(false);
        } else {
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Failed to decode JWT:', error);
        localStorage.removeItem('authToken');
      }
    }
  }, []);

  const login = () => setIsAuthenticated(true);

  const logout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
  };

  return (
    // FIXME: Fix any type
    <AuthContext.Provider value={{ isAuthenticated, login, logout } as any}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
