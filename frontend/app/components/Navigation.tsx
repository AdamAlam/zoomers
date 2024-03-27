'use client';

import React, { useState } from 'react';
import {
  MobileMenuDialog,
  DialogContent,
  DialogDescription,
  DialogHeader
} from '@/components/ui/mobile-menu-dialog';

import { Bars3Icon, FilmIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

interface Props {
  item: {
    name: string;
    href: string;
  };
  mobile?: boolean;
}

const navigationItems = [{ name: 'Home', href: '/' }];

const NavigationItem = ({ item, mobile = false }: Props) => {
  const baseClassName = 'text-sm font-semibold leading-6 text-gray-900';
  const className = mobile
    ? '-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50'
    : baseClassName;

  return (
    <Link key={item.name} href={item.href} className={className}>
      {item.name}
    </Link>
  );
};

const MobileMenu = ({
  isOpen,
  onClose
}: {
  isOpen: boolean;
  onClose: () => void;
}) => {
  return (
    <MobileMenuDialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogDescription>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  {navigationItems.map(item => (
                    <NavigationItem key={item.name} item={item} mobile />
                  ))}
                </div>
                <div className="py-6">
                  <Link
                    href="logIn"
                    className="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                  >
                    Log in
                  </Link>
                </div>
              </div>
            </div>
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </MobileMenuDialog>
  );
};

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white">
      <nav
        className="mx-auto flex max-w-7xl items-center justify-between gap-x-6 p-6 lg:px-8"
        aria-label="Global"
      >
        <div className="flex lg:flex-1">
          <Link
            href="/"
            className="hidden lg:block lg:text-sm lg:font-semibold lg:leading-6 lg:text-gray-900"
          >
            <FilmIcon className="h-6 w-6" aria-hidden="true" />
          </Link>
        </div>
        <div className="hidden lg:flex lg:gap-x-12">
          {navigationItems.map(item => (
            <NavigationItem key={item.name} item={item} />
          ))}
        </div>
        <div className="flex flex-1 items-center justify-end gap-x-6">
          <Link
            href="/login"
            className="hidden lg:block lg:text-sm lg:font-semibold lg:leading-6 lg:text-gray-900"
          >
            Log in
          </Link>
          <Link
            href="/signUp"
            className="rounded-md bg-gradient-to-br from-black to-neutral-600 px-3 py-2 text-sm font-medium text-white shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-zinc-800 dark:from-zinc-900 dark:to-zinc-900 dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
          >
            Sign up
          </Link>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
            onClick={() => setMobileMenuOpen(true)}
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
      </nav>
      <MobileMenu
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      />
    </header>
  );
}
