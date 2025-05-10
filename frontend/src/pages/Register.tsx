import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

export const Register = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted');
    setError('');
    setIsLoading(true);
    setSuccess(false);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      setIsLoading(false);
      return;
    }

    try {
      console.log('Attempting registration with:', { email });

      const payload = {
        email,
        username,
        name,
        password,
        password2: confirmPassword,
      };

      const response = await register(payload);
      console.log('Registration successful:', response);
      setSuccess(true);

      // Clear form
      setEmail('');
      setUsername('');
      setName('');
      setPassword('');
      setConfirmPassword('');

      // Show success message for 2 seconds before redirecting
      setTimeout(() => {
        console.log('Navigating to login page');
        navigate('/login');
      }, 2000);
    } catch (err) {
      console.error('Registration error details:', {
        error: err,
        isAxiosError: axios.isAxiosError(err),
        response: axios.isAxiosError(err) ? err.response : null,
      });

      if (axios.isAxiosError(err)) {
        if (err.response?.data) {
          if (typeof err.response.data === 'string') {
            setError(err.response.data);
          } else if (err.response.data.email) {
            setError(err.response.data.email[0]);
          } else if (err.response.data.password) {
            setError(err.response.data.password[0]);
          } else if (err.response.data.detail) {
            setError(err.response.data.detail);
          } else {
            setError('Registration failed. Please check your information and try again.');
          }
        } else if (err.response?.status === 400) {
          setError('Invalid email or password format');
        } else if (err.response?.status === 409) {
          setError('An account with this email already exists');
        } else if (!err.response) {
          setError('Network error. Please check your connection');
        } else {
          setError('Registration failed. Please try again later');
        }
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
            Create your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}
          {success && (
            <div className="rounded-md bg-green-50 p-4">
              <div className="text-sm text-green-700">
                Registration successful! Redirecting to login...
              </div>
            </div>
          )}
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                type="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isLoading || success}
              />
            </div>
            <div>
              <input
                type="text"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={isLoading || success}
              />
            </div>
            <div>
              <input
                type="text"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={isLoading || success}
              />
            </div>
            <div>
              <input
                type="password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading || success}
              />
            </div>
            <div>
              <input
                type="password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={isLoading || success}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading || success}
              className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
                isLoading || success ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
              } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
            >
              {isLoading ? 'Registering...' : success ? 'Registration Successful!' : 'Register'}
            </button>
          </div>
        </form>
        <div className="text-center">
          <Link
            to="/login"
            className="font-medium text-indigo-600 hover:text-indigo-500"
          >
            Already have an account? Sign in
          </Link>
        </div>
      </div>
    </div>
  );
};