import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import axiosInstance from '../lib/axios';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (payload: {
    email: string;
    username: string;
    name: string;
    password: string;
    password2: string;
  }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    console.log('Initial auth state:', { hasToken: !!token });
    setIsAuthenticated(!!token);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      console.log('Attempting login for:', email);
      const response = await axiosInstance.post('/users/login/', {
        email,
        password,
      });
      
      console.log('Login response:', response.data);
      
      if (!response.data.access || !response.data.refresh) {
        throw new Error('Invalid response from server: missing tokens');
      }

      const { access, refresh } = response.data;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      setIsAuthenticated(true);
      console.log('Login successful, tokens stored');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (payload: {
    email: string;
    username: string;
    name: string;
    password: string;
    password2: string;
  }) => {
    try {
      console.log('Starting registration process for:', payload.email);
      const response = await axiosInstance.post('/users/register/', payload);
      console.log('Registration response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Registration error in AuthContext:', {
        error,
        isAxiosError: error instanceof Error,
        response: error instanceof Error && 'response' in error ? error.response : null,
      });
      throw error;
    }
  };

  const logout = () => {
    console.log('Logging out user');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsAuthenticated(false);
  };

  const value = {
    isAuthenticated,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};