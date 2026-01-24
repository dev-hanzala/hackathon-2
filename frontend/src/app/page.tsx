'use client';

/**
 * Home page - redirects to tasks if authenticated, otherwise shows landing page.
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { CheckCircle2, ListTodo, TrendingUp } from 'lucide-react';
import { useAuthContext } from '@/components/AuthProvider';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuthContext();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/tasks');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header with Theme Toggle */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 md:py-6 flex justify-between items-center">
          <h2 className="text-xl font-bold text-foreground">Todo Evolution</h2>
          <ThemeToggle />
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 pt-28 pb-20 text-center">
        <h1 className="text-5xl font-extrabold text-foreground mb-6 sm:text-6xl lg:text-7xl">
          Todo Evolution
        </h1>
        <p className="text-xl text-muted-foreground mb-4 max-w-2xl mx-auto">
          Your personal productivity companion
        </p>
        <p className="text-lg text-muted-foreground mb-10 max-w-3xl mx-auto">
          Transform the way you manage tasks with an intuitive, powerful, and beautifully designed todo application. 
          Stay organized, track progress, and achieve more every day.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-20">
          <Button asChild size="lg" className="text-lg px-8 py-6">
            <Link href="/auth/signup">
              Get Started
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg" className="text-lg px-8 py-6">
            <Link href="/auth/signin">
              Sign In
            </Link>
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-24 bg-muted/30">
        <h2 className="text-3xl font-bold text-center text-foreground mb-12">
          Why Choose Todo Evolution?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Feature 1: Quick Task Creation */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <CheckCircle2 className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Quick Task Creation</CardTitle>
              <CardDescription>
                Add tasks in seconds with our streamlined interface. No complexity, just simplicity.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Lightning-fast input</li>
                <li>• Instant task organization</li>
                <li>• Minimal clicks required</li>
              </ul>
            </CardContent>
          </Card>

          {/* Feature 2: Task Organization */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <ListTodo className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Task Organization</CardTitle>
              <CardDescription>
                Keep your tasks structured and easy to find. Never lose track of what matters.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Clear task categorization</li>
                <li>• Smart filtering options</li>
                <li>• Intuitive list views</li>
              </ul>
            </CardContent>
          </Card>

          {/* Feature 3: Progress Tracking */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <TrendingUp className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Progress Tracking</CardTitle>
              <CardDescription>
                Watch your productivity soar with visual progress indicators and completion stats.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Visual task completion</li>
                <li>• Achievement milestones</li>
                <li>• Motivational insights</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="container mx-auto px-4 py-20 md:py-28 text-center">
        <h2 className="text-3xl font-bold text-foreground mb-6">
          Ready to boost your productivity?
        </h2>
        <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
          Join thousands of users who have transformed their task management with Todo Evolution.
        </p>
        <Button asChild size="lg" className="text-lg px-8 py-6">
          <Link href="/auth/signup">
            Start Free Today
          </Link>
        </Button>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>&copy; 2026 Todo Evolution. Built with Next.js and shadcn/ui.</p>
        </div>
      </footer>
    </div>
  );
}
