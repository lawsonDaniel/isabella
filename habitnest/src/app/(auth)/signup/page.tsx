'use client';

import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Mail, Lock, ArrowRight, User, Upload, X } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

// Validation schema using Yup
const validationSchema = Yup.object({
  name: Yup.string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters')
    .required('Name is required'),
  email: Yup.string()
    .email('Please enter a valid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .max(50, 'Password must be less than 50 characters')
    .required('Password is required'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Please confirm your password'),
  profileImage: Yup.string()
    .nullable()
});

export default function SignUpForm() {
  // Note: In real Next.js app, uncomment the line below
  // const router = useRouter();
  
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      profileImage: ''
    },
    validationSchema: validationSchema,
    onSubmit: async (values, { setSubmitting, setStatus }) => {
      try {
        setStatus && setStatus(null);
        
        console.log('Form values:', values);
      } catch (error) {
        console.error('Signup error:', error);
        formik.setStatus({ 
          type: 'error', 
          message: 'Network error. Please check your connection.' 
        });
      } finally {
        formik.setSubmitting(false);
      }
    }
  });

  const handleSubmit = (e: any) => {
    e.preventDefault();
    formik.handleSubmit();
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check file size (limit to 5MB)
      if (file.size > 5 * 1024 * 1024) {
        formik.setFieldError('profileImage', 'Image size must be less than 5MB');
        return;
      }

      // Check file type
      if (!file.type.startsWith('image/')) {
        formik.setFieldError('profileImage', 'Please select a valid image file');
        return;
      }

      const reader = new FileReader();
      reader.onload = (event) => {
        const base64String = event.target?.result as string;
        formik.setFieldValue('profileImage', base64String);
        setImagePreview(base64String);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    formik.setFieldValue('profileImage', '');
    setImagePreview(null);
  };

  return (
    <div className="bg-gray-800 text-gray-400 font-sans text-sm font-normal leading-6 min-h-screen grid place-items-center py-8">
      <div className="w-full max-w-80 mx-auto px-4">
        <div className="grid gap-3.5 text-gray-200">
          {/* Profile Image Upload */}
          <div className="flex flex-col items-center mb-4">
            <div className="relative">
              {imagePreview ? (
                <div className="relative">
                  <img 
                    src={imagePreview} 
                    alt="Profile preview" 
                    className="w-20 h-20 rounded-full object-cover border-2 border-gray-600"
                  />
                  <button
                    type="button"
                    onClick={removeImage}
                    className="absolute -top-1 -right-1 bg-red-500 hover:bg-red-600 text-white rounded-full p-1 transition-colors duration-300"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ) : (
                <div className="w-20 h-20 rounded-full bg-gray-600 border-2 border-gray-500 border-dashed flex items-center justify-center">
                  <Upload className="w-6 h-6 text-gray-400" />
                </div>
              )}
            </div>
            <label htmlFor="profileImage" className="mt-2 text-xs text-center cursor-pointer text-pink-400 hover:text-pink-300 transition-colors duration-300">
              {imagePreview ? 'Change Photo' : 'Upload Profile Photo'}
            </label>
            <input
              id="profileImage"
              name="profileImage"
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
            />
            {formik.errors.profileImage && (
              <div className="text-red-400 text-xs mt-1 text-center">
                {formik.errors.profileImage}
              </div>
            )}
          </div>

          {/* Name Field */}
          <div className="flex flex-col">
            <div className="flex">
              <label 
                htmlFor="name" 
                className="bg-gray-700 px-5 py-4 rounded-l border-r-0 flex items-center justify-center"
              >
                <User className="w-4 h-4 fill-current" />
                <span className="sr-only">Name</span>
              </label>
              <input
                id="name"
                name="name"
                type="text"
                placeholder="Full Name"
                autoComplete="name"
                value={formik.values.name}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`flex-1 bg-gray-600 px-4 py-4 rounded-r border-l-0 transition-colors duration-300 hover:bg-gray-500 focus:bg-gray-500 focus:outline-none ${
                  formik.errors.name && formik.touched.name ? 'ring-2 ring-red-500' : ''
                }`}
              />
            </div>
            {formik.errors.name && formik.touched.name && (
              <div className="text-red-400 text-xs mt-1 px-1">
                {formik.errors.name}
              </div>
            )}
          </div>

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
                autoComplete="new-password"
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

          {/* Confirm Password Field */}
          <div className="flex flex-col">
            <div className="flex">
              <label 
                htmlFor="confirmPassword" 
                className="bg-gray-700 px-5 py-4 rounded-l border-r-0 flex items-center justify-center"
              >
                <Lock className="w-4 h-4 fill-current" />
                <span className="sr-only">Confirm Password</span>
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                placeholder="Confirm Password"
                autoComplete="new-password"
                value={formik.values.confirmPassword}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`flex-1 bg-gray-600 px-4 py-4 rounded-r border-l-0 transition-colors duration-300 hover:bg-gray-500 focus:bg-gray-500 focus:outline-none ${
                  formik.errors.confirmPassword && formik.touched.confirmPassword ? 'ring-2 ring-red-500' : ''
                }`}
              />
            </div>
            {formik.errors.confirmPassword && formik.touched.confirmPassword && (
              <div className="text-red-400 text-xs mt-1 px-1">
                {formik.errors.confirmPassword}
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
              {formik.isSubmitting ? 'CREATING ACCOUNT...' : 'CREATE ACCOUNT'}
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
          Already have an account?{' '}
          <Link href="/login" className="text-gray-200 hover:underline focus:underline">
            Sign in here
          </Link>
          {' '}
          <ArrowRight className="w-4 h-4 inline-block align-middle ml-1" />
        </p>
      </div>
    </div>
  );
}