'use client';

/**
 * User sign-in page.
 * Migrated to shadcn/ui components for consistent styling.
 */

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';
import { useAuthContext } from '@/components/AuthProvider';
import { APIError } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function SigninPage() {
  const router = useRouter();
  const { signin, isLoading } = useAuthContext();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }
    
    try {
      await signin(email, password);
      router.push('/tasks');
    } catch (err) {
      const apiError = err as APIError;
      setError(apiError.detail || 'Sign in failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-bold">Sign in to your account</CardTitle>
          <CardDescription>
            Or{' '}
            <Link href="/auth/signup" className="font-medium text-primary hover:underline">
              create a new account
            </Link>
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <form className="space-y-4" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md bg-destructive/10 p-4">
                <p className="text-sm text-destructive">{error}</p>
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="email">Email address</Label>
              <Input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
              />
            </div>

            <div className="flex items-center justify-end">
              <Link 
                href="#" 
                className="text-sm font-medium text-primary hover:underline"
              >
                Forgot your password?
              </Link>
            </div>

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Signing in...
                </span>
              ) : (
                'Sign in'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
