import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-primary-700">NeuroVision AI</h1>
            <div className="mt-8 bg-white p-8 rounded-lg shadow-sm border border-gray-200">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl text-primary-700">✓</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Check your email</h2>
              <p className="text-gray-600 mb-6">
                We've sent password reset instructions to {email}
              </p>
              <Link to="/login" className="btn-primary w-full block text-center">
                Return to Login
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-primary-700 text-center">NeuroVision AI</h1>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            Reset your password
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Enter your email address and we'll send you instructions to reset your password
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
              placeholder="doctor@hospital.com"
            />
          </div>

          <div>
            <button type="submit" className="btn-primary w-full">
              Send Reset Instructions
            </button>
          </div>
        </form>

        <div className="text-center">
          <Link to="/login" className="text-sm font-medium text-primary-700 hover:text-primary-800">
            Back to login
          </Link>
        </div>
      </div>
    </div>
  );
}
