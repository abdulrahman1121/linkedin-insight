/**
 * Landing Page Call-to-Action Section
 */

import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import Link from 'next/link';

export function LandingCTA() {
  return (
    <section className="py-20 md:py-32 bg-white">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl rounded-2xl border-2 border-[#0077B5]/20 bg-gradient-to-r from-[#0077B5]/5 via-[#0077B5]/10 to-[#0077B5]/5 p-8 md:p-12 text-center shadow-lg">
          <h2 className="mb-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Ready to transform your career?
          </h2>
          <p className="mb-8 text-lg text-gray-600">
            Join LinkedInsight today and start your journey toward your dream career.
          </p>
          <Button 
            asChild 
            size="lg" 
            className="text-lg bg-[#0077B5] hover:bg-[#004182] text-white font-semibold px-8 py-6 rounded-full shadow-lg hover:shadow-xl transition-all"
          >
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

