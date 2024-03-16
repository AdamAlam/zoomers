import React from 'react';
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="text-center">
      <h1 className="mt-4 text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">
        <span className="font-bold text-indigo-600">404</span> Not Found
      </h1>
      <div className="mt-10 flex items-center justify-center gap-x-6">
        <Link
          href="/"
          className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
          Go back home
        </Link>
      </div>
    </div>
  );
}
