'use client';

import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Mail, Lock, ArrowRight } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

// Validation schema using Yup
const validationSchema = Yup.object({
  email: Yup.string()
    .email('Please enter a valid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .max(50, 'Password must be less than 50 characters')
    .required('Password is required')
});

export default function LoginForm() {
  // Note: In real Next.js app, uncomment the line below
  // const router = useRouter();

  const formik = useFormik({
    initialValues: {
      email: '',
      password: ''
    },
    validationSchema: validationSchema,
    onSubmit: async (values, { setSubmitting, setStatus }) => {
      try {
        setStatus && setStatus(null);
        
        // Next.js API route call
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(values),
        });

        const data = await response.json();

        if (response.ok) {
          formik.setStatus({ type: 'success', message: 'Login successful!' });
          
          // Redirect to dashboard after successful login
          // In real Next.js app, uncomment the line below
          // router.push('/dashboard');
          
          console.log('Login successful, would redirect to /dashboard');
        } else {
          formik.setStatus({ 
            type: 'error', 
            message: data.message || 'Login failed. Please try again.' 
          });
        }
      } catch (error) {
        console.error('Login error:', error);
        formik.setStatus({ 
          type: 'error', 
          message: 'Network error. Please check your connection.' 
        });
      } finally {
        formik.setSubmitting(false);
      }
    }
  });

  const handleSubmit = (e:any) => {
    e.preventDefault();
    formik.handleSubmit();
  };

  return (
    <div className="bg-gray-800 text-gray-400 font-sans text-sm font-normal leading-6 min-h-screen grid place-items-center">
      <div className="w-full max-w-80 mx-auto px-4">
        <div className="grid gap-3.5 text-gray-200">
          {/* Email Field */}
          <div className="flex flex-col">
            <div className="flex">
              <label 
                htmlFor="email" 
                className="bg-gray-700 px-5 py-4 rounded-l border-r-0 flex items-center justify-center"
              >
                <Mail className="w-4 h-4 fill-current" />
                <span className="sr-only">Email</span>
              </label>
              <input
                id="email"
                name="email"
                type="email"
                placeholder="Email"
                autoComplete="email"
                value={formik.values.email}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`flex-1 bg-gray-600 px-4 py-4 rounded-r border-l-0 transition-colors duration-300 hover:bg-gray-500 focus:bg-gray-500 focus:outline-none ${
                  formik.errors.email && formik.touched.email ? 'ring-2 ring-red-500' : ''
                }`}
              />
            </div>
            {formik.errors.email && formik.touched.email && (
              <div className="text-red-400 text-xs mt-1 px-1">
                {formik.errors.email}
              </div>
            )}
          </div>

          {/* Password Field */}
          <div className="flex flex-col">
            <div className="flex">
              <label 
                htmlFor="password" 
                className="bg-gray-700 px-5 py-4 rounded-l border-r-0 flex items-center justify-center"
              >
                <Lock className="w-4 h-4 fill-current" />
                <span className="sr-only">Password</span>
              </label>
              <input
                id="password"
                name="password"
                type="password"
                placeholder="Password"
                autoComplete="current-password"
                value={formik.values.password}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`flex-1 bg-gray-600 px-4 py-4 rounded-r border-l-0 transition-colors duration-300 hover:bg-gray-500 focus:bg-gray-500 focus:outline-none ${
                  formik.errors.password && formik.touched.password ? 'ring-2 ring-red-500' : ''
                }`}
              />
            </div>
            {formik.errors.password && formik.touched.password && (
              <div className="text-red-400 text-xs mt-1 px-1">
                {formik.errors.password}
              </div>
            )}
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              onClick={handleSubmit}
              disabled={formik.isSubmitting}
              className={`w-full font-bold uppercase px-4 py-4 rounded transition-colors duration-300 focus:outline-none ${
                formik.isSubmitting 
                  ? 'bg-gray-500 text-gray-300 cursor-not-allowed' 
                  : 'bg-pink-600 text-gray-200 cursor-pointer hover:bg-pink-700 focus:bg-pink-700'
              }`}
            >
              {formik.isSubmitting ? 'SIGNING IN...' : 'SIGN IN'}
            </button>
          </div>

          {/* Status Messages */}
          {formik.status && (
            <div className={`text-center text-sm px-2 py-1 rounded ${
              formik.status.type === 'success' 
                ? 'text-green-400 bg-green-900/20' 
                : 'text-red-400 bg-red-900/20'
            }`}>
              {formik.status.message}
            </div>
          )}
        </div>
        
        <p className="text-center mt-6 mb-6">
          Not a member?{' '}
          <Link href="/signup" className="text-gray-200 hover:underline focus:underline">
            Sign up now
          </Link>
          {' '}
          <ArrowRight className="w-4 h-4 inline-block align-middle ml-1" />
        </p>
      </div>
    </div>
  );
}
