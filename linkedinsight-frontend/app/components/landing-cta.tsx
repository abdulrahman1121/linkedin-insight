/**
 * Landing Page Call-to-Action Section
 */

import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import Link from 'next/link';

export function LandingCTA() {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl rounded-2xl border bg-gradient-to-r from-primary/10 to-primary/5 p-8 md:p-12 text-center">
          <h2 className="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Ready to transform your career?
          </h2>
          <p className="mb-8 text-lg text-muted-foreground">
            Join LinkedInsight today and start your journey toward your dream career.
          </p>
          <Button asChild size="lg" className="text-lg">
            <Link href="/dashboard">
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}

