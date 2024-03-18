'use client';
import React, { useState } from 'react';
import { Label } from './../components/ui/label';
import { Input } from './../components/ui/input';
import { cn } from '../utils/cn';
import {
  IconBrandGithub,
  IconBrandGoogle,
  IconBrandOnlyfans
} from '@tabler/icons-react';
import { supabase } from '../lib/supabase/supabaseClient';
import { Provider } from '@supabase/supabase-js';
import { useToast } from '@/components/ui/use-toast';
import { z } from 'zod';

const SignUp = () => {
  const { toast } = useToast();

  const [formData, setFormData] = useState({});

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Form submitted');
    toast({ title: 'Form submitted', description: 'success' });
  };

  const handleOAuthLogin = async (provider: Provider) => {
    await supabase.auth.signInWithOAuth({
      provider: provider
    });
  };

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const FormSchema = z
    .object({
      email: z.string().email(),
      password: z.string().min(6),
      passwordConfirm: z.string().min(6),
      firstname: z.string(),
      lastname: z.string()
    })
    .refine(data => data.password === data.passwordConfirm, {
      message: 'Passwords do not match',
      path: ['passwordConfirm']
    });

  return (
    <div className="mx-auto w-full max-w-md rounded-none bg-white p-4 shadow-input dark:bg-black md:rounded-2xl md:p-8">
      <h2 className="text-xl font-bold text-neutral-800 dark:text-neutral-200">
        Welcome to APP NAME HERE
      </h2>
      <p className="mt-2 max-w-sm text-sm text-neutral-600 dark:text-neutral-300">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
      </p>

      <form className="my-8" onSubmit={handleSubmit}>
        <div className="mb-4 flex flex-col space-y-2 md:flex-row md:space-x-2 md:space-y-0">
          <LabelInputContainer>
            <Label htmlFor="firstname">First name</Label>
            <Input
              name="firstname"
              placeholder="Tyler"
              type="text"
              onChange={handleFormChange}
            />
          </LabelInputContainer>
          <LabelInputContainer>
            <Label htmlFor="lastname">Last name</Label>
            <Input
              name="lastname"
              placeholder="Durden"
              type="text"
              onChange={handleFormChange}
            />
          </LabelInputContainer>
        </div>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="email">Email Address</Label>
          <Input
            name="email"
            placeholder="projectmayhem@fc.com"
            type="email"
            onChange={handleFormChange}
          />
        </LabelInputContainer>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="password">Password</Label>
          <Input
            name="password"
            placeholder="••••••••"
            type="password"
            onChange={handleFormChange}
          />
        </LabelInputContainer>
        <LabelInputContainer className="mb-8">
          <Label htmlFor="passwordConfirm">Confirm Password</Label>
          <Input
            name="passwordConfirm"
            placeholder="••••••••"
            type="password"
            onChange={handleFormChange}
          />
        </LabelInputContainer>

        <button
          className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-black to-neutral-600 font-medium text-white shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-zinc-800 dark:from-zinc-900 dark:to-zinc-900 dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
          type="submit"
        >
          Sign up &rarr;
          <BottomGradient />
        </button>

        <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-neutral-700" />

        <div className="flex flex-col space-y-4">
          <button
            className=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
            type="submit"
            onClick={() => handleOAuthLogin('github')}
          >
            <IconBrandGithub className="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
            <span className="text-sm text-neutral-700 dark:text-neutral-300">
              GitHub
            </span>
            <BottomGradient />
          </button>
          <button
            className=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
            type="submit"
            onClick={() => handleOAuthLogin('google')}
          >
            <IconBrandGoogle className="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
            <span className="text-sm text-neutral-700 dark:text-neutral-300">
              Google
            </span>
            <BottomGradient />
          </button>
          <button
            className=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
            type="submit"
          >
            <IconBrandOnlyfans className="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
            <span className="text-sm text-neutral-700 dark:text-neutral-300">
              OnlyFans
            </span>
            <BottomGradient />
          </button>
        </div>
      </form>
    </div>
  );
};

const BottomGradient = () => {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
    </>
  );
};

const LabelInputContainer = ({
  children,
  className
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div className={cn('flex w-full flex-col space-y-2', className)}>
      {children}
    </div>
  );
};
export default SignUp;
